import pytest
from unittest.mock import MagicMock, patch
from open_to_close_api.client import OpenToCloseAPI
from open_to_close_api.property_contacts import PropertyContactsAPI

@pytest.fixture
def client() -> OpenToCloseAPI:
    """Provides an OpenToCloseAPI client instance for testing."""
    return OpenToCloseAPI(api_key="test_api_key")

@pytest.fixture
def property_contacts_api(client: OpenToCloseAPI) -> PropertyContactsAPI:
    """Provides a PropertyContactsAPI instance for testing."""
    return PropertyContactsAPI(client)

def test_list_property_contacts_success(property_contacts_api: PropertyContactsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a list of contacts for a property."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1, "name": "Tenant A"}]}
    property_id = 100
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        params = {"role": "tenant"}
        result = property_contacts_api.list_property_contacts(property_id=property_id, params=params)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/contacts", params=params)
    assert result == [{"id": 1, "name": "Tenant A"}]

def test_create_property_contact_success(property_contacts_api: PropertyContactsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful creation of a property contact."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"data": {"id": 2, "name": "Tenant B"}}
    property_id = 100
    contact_data = {"name": "Tenant B", "email": "tenantb@example.com"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_contacts_api.create_property_contact(property_id=property_id, contact_data=contact_data)
        mock_method.assert_called_once_with("POST", f"/properties/{property_id}/contacts", json_data=contact_data)
    assert result == {"id": 2, "name": "Tenant B"}

def test_retrieve_property_contact_success(property_contacts_api: PropertyContactsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a specific property contact."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "Tenant A"}}
    property_id = 100
    contact_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_contacts_api.retrieve_property_contact(property_id=property_id, contact_id=contact_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/contacts/{contact_id}")
    assert result == {"id": 1, "name": "Tenant A"}

def test_update_property_contact_success(property_contacts_api: PropertyContactsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful update of a property contact."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "Tenant Alpha"}}
    property_id = 100
    contact_id = 1
    update_data = {"name": "Tenant Alpha"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_contacts_api.update_property_contact(property_id=property_id, contact_id=contact_id, contact_data=update_data)
        mock_method.assert_called_once_with("PUT", f"/properties/{property_id}/contacts/{contact_id}", json_data=update_data)
    assert result == {"id": 1, "name": "Tenant Alpha"}

def test_delete_property_contact_success_204(property_contacts_api: PropertyContactsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a property contact with a 204 response."""
    mock_response = MagicMock()
    mock_response.status_code = 204
    property_id = 100
    contact_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_contacts_api.delete_property_contact(property_id=property_id, contact_id=contact_id)
        mock_method.assert_called_once_with("DELETE", f"/properties/{property_id}/contacts/{contact_id}")
    assert result == {}

def test_delete_property_contact_success_json_response(property_contacts_api: PropertyContactsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a property contact with a JSON response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Property contact deleted"}
    property_id = 100
    contact_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_contacts_api.delete_property_contact(property_id=property_id, contact_id=contact_id)
        mock_method.assert_called_once_with("DELETE", f"/properties/{property_id}/contacts/{contact_id}")
    assert result == {"message": "Property contact deleted"}

def test_list_property_contacts_empty(property_contacts_api: PropertyContactsAPI, client: OpenToCloseAPI) -> None:
    """Tests listing property contacts when API returns an empty list."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    property_id = 101
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_contacts_api.list_property_contacts(property_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/contacts", params=None)
    assert result == []

def test_list_property_contacts_no_data_key(property_contacts_api: PropertyContactsAPI, client: OpenToCloseAPI) -> None:
    """Tests listing property contacts when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    property_id = 102
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_contacts_api.list_property_contacts(property_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/contacts", params=None)
    assert result == []

def test_create_property_contact_no_data_key(property_contacts_api: PropertyContactsAPI, client: OpenToCloseAPI) -> None:
    """Tests creating a property contact when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {}
    property_id = 103
    contact_data = {"name": "New Contact"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_contacts_api.create_property_contact(property_id, contact_data)
        mock_method.assert_called_once_with("POST", f"/properties/{property_id}/contacts", json_data=contact_data)
    assert result == {}

def test_retrieve_property_contact_no_data_key(property_contacts_api: PropertyContactsAPI, client: OpenToCloseAPI) -> None:
    """Tests retrieving a property contact when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    property_id = 104
    contact_id = 50
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_contacts_api.retrieve_property_contact(property_id, contact_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/contacts/{contact_id}")
    assert result == {}

def test_update_property_contact_no_data_key(property_contacts_api: PropertyContactsAPI, client: OpenToCloseAPI) -> None:
    """Tests updating a property contact when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    property_id = 105
    contact_id = 51
    update_data = {"name": "Updated Contact Name"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_contacts_api.update_property_contact(property_id, contact_id, update_data)
        mock_method.assert_called_once_with("PUT", f"/properties/{property_id}/contacts/{contact_id}", json_data=update_data)
    assert result == {} 