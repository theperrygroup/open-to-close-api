# Basic smoke tests
import open_to_close


def test_package_imports() -> None:
    assert hasattr(open_to_close, "OpenToCloseAPI")
    assert hasattr(open_to_close, "__version__")


def test_basic_client_instantiation() -> None:
    client = open_to_close.OpenToCloseAPI("test_key")
    assert client is not None
