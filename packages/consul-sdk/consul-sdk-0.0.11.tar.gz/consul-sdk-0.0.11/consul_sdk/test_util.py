from consul_sdk.util import chunk


def test_chunk():
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert chunk(x, 5) == [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
