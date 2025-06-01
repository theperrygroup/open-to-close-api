# Basic smoke tests
import open_to_close_api


def test_import():
    assert hasattr(open_to_close_api, "OpenToCloseAPI")
    assert hasattr(open_to_close_api, "__version__")


def test_client_instantiation():
    client = open_to_close_api.OpenToCloseAPI("test_key")
    assert client is not None
