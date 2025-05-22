import pytest
from unittest.mock import MagicMock, patch
from open_to_close_api.client import OpenToCloseAPI
from open_to_close_api.properties import PropertiesAPI

@pytest.fixture
def client() -> OpenToCloseAPI:
    """Provides an OpenToCloseAPI client instance for testing."""
    return OpenToCloseAPI(api_key="test_api_key")

@pytest.fixture
def properties_api(client: OpenToCloseAPI) -> PropertiesAPI:
    """Provides a PropertiesAPI instance for testing."""
    return PropertiesAPI(client)

def test_list_properties_success(properties_api: PropertiesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a list of properties."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1, "address": "123 Main St"}]}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        params = {"status": "active"}
        result = properties_api.list_properties(params=params)
        mock_method.assert_called_once_with("GET", "/properties", params=params)
    assert result == [{"id": 1, "address": "123 Main St"}]

def test_create_property_success(properties_api: PropertiesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful creation of a property."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"data": {"id": 2, "address": "456 Oak Ave"}}
    property_data = {"address": "456 Oak Ave", "city": "Anytown"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = properties_api.create_property(property_data=property_data)
        mock_method.assert_called_once_with("POST", "/properties", json_data=property_data)
    assert result == {"id": 2, "address": "456 Oak Ave"}

def test_retrieve_property_success(properties_api: PropertiesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a specific property."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "address": "123 Main St"}}
    property_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = properties_api.retrieve_property(property_id=property_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}")
    assert result == {"id": 1, "address": "123 Main St"}

def test_update_property_success(properties_api: PropertiesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful update of a property."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "address": "123 Main Street"}}
    property_id = 1
    update_data = {"address": "123 Main Street"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = properties_api.update_property(property_id=property_id, property_data=update_data)
        mock_method.assert_called_once_with("PUT", f"/properties/{property_id}", json_data=update_data)
    assert result == {"id": 1, "address": "123 Main Street"}

def test_delete_property_success_204(properties_api: PropertiesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a property with a 204 response."""
    mock_response = MagicMock()
    mock_response.status_code = 204
    property_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = properties_api.delete_property(property_id=property_id)
        mock_method.assert_called_once_with("DELETE", f"/properties/{property_id}")
    assert result == {}

def test_delete_property_success_json_response(properties_api: PropertiesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a property with a JSON response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Property deleted"}
    property_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = properties_api.delete_property(property_id=property_id)
        mock_method.assert_called_once_with("DELETE", f"/properties/{property_id}")
    assert result == {"message": "Property deleted"}

def test_list_properties_empty(properties_api: PropertiesAPI, client: OpenToCloseAPI) -> None:
    """Tests listing properties when API returns an empty list."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = properties_api.list_properties()
        mock_method.assert_called_once_with("GET", "/properties", params=None)
    assert result == []

def test_list_properties_no_data_key(properties_api: PropertiesAPI, client: OpenToCloseAPI) -> None:
    """Tests listing properties when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = properties_api.list_properties()
        mock_method.assert_called_once_with("GET", "/properties", params=None)
    assert result == []

def test_create_property_no_data_key(properties_api: PropertiesAPI, client: OpenToCloseAPI) -> None:
    """Tests creating a property when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {}
    property_data = {"address": "789 Pine Ln"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = properties_api.create_property(property_data)
        mock_method.assert_called_once_with("POST", "/properties", json_data=property_data)
    assert result == {}

def test_retrieve_property_no_data_key(properties_api: PropertiesAPI, client: OpenToCloseAPI) -> None:
    """Tests retrieving a property when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    property_id = 404
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = properties_api.retrieve_property(property_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}")
    assert result == {}

def test_update_property_no_data_key(properties_api: PropertiesAPI, client: OpenToCloseAPI) -> None:
    """Tests updating a property when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    property_id = 404
    update_data = {"address": "789 Updated Pine Ln"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = properties_api.update_property(property_id, update_data)
        mock_method.assert_called_once_with("PUT", f"/properties/{property_id}", json_data=update_data)
    assert result == {} 