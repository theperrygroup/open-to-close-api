import pytest
from unittest.mock import MagicMock, patch
from open_to_close_api.client import OpenToCloseAPI
from open_to_close_api.users import UsersAPI

@pytest.fixture
def client() -> OpenToCloseAPI:
    """Provides an OpenToCloseAPI client instance for testing."""
    return OpenToCloseAPI(api_key="test_api_key")

@pytest.fixture
def users_api(client: OpenToCloseAPI) -> UsersAPI:
    """Provides a UsersAPI instance for testing."""
    return UsersAPI(client)

def test_list_users_success(users_api: UsersAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a list of users."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1, "name": "Alice"}]}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        params = {"role": "agent"}
        result = users_api.list_users(params=params)
        mock_method.assert_called_once_with("GET", "/users", params=params)
    assert result == [{"id": 1, "name": "Alice"}]

def test_create_user_success(users_api: UsersAPI, client: OpenToCloseAPI) -> None:
    """Tests successful creation of a user."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"data": {"id": 2, "name": "Bob"}}
    user_data = {"name": "Bob", "email": "bob@example.com"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = users_api.create_user(user_data=user_data)
        mock_method.assert_called_once_with("POST", "/users", json_data=user_data)
    assert result == {"id": 2, "name": "Bob"}

def test_retrieve_user_success(users_api: UsersAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a specific user."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "Alice"}}
    user_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = users_api.retrieve_user(user_id=user_id)
        mock_method.assert_called_once_with("GET", f"/users/{user_id}")
    assert result == {"id": 1, "name": "Alice"}

def test_update_user_success(users_api: UsersAPI, client: OpenToCloseAPI) -> None:
    """Tests successful update of a user."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "Alicia"}}
    user_id = 1
    update_data = {"name": "Alicia"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = users_api.update_user(user_id=user_id, user_data=update_data)
        mock_method.assert_called_once_with("PUT", f"/users/{user_id}", json_data=update_data)
    assert result == {"id": 1, "name": "Alicia"}

def test_delete_user_success_204(users_api: UsersAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a user with a 204 response."""
    mock_response = MagicMock()
    mock_response.status_code = 204
    user_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = users_api.delete_user(user_id=user_id)
        mock_method.assert_called_once_with("DELETE", f"/users/{user_id}")
    assert result == {}

def test_delete_user_success_json_response(users_api: UsersAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a user with a JSON response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "User deleted"}
    user_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = users_api.delete_user(user_id=user_id)
        mock_method.assert_called_once_with("DELETE", f"/users/{user_id}")
    assert result == {"message": "User deleted"}

def test_list_users_empty(users_api: UsersAPI, client: OpenToCloseAPI) -> None:
    """Tests listing users when API returns an empty list."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = users_api.list_users()
        mock_method.assert_called_once_with("GET", "/users", params=None)
    assert result == []

def test_list_users_no_data_key(users_api: UsersAPI, client: OpenToCloseAPI) -> None:
    """Tests listing users when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = users_api.list_users()
        mock_method.assert_called_once_with("GET", "/users", params=None)
    assert result == []

def test_create_user_no_data_key(users_api: UsersAPI, client: OpenToCloseAPI) -> None:
    """Tests creating a user when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {}
    user_data = {"name": "Charlie"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = users_api.create_user(user_data)
        mock_method.assert_called_once_with("POST", "/users", json_data=user_data)
    assert result == {}

def test_retrieve_user_no_data_key(users_api: UsersAPI, client: OpenToCloseAPI) -> None:
    """Tests retrieving a user when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    user_id = 404
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = users_api.retrieve_user(user_id)
        mock_method.assert_called_once_with("GET", f"/users/{user_id}")
    assert result == {}

def test_update_user_no_data_key(users_api: UsersAPI, client: OpenToCloseAPI) -> None:
    """Tests updating a user when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    user_id = 404
    update_data = {"name": "Charles"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = users_api.update_user(user_id, update_data)
        mock_method.assert_called_once_with("PUT", f"/users/{user_id}", json_data=update_data)
    assert result == {} 