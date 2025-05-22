import pytest
from unittest.mock import MagicMock, patch
from open_to_close_api.client import OpenToCloseAPI
from open_to_close_api.property_fields import PropertyFieldsAPI

@pytest.fixture
def client() -> OpenToCloseAPI:
    """Provides an OpenToCloseAPI client instance for testing."""
    return OpenToCloseAPI(api_key="test_api_key")

@pytest.fixture
def property_fields_api(client: OpenToCloseAPI) -> PropertyFieldsAPI:
    """Provides a PropertyFieldsAPI instance for testing."""
    return PropertyFieldsAPI(client)

def test_list_property_fields_success(property_fields_api: PropertyFieldsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a list of fields for a property."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1, "label": "Lockbox Code"}]}
    property_id = 400
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        params = {"group": "access"}
        result = property_fields_api.list_property_fields(property_id=property_id, params=params)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/fields", params=params)
    assert result == [{"id": 1, "label": "Lockbox Code"}]

def test_create_property_field_success(property_fields_api: PropertyFieldsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful creation of a property field."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"data": {"id": 2, "label": "Alarm Code"}}
    property_id = 400
    field_data = {"label": "Alarm Code", "value": "1234"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_fields_api.create_property_field(property_id=property_id, field_data=field_data)
        mock_method.assert_called_once_with("POST", f"/properties/{property_id}/fields", json_data=field_data)
    assert result == {"id": 2, "label": "Alarm Code"}

def test_retrieve_property_field_success(property_fields_api: PropertyFieldsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a specific property field."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "label": "Lockbox Code"}}
    property_id = 400
    field_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_fields_api.retrieve_property_field(property_id=property_id, field_id=field_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/fields/{field_id}")
    assert result == {"id": 1, "label": "Lockbox Code"}

def test_update_property_field_success(property_fields_api: PropertyFieldsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful update of a property field."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "label": "Gate Code"}}
    property_id = 400
    field_id = 1
    update_data = {"label": "Gate Code"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_fields_api.update_property_field(property_id=property_id, field_id=field_id, field_data=update_data)
        mock_method.assert_called_once_with("PUT", f"/properties/{property_id}/fields/{field_id}", json_data=update_data)
    assert result == {"id": 1, "label": "Gate Code"}

def test_delete_property_field_success_204(property_fields_api: PropertyFieldsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a property field with a 204 response."""
    mock_response = MagicMock()
    mock_response.status_code = 204
    property_id = 400
    field_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_fields_api.delete_property_field(property_id=property_id, field_id=field_id)
        mock_method.assert_called_once_with("DELETE", f"/properties/{property_id}/fields/{field_id}")
    assert result == {}

def test_delete_property_field_success_json_response(property_fields_api: PropertyFieldsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a property field with a JSON response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Property field deleted"}
    property_id = 400
    field_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_fields_api.delete_property_field(property_id=property_id, field_id=field_id)
        mock_method.assert_called_once_with("DELETE", f"/properties/{property_id}/fields/{field_id}")
    assert result == {"message": "Property field deleted"}

def test_list_property_fields_empty(property_fields_api: PropertyFieldsAPI, client: OpenToCloseAPI) -> None:
    """Tests listing property fields when API returns an empty list."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    property_id = 401
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_fields_api.list_property_fields(property_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/fields", params=None)
    assert result == []

def test_list_property_fields_no_data_key(property_fields_api: PropertyFieldsAPI, client: OpenToCloseAPI) -> None:
    """Tests listing property fields when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    property_id = 402
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_fields_api.list_property_fields(property_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/fields", params=None)
    assert result == []

def test_create_property_field_no_data_key(property_fields_api: PropertyFieldsAPI, client: OpenToCloseAPI) -> None:
    """Tests creating a property field when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {}
    property_id = 403
    field_data = {"label": "Notes"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_fields_api.create_property_field(property_id, field_data)
        mock_method.assert_called_once_with("POST", f"/properties/{property_id}/fields", json_data=field_data)
    assert result == {}

def test_retrieve_property_field_no_data_key(property_fields_api: PropertyFieldsAPI, client: OpenToCloseAPI) -> None:
    """Tests retrieving a property field when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    property_id = 404
    field_id = 50
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_fields_api.retrieve_property_field(property_id, field_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/fields/{field_id}")
    assert result == {}

def test_update_property_field_no_data_key(property_fields_api: PropertyFieldsAPI, client: OpenToCloseAPI) -> None:
    """Tests updating a property field when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    property_id = 405
    field_id = 51
    update_data = {"label": "Special Notes"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_fields_api.update_property_field(property_id, field_id, update_data)
        mock_method.assert_called_once_with("PUT", f"/properties/{property_id}/fields/{field_id}", json_data=update_data)
    assert result == {} 