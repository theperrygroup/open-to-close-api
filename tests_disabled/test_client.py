import pytest
import os
import requests
from unittest.mock import patch, MagicMock
from open_to_close_api.client import OpenToCloseAPI

@pytest.fixture
def client() -> OpenToCloseAPI:
    """Provides an OpenToCloseAPI client instance for testing."""
    return OpenToCloseAPI(api_key="test_api_key")

def test_client_initialization_with_api_key(client: OpenToCloseAPI) -> None:
    """Tests API client initialization with a direct API key."""
    assert client.api_key == "test_api_key"
    assert client.base_url == "https://api.opentoclose.com/v1"
    assert "Authorization" in client.headers
    assert client.headers["Authorization"] == "Bearer test_api_key"

@patch.dict(os.environ, {"OPEN_TO_CLOSE_API_KEY": "env_api_key"})
def test_client_initialization_from_env() -> None:
    """Tests API client initialization from environment variables."""
    client = OpenToCloseAPI()
    assert client.api_key == "env_api_key"
    assert client.headers["Authorization"] == "Bearer env_api_key"

def test_client_initialization_no_api_key() -> None:
    """Tests API client initialization raises ValueError if no API key is found."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="API key not provided and not found in environment variables."):
            OpenToCloseAPI()

@patch('requests.request')
def test_request_success(mock_request: MagicMock, client: OpenToCloseAPI) -> None:
    """Tests a successful API request."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "success"}
    mock_response.raise_for_status = MagicMock()
    mock_request.return_value = mock_response

    response = client._request("GET", "/test_endpoint", params={"param": "value"})

    mock_request.assert_called_once_with(
        "GET",
        "https://api.opentoclose.com/v1/test_endpoint",
        headers=client.headers,
        params={"param": "value"},
        json=None
    )
    response.raise_for_status.assert_called_once()
    assert response.json() == {"data": "success"}

@patch('requests.request')
def test_request_failure(mock_request: MagicMock, client: OpenToCloseAPI) -> None:
    """Tests an API request that results in an HTTP error."""
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Client Error")
    mock_request.return_value = mock_response

    with pytest.raises(requests.exceptions.HTTPError, match="Client Error"):
        client._request("POST", "/another_endpoint", json_data={"key": "value"})

    mock_request.assert_called_once_with(
        "POST",
        "https://api.opentoclose.com/v1/another_endpoint",
        headers=client.headers,
        params=None,
        json={"key": "value"}
    )
    mock_response.raise_for_status.assert_called_once() 