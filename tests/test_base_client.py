"""Tests for BaseClient functionality."""

import pytest
from unittest.mock import Mock, patch
import requests

from open_to_close.base_client import BaseClient
from open_to_close.exceptions import (
    AuthenticationError,
    NetworkError,
    NotFoundError,
    OpenToCloseAPIError,
    RateLimitError,
    ServerError,
    ValidationError,
)


class TestBaseClient:
    """Test BaseClient functionality."""

    @patch.dict("os.environ", {}, clear=True)
    @patch("open_to_close.base_client.load_dotenv")
    def test_init_without_api_key_raises_error(self, mock_load_dotenv: Mock) -> None:
        """Test that BaseClient raises AuthenticationError without API key."""
        with pytest.raises(AuthenticationError, match="API key is required"):
            BaseClient()

    @patch.dict("os.environ", {"OPEN_TO_CLOSE_API_KEY": "env_api_key"}, clear=True)
    @patch("open_to_close.base_client.load_dotenv")
    def test_init_with_env_api_key(self, mock_load_dotenv: Mock) -> None:
        """Test BaseClient initialization with API key from environment."""
        client = BaseClient()
        assert client.api_key == "env_api_key"
        assert client.base_url == "https://api.opentoclose.com/v1"

    def test_init_with_direct_api_key(self) -> None:
        """Test BaseClient initialization with directly provided API key."""
        client = BaseClient(api_key="direct_api_key")
        assert client.api_key == "direct_api_key"
        assert client.base_url == "https://api.opentoclose.com/v1"

    def test_init_with_custom_base_url(self) -> None:
        """Test BaseClient initialization with custom base URL."""
        client = BaseClient(api_key="test_key", base_url="https://custom.api.com")
        assert client.api_key == "test_key"
        assert client.base_url == "https://custom.api.com"

    def test_session_headers(self) -> None:
        """Test that session headers are set correctly."""
        client = BaseClient(api_key="test_key")
        expected_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        for key, value in expected_headers.items():
            assert client.session.headers.get(key) == value

    @patch("open_to_close.base_client.requests.Session.request")
    def test_handle_response_200(self, mock_request: Mock) -> None:
        """Test handling successful 200 response."""
        client = BaseClient(api_key="test_key")
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.content = b'{"id": 1, "name": "test"}'
        response.json.return_value = {"id": 1, "name": "test"}

        result = client._handle_response(response)
        assert result == {"id": 1, "name": "test"}

    @patch("open_to_close.base_client.requests.Session.request")
    def test_handle_response_201(self, mock_request: Mock) -> None:
        """Test handling successful 201 response."""
        client = BaseClient(api_key="test_key")
        response = Mock(spec=requests.Response)
        response.status_code = 201
        response.content = b'{"id": 1, "name": "created"}'
        response.json.return_value = {"id": 1, "name": "created"}

        result = client._handle_response(response)
        assert result == {"id": 1, "name": "created"}

    @patch("open_to_close.base_client.requests.Session.request")
    def test_handle_response_204(self, mock_request: Mock) -> None:
        """Test handling 204 No Content response."""
        client = BaseClient(api_key="test_key")
        response = Mock(spec=requests.Response)
        response.status_code = 204
        response.content = b""

        result = client._handle_response(response)
        assert result == {}

    @patch("open_to_close.base_client.requests.Session.request")
    def test_handle_response_400_validation_error(self, mock_request: Mock) -> None:
        """Test handling 400 Bad Request response."""
        client = BaseClient(api_key="test_key")
        response = Mock(spec=requests.Response)
        response.status_code = 400
        response.content = b'{"message": "Invalid request"}'
        response.json.return_value = {"message": "Invalid request"}

        with pytest.raises(ValidationError, match="Bad request: Invalid request"):
            client._handle_response(response)

    @patch("open_to_close.base_client.requests.Session.request")
    def test_handle_response_401_authentication_error(self, mock_request: Mock) -> None:
        """Test handling 401 Unauthorized response."""
        client = BaseClient(api_key="test_key")
        response = Mock(spec=requests.Response)
        response.status_code = 401
        response.content = b'{"message": "Invalid credentials"}'
        response.json.return_value = {"message": "Invalid credentials"}

        with pytest.raises(
            AuthenticationError, match="Authentication failed: Invalid credentials"
        ):
            client._handle_response(response)

    @patch("open_to_close.base_client.requests.Session.request")
    def test_handle_response_404_not_found_error(self, mock_request: Mock) -> None:
        """Test handling 404 Not Found response."""
        client = BaseClient(api_key="test_key")
        response = Mock(spec=requests.Response)
        response.status_code = 404
        response.content = b'{"message": "Resource not found"}'
        response.json.return_value = {"message": "Resource not found"}

        with pytest.raises(
            NotFoundError, match="Resource not found: Resource not found"
        ):
            client._handle_response(response)

    @patch("open_to_close.base_client.requests.Session.request")
    def test_handle_response_429_rate_limit_error(self, mock_request: Mock) -> None:
        """Test handling 429 Rate Limit response."""
        client = BaseClient(api_key="test_key")
        response = Mock(spec=requests.Response)
        response.status_code = 429
        response.content = b'{"message": "Too many requests"}'
        response.json.return_value = {"message": "Too many requests"}

        with pytest.raises(
            RateLimitError, match="Rate limit exceeded: Too many requests"
        ):
            client._handle_response(response)

    @patch("open_to_close.base_client.requests.Session.request")
    def test_handle_response_500_server_error(self, mock_request: Mock) -> None:
        """Test handling 500 Server Error response."""
        client = BaseClient(api_key="test_key")
        response = Mock(spec=requests.Response)
        response.status_code = 500
        response.content = b'{"message": "Internal server error"}'
        response.json.return_value = {"message": "Internal server error"}

        with pytest.raises(ServerError, match="Server error: Internal server error"):
            client._handle_response(response)

    @patch("open_to_close.base_client.requests.Session.request")
    def test_handle_response_unknown_error(self, mock_request: Mock) -> None:
        """Test handling unknown error response."""
        client = BaseClient(api_key="test_key")
        response = Mock(spec=requests.Response)
        response.status_code = 418  # I'm a teapot
        response.content = b'{"message": "Unknown error"}'
        response.json.return_value = {"message": "Unknown error"}

        with pytest.raises(
            OpenToCloseAPIError, match="Unexpected error: Unknown error"
        ):
            client._handle_response(response)

    @patch("open_to_close.base_client.requests.Session.request")
    def test_handle_response_invalid_json(self, mock_request: Mock) -> None:
        """Test handling response with invalid JSON."""
        client = BaseClient(api_key="test_key")
        response = Mock(spec=requests.Response)
        response.status_code = 400
        response.content = b"invalid json"
        response.text = "invalid json"
        response.json.side_effect = ValueError("Invalid JSON")

        with pytest.raises(ValidationError, match="Bad request: invalid json"):
            client._handle_response(response)

    @patch("open_to_close.base_client.requests.Session.request")
    def test_handle_response_no_content(self, mock_request: Mock) -> None:
        """Test handling response with no content."""
        client = BaseClient(api_key="test_key")
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.content = b""

        result = client._handle_response(response)
        assert result == {}

    @patch("open_to_close.base_client.requests.Session.request")
    def test_request_method(self, mock_session_request: Mock) -> None:
        """Test the _request method."""
        client = BaseClient(api_key="test_key")

        # Mock response
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.content = b'{"id": 1}'
        response.json.return_value = {"id": 1}
        mock_session_request.return_value = response

        result = client._request("GET", "/test", params={"limit": 10})

        # Check that session.request was called with correct parameters
        mock_session_request.assert_called_once_with(
            method="GET",
            url="https://api.opentoclose.com/v1/test",
            json=None,
            data=None,
            files=None,
            params={"limit": 10, "api_token": "test_key"},
        )
        assert result == {"id": 1}

    @patch("open_to_close.base_client.requests.Session.request")
    def test_request_network_error(self, mock_session_request: Mock) -> None:
        """Test _request method with network error."""
        client = BaseClient(api_key="test_key")
        mock_session_request.side_effect = requests.exceptions.ConnectionError(
            "Connection failed"
        )

        with pytest.raises(NetworkError, match="Network error: Connection failed"):
            client._request("GET", "/test")

    @patch("open_to_close.base_client.requests.Session.request")
    def test_get_method(self, mock_session_request: Mock) -> None:
        """Test the get method."""
        client = BaseClient(api_key="test_key")

        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.content = b'{"data": "test"}'
        response.json.return_value = {"data": "test"}
        mock_session_request.return_value = response

        result = client.get("/test", params={"page": 1})

        mock_session_request.assert_called_once_with(
            method="GET",
            url="https://api.opentoclose.com/v1/test",
            json=None,
            data=None,
            files=None,
            params={"page": 1, "api_token": "test_key"},
        )
        assert result == {"data": "test"}

    @patch("open_to_close.base_client.requests.Session.request")
    def test_post_method(self, mock_session_request: Mock) -> None:
        """Test the post method."""
        client = BaseClient(api_key="test_key")

        response = Mock(spec=requests.Response)
        response.status_code = 201
        response.content = b'{"id": 1, "created": true}'
        response.json.return_value = {"id": 1, "created": True}
        mock_session_request.return_value = response

        json_data = {"name": "Test", "value": 123}
        result = client.post("/test", json_data=json_data)

        mock_session_request.assert_called_once_with(
            method="POST",
            url="https://api.opentoclose.com/v1/test",
            json=json_data,
            data=None,
            files=None,
            params={"api_token": "test_key"},
        )
        assert result == {"id": 1, "created": True}

    @patch("open_to_close.base_client.requests.Session.request")
    def test_put_method(self, mock_session_request: Mock) -> None:
        """Test the put method."""
        client = BaseClient(api_key="test_key")

        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.content = b'{"id": 1, "updated": true}'
        response.json.return_value = {"id": 1, "updated": True}
        mock_session_request.return_value = response

        json_data = {"name": "Updated Test"}
        result = client.put("/test/1", json_data=json_data)

        mock_session_request.assert_called_once_with(
            method="PUT",
            url="https://api.opentoclose.com/v1/test/1",
            json=json_data,
            data=None,
            files=None,
            params={"api_token": "test_key"},
        )
        assert result == {"id": 1, "updated": True}

    @patch("open_to_close.base_client.requests.Session.request")
    def test_delete_method(self, mock_session_request: Mock) -> None:
        """Test the delete method."""
        client = BaseClient(api_key="test_key")

        response = Mock(spec=requests.Response)
        response.status_code = 204
        response.content = b""
        mock_session_request.return_value = response

        result = client.delete("/test/1")

        mock_session_request.assert_called_once_with(
            method="DELETE",
            url="https://api.opentoclose.com/v1/test/1",
            json=None,
            data=None,
            files=None,
            params={"api_token": "test_key"},
        )
        assert result == {}

    @patch("open_to_close.base_client.requests.Session.request")
    def test_patch_method(self, mock_session_request: Mock) -> None:
        """Test the patch method."""
        client = BaseClient(api_key="test_key")

        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.content = b'{"id": 1, "patched": true}'
        response.json.return_value = {"id": 1, "patched": True}
        mock_session_request.return_value = response

        json_data = {"status": "active"}
        result = client.patch("/test/1", json_data=json_data)

        mock_session_request.assert_called_once_with(
            method="PATCH",
            url="https://api.opentoclose.com/v1/test/1",
            json=json_data,
            data=None,
            files=None,
            params={"api_token": "test_key"},
        )
        assert result == {"id": 1, "patched": True}

    @patch("open_to_close.base_client.requests.Session.request")
    def test_request_with_leading_slash_endpoint(
        self, mock_session_request: Mock
    ) -> None:
        """Test _request method with endpoint that has leading slash."""
        client = BaseClient(api_key="test_key")

        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.content = b'{"data": "test"}'
        response.json.return_value = {"data": "test"}
        mock_session_request.return_value = response

        result = client._request("GET", "/test")

        # URL should be correctly formed even with leading slash
        mock_session_request.assert_called_once_with(
            method="GET",
            url="https://api.opentoclose.com/v1/test",
            json=None,
            data=None,
            files=None,
            params={"api_token": "test_key"},
        )

    @patch("open_to_close.base_client.requests.Session.request")
    def test_request_with_files(self, mock_session_request: Mock) -> None:
        """Test _request method with files parameter."""
        client = BaseClient(api_key="test_key")

        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.content = b'{"uploaded": true}'
        response.json.return_value = {"uploaded": True}
        mock_session_request.return_value = response

        files = {"file": ("test.txt", "file content")}
        result = client.post("/upload", files=files)

        mock_session_request.assert_called_once_with(
            method="POST",
            url="https://api.opentoclose.com/v1/upload",
            json=None,
            data=None,
            files=files,
            params={"api_token": "test_key"},
        )
        assert result == {"uploaded": True}

    @patch("open_to_close.base_client.requests.Session.request")
    def test_request_with_data(self, mock_session_request: Mock) -> None:
        """Test _request method with data parameter."""
        client = BaseClient(api_key="test_key")

        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.content = b'{"submitted": true}'
        response.json.return_value = {"submitted": True}
        mock_session_request.return_value = response

        data = {"form_field": "value"}
        result = client.post("/form", data=data)

        mock_session_request.assert_called_once_with(
            method="POST",
            url="https://api.opentoclose.com/v1/form",
            json=None,
            data=data,
            files=None,
            params={"api_token": "test_key"},
        )
        assert result == {"submitted": True}
