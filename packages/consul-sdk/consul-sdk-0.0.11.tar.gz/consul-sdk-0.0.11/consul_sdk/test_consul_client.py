import time
from os import environ
from unittest.mock import patch

import pytest

from consul_sdk.client import ConsulClient


@pytest.fixture
def client():
    yield ConsulClient(url=environ.get("CONSUL_ADDR", "http://127.0.0.1:8500"))


@pytest.mark.integration
def test_create_and_get_session(client):
    session_id = client.create_session(30)
    assert session_id == client.get_session(session_id)


@pytest.mark.integration
def test_renew_session(client):
    session_id = client.create_session(10)
    assert session_id == client.get_session(session_id)

    time.sleep(9)
    client.renew_session(session_id)

    time.sleep(2)
    assert client.get_session(session_id) is not None


@pytest.mark.skip("Failing")
def test_get_session_returns_none_if_session_expired(client):
    session_id = client.create_session(10)
    assert session_id == client.get_session(session_id)

    time.sleep(15)
    assert client.get_session(session_id) is None


@pytest.mark.integration
def test_acquire_and_release_lock(client):
    session_id = client.create_session(10)

    assert client.acquire_lock("my-key", session_id)
    assert client.release_lock("my-key", session_id)


@pytest.mark.integration
def test_acquire_and_release_txn_locks(client):
    session_id = client.create_session(10)

    assert client.acquire_locks(["my-key-1", "my-key-2", "my-key-3"], session_id)
    assert client.release_locks(["my-key-1", "my-key-2", "my-key-3"], session_id)


@pytest.mark.integration
def test_acquire_and_reacquire_same_txn_locks_raises_error(client):
    session_id_1 = client.create_session(10)
    session_id_2 = client.create_session(10)

    assert client.acquire_locks(["my-key-1", "my-key-2"], session_id_1)
    assert not client.acquire_locks(["my-key-1"], session_id_2)

    assert client.release_locks(["my-key-1", "my-key-2"], session_id_1)

    assert client.acquire_locks(["my-key-1"], session_id_2)
    assert client.release_locks(["my-key-1"], session_id_2)


@pytest.mark.integration
def test_legacy_lock_works_with_new_txn_locks(client):
    session_id_1 = client.create_session(10)
    session_id_2 = client.create_session(10)

    assert client.acquire_lock("my-key-1", session_id_1)
    assert client.release_locks(["my-key-1"], session_id_1)

    assert client.acquire_lock("my-key-1", session_id_2)
    assert not client.acquire_locks(["my-key-1"], session_id_1)
    assert client.release_lock("my-key-1", session_id_2)

    assert client.acquire_locks(["my-key-1", "my-key-2"], session_id_1)
    assert not client.acquire_lock("my-key-1", session_id_2)
    assert client.release_lock("my-key-1", session_id_1)
    assert client.release_lock("my-key-2", session_id_1)


@pytest.mark.integration
def test_successful_lock_acquired_released_for_64_and_above_keys(client):
    keys = [f"my-key-{i}" for i in range(65)]
    session_id_1 = client.create_session(10)
    session_id_2 = client.create_session(10)

    assert client.acquire_lock("my-key-1", session_id_1)
    assert not client.acquire_locks(keys, session_id_2)
    assert client.release_locks(["my-key-1"], session_id_1)

    assert client.acquire_locks(keys, session_id_2)
    assert not client.acquire_lock("my-key-1", session_id_1)
    assert client.release_locks(keys[0:64], session_id_2)
    assert client.release_lock(keys[64], session_id_2)

    assert client.acquire_locks(keys, session_id_1)
    assert client.release_locks(keys, session_id_1)


@pytest.mark.integration
def test_bulk_locks_gives_unable_to_acquire_lock_after_few_iterations_check_acquired_locks_are_reverted(
    client,
):
    keys = [f"my-key-{i}" for i in range(70)]
    session_id_1 = client.create_session(10)
    session_id_2 = client.create_session(10)

    assert client.acquire_lock("my-key-66", session_id_1)
    assert not client.acquire_locks(keys, session_id_2)
    assert client.acquire_locks(keys[:65], session_id_2)
    assert client.release_locks(keys[:65], session_id_2)
    assert client.release_lock("my-key-66", session_id_1)


@patch("consul_sdk.client.ConsulClient._acquire_locks")
@patch("consul_sdk.client.ConsulClient.release_locks")
def test_bulk_locks_gives_exc_after_few_iterations_check_acquired_locks_are_reverted(
    fake_release, fake__acquire_locks, client
):
    keys = [f"my-key-{i}" for i in range(70)]
    fake__acquire_locks.side_effect = [True, RuntimeError]

    with pytest.raises(RuntimeError):
        assert not client.acquire_locks(keys, "dummy_session")
        assert fake_release.called


@patch("consul_sdk.client.ConsulClient._acquire_locks")
@patch("consul_sdk.client.ConsulClient.release_locks")
def test_bulk_locks_unable_to_acquire_lock_after_few_iterations_check_acquired_locks_are_reverted_unit_test(
    fake_release, fake__acquire_locks, client
):
    keys = [f"my-key-{i}" for i in range(70)]
    fake__acquire_locks.side_effect = [True, False]

    assert not client.acquire_locks(keys, "dummy_session")
    assert fake_release.called


@pytest.mark.integration
def test_bulk_lock_for_single_key(client):
    session_id_1 = client.create_session(10)
    session_id_2 = client.create_session(10)
    key = "dummy_fleet:dummy_vehicle_allocation/dummy_vehicle_id/4d7e8ac0-b95b-427a-0000-00fd8ce00000"

    assert client.acquire_locks([key], session_id_1)
    assert not client.acquire_locks([key], session_id_2)
    assert client.release_locks([key], session_id_1)
