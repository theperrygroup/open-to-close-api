import pytest
from unittest.mock import MagicMock, patch
from open_to_close_api.client import OpenToCloseAPI
from open_to_close_api.contact_roles import ContactRolesAPI

@pytest.fixture
def client() -> OpenToCloseAPI:
    """Provides an OpenToCloseAPI client instance for testing."""
    return OpenToCloseAPI(api_key="test_api_key")

@pytest.fixture
def contact_roles_api(client: OpenToCloseAPI) -> ContactRolesAPI:
    """Provides a ContactRolesAPI instance for testing."""
    return ContactRolesAPI(client)

def test_list_contact_roles_success(contact_roles_api: ContactRolesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a list of contact roles."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1, "name": "Buyer"}]}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        params = {"category": "transaction"}
        result = contact_roles_api.list_contact_roles(params=params)
        mock_method.assert_called_once_with("GET", "/contact_roles", params=params)
    assert result == [{"id": 1, "name": "Buyer"}]

def test_create_contact_role_success(contact_roles_api: ContactRolesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful creation of a contact role."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"data": {"id": 2, "name": "Seller"}}
    contact_role_data = {"name": "Seller"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = contact_roles_api.create_contact_role(contact_role_data=contact_role_data)
        mock_method.assert_called_once_with("POST", "/contact_roles", json_data=contact_role_data)
    assert result == {"id": 2, "name": "Seller"}

def test_retrieve_contact_role_success(contact_roles_api: ContactRolesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a specific contact role."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "Buyer"}}
    contact_role_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = contact_roles_api.retrieve_contact_role(contact_role_id=contact_role_id)
        mock_method.assert_called_once_with("GET", f"/contact_roles/{contact_role_id}")
    assert result == {"id": 1, "name": "Buyer"}

def test_update_contact_role_success(contact_roles_api: ContactRolesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful update of a contact role."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "Primary Buyer"}}
    contact_role_id = 1
    update_data = {"name": "Primary Buyer"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = contact_roles_api.update_contact_role(contact_role_id=contact_role_id, contact_role_data=update_data)
        mock_method.assert_called_once_with("PUT", f"/contact_roles/{contact_role_id}", json_data=update_data)
    assert result == {"id": 1, "name": "Primary Buyer"}

def test_delete_contact_role_success_204(contact_roles_api: ContactRolesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a contact role with a 204 response."""
    mock_response = MagicMock()
    mock_response.status_code = 204
    contact_role_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = contact_roles_api.delete_contact_role(contact_role_id=contact_role_id)
        mock_method.assert_called_once_with("DELETE", f"/contact_roles/{contact_role_id}")
    assert result == {}

def test_delete_contact_role_success_json_response(contact_roles_api: ContactRolesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a contact role with a JSON response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Contact role deleted"}
    contact_role_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = contact_roles_api.delete_contact_role(contact_role_id=contact_role_id)
        mock_method.assert_called_once_with("DELETE", f"/contact_roles/{contact_role_id}")
    assert result == {"message": "Contact role deleted"}

def test_list_contact_roles_empty(contact_roles_api: ContactRolesAPI, client: OpenToCloseAPI) -> None:
    """Tests listing contact roles when API returns an empty list."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = contact_roles_api.list_contact_roles()
        mock_method.assert_called_once_with("GET", "/contact_roles", params=None)
    assert result == []

def test_list_contact_roles_no_data_key(contact_roles_api: ContactRolesAPI, client: OpenToCloseAPI) -> None:
    """Tests listing contact roles when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = contact_roles_api.list_contact_roles()
        mock_method.assert_called_once_with("GET", "/contact_roles", params=None)
    assert result == []

def test_create_contact_role_no_data_key(contact_roles_api: ContactRolesAPI, client: OpenToCloseAPI) -> None:
    """Tests creating contact role when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {}
    contact_role_data = {"name": "Lender"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = contact_roles_api.create_contact_role(contact_role_data)
        mock_method.assert_called_once_with("POST", "/contact_roles", json_data=contact_role_data)
    assert result == {}

def test_retrieve_contact_role_no_data_key(contact_roles_api: ContactRolesAPI, client: OpenToCloseAPI) -> None:
    """Tests retrieving contact role when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    contact_role_id = 3
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = contact_roles_api.retrieve_contact_role(contact_role_id)
        mock_method.assert_called_once_with("GET", f"/contact_roles/{contact_role_id}")
    assert result == {}

def test_update_contact_role_no_data_key(contact_roles_api: ContactRolesAPI, client: OpenToCloseAPI) -> None:
    """Tests updating contact role when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    contact_role_id = 3
    update_data = {"name": "Co-Lender"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = contact_roles_api.update_contact_role(contact_role_id, update_data)
        mock_method.assert_called_once_with("PUT", f"/contact_roles/{contact_role_id}", json_data=update_data)
    assert result == {} 