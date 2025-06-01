import pytest
from unittest.mock import MagicMock, patch
from open_to_close_api.client import OpenToCloseAPI
from open_to_close_api.contacts import ContactsAPI

@pytest.fixture
def client() -> OpenToCloseAPI:
    """Provides an OpenToCloseAPI client instance for testing."""
    return OpenToCloseAPI(api_key="test_api_key")

@pytest.fixture
def contacts_api(client: OpenToCloseAPI) -> ContactsAPI:
    """Provides a ContactsAPI instance for testing."""
    return ContactsAPI(client)

def test_list_contacts_success(contacts_api: ContactsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a list of contacts."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1, "name": "John Doe"}]}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        params = {"type": "client"}
        result = contacts_api.list_contacts(params=params)
        mock_method.assert_called_once_with("GET", "/contacts", params=params)
    assert result == [{"id": 1, "name": "John Doe"}]

def test_create_contact_success(contacts_api: ContactsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful creation of a contact."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"data": {"id": 2, "name": "Jane Doe"}}
    contact_data = {"name": "Jane Doe", "email": "jane@example.com"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = contacts_api.create_contact(contact_data=contact_data)
        mock_method.assert_called_once_with("POST", "/contacts", json_data=contact_data)
    assert result == {"id": 2, "name": "Jane Doe"}

def test_retrieve_contact_success(contacts_api: ContactsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a specific contact."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "John Doe"}}
    contact_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = contacts_api.retrieve_contact(contact_id=contact_id)
        mock_method.assert_called_once_with("GET", f"/contacts/{contact_id}")
    assert result == {"id": 1, "name": "John Doe"}

def test_update_contact_success(contacts_api: ContactsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful update of a contact."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "Johnathan Doe"}}
    contact_id = 1
    update_data = {"name": "Johnathan Doe"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = contacts_api.update_contact(contact_id=contact_id, contact_data=update_data)
        mock_method.assert_called_once_with("PUT", f"/contacts/{contact_id}", json_data=update_data)
    assert result == {"id": 1, "name": "Johnathan Doe"}

def test_delete_contact_success_204(contacts_api: ContactsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a contact with a 204 response."""
    mock_response = MagicMock()
    mock_response.status_code = 204
    contact_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = contacts_api.delete_contact(contact_id=contact_id)
        mock_method.assert_called_once_with("DELETE", f"/contacts/{contact_id}")
    assert result == {}

def test_delete_contact_success_json_response(contacts_api: ContactsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a contact with a JSON response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Contact deleted"}
    contact_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = contacts_api.delete_contact(contact_id=contact_id)
        mock_method.assert_called_once_with("DELETE", f"/contacts/{contact_id}")
    assert result == {"message": "Contact deleted"}

def test_list_contacts_empty(contacts_api: ContactsAPI, client: OpenToCloseAPI) -> None:
    """Tests listing contacts when API returns an empty list."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = contacts_api.list_contacts()
        mock_method.assert_called_once_with("GET", "/contacts", params=None)
    assert result == []

def test_list_contacts_no_data_key(contacts_api: ContactsAPI, client: OpenToCloseAPI) -> None:
    """Tests listing contacts when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = contacts_api.list_contacts()
        mock_method.assert_called_once_with("GET", "/contacts", params=None)
    assert result == []

def test_create_contact_no_data_key(contacts_api: ContactsAPI, client: OpenToCloseAPI) -> None:
    """Tests creating contact when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {}
    contact_data = {"name": "Test"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = contacts_api.create_contact(contact_data)
        mock_method.assert_called_once_with("POST", "/contacts", json_data=contact_data)
    assert result == {}

def test_retrieve_contact_no_data_key(contacts_api: ContactsAPI, client: OpenToCloseAPI) -> None:
    """Tests retrieving contact when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    contact_id = 5
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = contacts_api.retrieve_contact(contact_id)
        mock_method.assert_called_once_with("GET", f"/contacts/{contact_id}")
    assert result == {}

def test_update_contact_no_data_key(contacts_api: ContactsAPI, client: OpenToCloseAPI) -> None:
    """Tests updating contact when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    contact_id = 5
    update_data = {"name": "Updated"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = contacts_api.update_contact(contact_id, update_data)
        mock_method.assert_called_once_with("PUT", f"/contacts/{contact_id}", json_data=update_data)
    assert result == {} 