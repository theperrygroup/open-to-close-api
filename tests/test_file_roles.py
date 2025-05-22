import pytest
from unittest.mock import MagicMock, patch
from open_to_close_api.client import OpenToCloseAPI
from open_to_close_api.file_roles import FileRolesAPI

@pytest.fixture
def client() -> OpenToCloseAPI:
    """Provides an OpenToCloseAPI client instance for testing."""
    return OpenToCloseAPI(api_key="test_api_key")

@pytest.fixture
def file_roles_api(client: OpenToCloseAPI) -> FileRolesAPI:
    """Provides a FileRolesAPI instance for testing."""
    return FileRolesAPI(client)

def test_list_file_roles_success(file_roles_api: FileRolesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a list of file roles."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1, "name": "Contract"}]}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        params = {"scope": "global"}
        result = file_roles_api.list_file_roles(params=params)
        mock_method.assert_called_once_with("GET", "/file_roles", params=params)
    assert result == [{"id": 1, "name": "Contract"}]

def test_create_file_role_success(file_roles_api: FileRolesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful creation of a file role."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"data": {"id": 2, "name": "Disclosure"}}
    file_role_data = {"name": "Disclosure"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = file_roles_api.create_file_role(file_role_data=file_role_data)
        mock_method.assert_called_once_with("POST", "/file_roles", json_data=file_role_data)
    assert result == {"id": 2, "name": "Disclosure"}

def test_retrieve_file_role_success(file_roles_api: FileRolesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a specific file role."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "Contract"}}
    file_role_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = file_roles_api.retrieve_file_role(file_role_id=file_role_id)
        mock_method.assert_called_once_with("GET", f"/file_roles/{file_role_id}")
    assert result == {"id": 1, "name": "Contract"}

def test_update_file_role_success(file_roles_api: FileRolesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful update of a file role."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "Signed Contract"}}
    file_role_id = 1
    update_data = {"name": "Signed Contract"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = file_roles_api.update_file_role(file_role_id=file_role_id, file_role_data=update_data)
        mock_method.assert_called_once_with("PUT", f"/file_roles/{file_role_id}", json_data=update_data)
    assert result == {"id": 1, "name": "Signed Contract"}

def test_delete_file_role_success_204(file_roles_api: FileRolesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a file role with a 204 response."""
    mock_response = MagicMock()
    mock_response.status_code = 204
    file_role_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = file_roles_api.delete_file_role(file_role_id=file_role_id)
        mock_method.assert_called_once_with("DELETE", f"/file_roles/{file_role_id}")
    assert result == {}

def test_delete_file_role_success_json_response(file_roles_api: FileRolesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a file role with a JSON response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "File role deleted"}
    file_role_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = file_roles_api.delete_file_role(file_role_id=file_role_id)
        mock_method.assert_called_once_with("DELETE", f"/file_roles/{file_role_id}")
    assert result == {"message": "File role deleted"}

def test_list_file_roles_empty(file_roles_api: FileRolesAPI, client: OpenToCloseAPI) -> None:
    """Tests listing file roles when API returns an empty list."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = file_roles_api.list_file_roles()
        mock_method.assert_called_once_with("GET", "/file_roles", params=None)
    assert result == []

def test_list_file_roles_no_data_key(file_roles_api: FileRolesAPI, client: OpenToCloseAPI) -> None:
    """Tests listing file roles when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = file_roles_api.list_file_roles()
        mock_method.assert_called_once_with("GET", "/file_roles", params=None)
    assert result == []

def test_create_file_role_no_data_key(file_roles_api: FileRolesAPI, client: OpenToCloseAPI) -> None:
    """Tests creating file role when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {}
    file_role_data = {"name": "Inspection Report"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = file_roles_api.create_file_role(file_role_data)
        mock_method.assert_called_once_with("POST", "/file_roles", json_data=file_role_data)
    assert result == {}

def test_retrieve_file_role_no_data_key(file_roles_api: FileRolesAPI, client: OpenToCloseAPI) -> None:
    """Tests retrieving file role when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    file_role_id = 3
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = file_roles_api.retrieve_file_role(file_role_id)
        mock_method.assert_called_once_with("GET", f"/file_roles/{file_role_id}")
    assert result == {}

def test_update_file_role_no_data_key(file_roles_api: FileRolesAPI, client: OpenToCloseAPI) -> None:
    """Tests updating file role when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    file_role_id = 3
    update_data = {"name": "Final Inspection Report"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = file_roles_api.update_file_role(file_role_id, update_data)
        mock_method.assert_called_once_with("PUT", f"/file_roles/{file_role_id}", json_data=update_data)
    assert result == {} 