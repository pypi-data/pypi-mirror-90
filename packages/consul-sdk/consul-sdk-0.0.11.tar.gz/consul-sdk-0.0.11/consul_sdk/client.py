from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus
from typing import List, Dict

import requests
from retrying import retry, RetryError

from consul_sdk.util import chunk


class ConsulClient:
    def __init__(self, url="http://127.0.0.1:8500", service_name=None):
        if not url.startswith("http://") and not url.startswith("https://"):
            url = f"http://{url}"

        self._url = url
        self._service_name = service_name
        self._chunk_size = 64  # ref: https://github.com/hashicorp/consul/issues/2921

    def acquire_lock(self, key, session_id):
        payload = {"acquire": session_id}
        return self._put_key(key, payload)

    def release_lock(self, key, session_id):
        payload = {"release": session_id}
        return self._put_key(key, payload)

    def acquire_locks(self, keys: List[str], session_id):
        return self._execute_bulk_txn(
            keys=keys,
            session_id=session_id,
            fn=self._acquire_locks,
            revert_fn=self.release_locks,
        )

    def release_locks(self, keys: List[str], session_id):
        return self._execute_bulk_txn(
            keys=keys,
            session_id=session_id,
            fn=self._release_locks,
            revert_fn=self.acquire_locks,
        )

    def _execute_bulk_txn(self, keys: List[str], session_id, fn, revert_fn):
        keys = list(set(keys))
        batched_keys = chunk(it=keys, size=self._chunk_size)
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(fn, keys=ks, session_id=session_id)
                for ks in batched_keys
            ]

            success, exceptions, failed = [], [], []
            for i, future in enumerate(futures):
                try:
                    result = future.result()
                except RuntimeError as e:
                    exceptions.append(str(e))
                else:
                    success.append(batched_keys[i]) if result else failed.append(
                        batched_keys[i]
                    )

            if exceptions or failed:
                if success:
                    r_keys = [ss for s in success for ss in s]
                    revert_fn(keys=r_keys, session_id=session_id)
                if exceptions:
                    raise RuntimeError(f"Consul request failed. {exceptions}")

            return len(success) == len(batched_keys)

    def _acquire_locks(self, keys, session_id):
        @retry(
            stop_max_attempt_number=3,
            retry_on_exception=lambda exc: isinstance(exc, RuntimeError),
            retry_on_result=lambda result: result is False,
            wait_fixed=0.5,
        )
        def _acquire_lock(keys, sess_id):
            payload = self._lock_payload(type="lock", keys=keys, session_id=sess_id)
            return self._run_in_txn(payload)

        try:
            return _acquire_lock(keys, session_id)
        except RetryError as e:
            return False

    def _release_locks(self, keys, session_id):
        @retry(
            stop_max_attempt_number=3,
            retry_on_exception=lambda exc: isinstance(exc, RuntimeError),
            retry_on_result=lambda result: result is False,
            wait_fixed=0.5,
        )
        def _acquire_lock(keys, sess_id):
            payload = self._lock_payload(type="unlock", keys=keys, session_id=sess_id)
            return self._run_in_txn(payload)

        try:
            return _acquire_lock(keys, session_id)
        except RetryError as e:
            return False

    def get_key(self, key):
        response = requests.get(f"{self._url}/v1/kv/{key}")

        if response.status_code == HTTPStatus.NOT_FOUND:
            return None

        self._assert_response(response)
        return response.json()[0]

    def create_session(
        self, ttl_in_secs: int, lock_delay_in_secs: int = 15, behavior="release"
    ):
        payload = {
            "LockDelay": f"{lock_delay_in_secs}s",
            "Name": self._service_name,
            "Node": None,
            "Checks": [],
            "Behavior": behavior,
            "TTL": f"{ttl_in_secs}s",
        }

        response = requests.put(f"{self._url}/v1/session/create", json=payload)
        self._assert_response(response)

        return response.json()["ID"]

    def renew_session(self, session_id):
        response = requests.put(f"{self._url}/v1/session/renew/{session_id}")
        self._assert_response(response)

    def get_session(self, session_id):
        response = requests.get(f"{self._url}/v1/session/info/{session_id}")
        self._assert_response(response)

        data = response.json()
        if len(data) == 0:
            return None

        session = data[0]
        return session["ID"]

    def _lock_payload(self, type: str, keys: List[str], session_id: str):
        return [
            {"KV": {"Verb": type, "Key": key, "Value": None, "Session": session_id}}
            for key in keys
        ]

    def _put_key(self, key, payload):
        response = requests.put(f"{self._url}/v1/kv/{key}", params=payload)
        self._assert_response(response)

        return response.json()

    def _run_in_txn(self, payload: List[Dict]):
        response = requests.put(f"{self._url}/v1/txn", json=payload)
        if response.status_code == HTTPStatus.CONFLICT:
            return False

        self._assert_response(response)
        return response.json()

    def _assert_response(self, response):
        if response.status_code != HTTPStatus.OK:
            raise RuntimeError(
                f"""
                Consul request failed.

                Status code: {response.status_code}
                Body:

                {response.text}
            """
            )
