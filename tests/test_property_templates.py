import pytest
from unittest.mock import MagicMock, patch
from open_to_close_api.client import OpenToCloseAPI
from open_to_close_api.property_templates import PropertyTemplatesAPI

@pytest.fixture
def client() -> OpenToCloseAPI:
    """Provides an OpenToCloseAPI client instance for testing."""
    return OpenToCloseAPI(api_key="test_api_key")

@pytest.fixture
def property_templates_api(client: OpenToCloseAPI) -> PropertyTemplatesAPI:
    """Provides a PropertyTemplatesAPI instance for testing."""
    return PropertyTemplatesAPI(client)

def test_list_property_templates_success(property_templates_api: PropertyTemplatesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a list of property templates."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1, "name": "Residential Purchase"}]}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        params = {"type": "buyer"}
        result = property_templates_api.list_property_templates(params=params)
        mock_method.assert_called_once_with("GET", "/property_templates", params=params)
    assert result == [{"id": 1, "name": "Residential Purchase"}]

def test_create_property_template_success(property_templates_api: PropertyTemplatesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful creation of a property template."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"data": {"id": 2, "name": "Commercial Lease"}}
    template_data = {"name": "Commercial Lease", "category": "lease"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_templates_api.create_property_template(template_data=template_data)
        mock_method.assert_called_once_with("POST", "/property_templates", json_data=template_data)
    assert result == {"id": 2, "name": "Commercial Lease"}

def test_retrieve_property_template_success(property_templates_api: PropertyTemplatesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a specific property template."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "Residential Purchase"}}
    template_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_templates_api.retrieve_property_template(template_id=template_id)
        mock_method.assert_called_once_with("GET", f"/property_templates/{template_id}")
    assert result == {"id": 1, "name": "Residential Purchase"}

def test_update_property_template_success(property_templates_api: PropertyTemplatesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful update of a property template."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "Residential Sale"}}
    template_id = 1
    update_data = {"name": "Residential Sale"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_templates_api.update_property_template(template_id=template_id, template_data=update_data)
        mock_method.assert_called_once_with("PUT", f"/property_templates/{template_id}", json_data=update_data)
    assert result == {"id": 1, "name": "Residential Sale"}

def test_delete_property_template_success_204(property_templates_api: PropertyTemplatesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a property template with a 204 response."""
    mock_response = MagicMock()
    mock_response.status_code = 204
    template_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_templates_api.delete_property_template(template_id=template_id)
        mock_method.assert_called_once_with("DELETE", f"/property_templates/{template_id}")
    assert result == {}

def test_delete_property_template_success_json_response(property_templates_api: PropertyTemplatesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a property template with a JSON response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Template deleted"}
    template_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_templates_api.delete_property_template(template_id=template_id)
        mock_method.assert_called_once_with("DELETE", f"/property_templates/{template_id}")
    assert result == {"message": "Template deleted"}

def test_list_property_templates_empty(property_templates_api: PropertyTemplatesAPI, client: OpenToCloseAPI) -> None:
    """Tests listing property templates when API returns an empty list."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_templates_api.list_property_templates()
        mock_method.assert_called_once_with("GET", "/property_templates", params=None)
    assert result == []

def test_list_property_templates_no_data_key(property_templates_api: PropertyTemplatesAPI, client: OpenToCloseAPI) -> None:
    """Tests listing property templates when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_templates_api.list_property_templates()
        mock_method.assert_called_once_with("GET", "/property_templates", params=None)
    assert result == []

def test_create_property_template_no_data_key(property_templates_api: PropertyTemplatesAPI, client: OpenToCloseAPI) -> None:
    """Tests creating a property template when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {}
    template_data = {"name": "Land Listing"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_templates_api.create_property_template(template_data)
        mock_method.assert_called_once_with("POST", "/property_templates", json_data=template_data)
    assert result == {}

def test_retrieve_property_template_no_data_key(property_templates_api: PropertyTemplatesAPI, client: OpenToCloseAPI) -> None:
    """Tests retrieving a property template when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    template_id = 404
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_templates_api.retrieve_property_template(template_id)
        mock_method.assert_called_once_with("GET", f"/property_templates/{template_id}")
    assert result == {}

def test_update_property_template_no_data_key(property_templates_api: PropertyTemplatesAPI, client: OpenToCloseAPI) -> None:
    """Tests updating a property template when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    template_id = 404
    update_data = {"name": "Updated Land Listing"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_templates_api.update_property_template(template_id, update_data)
        mock_method.assert_called_once_with("PUT", f"/property_templates/{template_id}", json_data=update_data)
    assert result == {} 