import pytest
from unittest.mock import MagicMock, patch
from open_to_close_api.client import OpenToCloseAPI
from open_to_close_api.property_field_sections import PropertyFieldSectionsAPI

@pytest.fixture
def client() -> OpenToCloseAPI:
    """Provides an OpenToCloseAPI client instance for testing."""
    return OpenToCloseAPI(api_key="test_api_key")

@pytest.fixture
def property_field_sections_api(client: OpenToCloseAPI) -> PropertyFieldSectionsAPI:
    """Provides a PropertyFieldSectionsAPI instance for testing."""
    return PropertyFieldSectionsAPI(client)

def test_list_property_field_sections_success(property_field_sections_api: PropertyFieldSectionsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a list of property field sections."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1, "name": "General Info"}]}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        params = {"template_id": 5}
        result = property_field_sections_api.list_property_field_sections(params=params)
        mock_method.assert_called_once_with("GET", "/property_field_sections", params=params)
    assert result == [{"id": 1, "name": "General Info"}]

def test_create_property_field_section_success(property_field_sections_api: PropertyFieldSectionsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful creation of a property field section."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"data": {"id": 2, "name": "Financial Details"}}
    section_data = {"name": "Financial Details", "order": 1}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_field_sections_api.create_property_field_section(section_data=section_data)
        mock_method.assert_called_once_with("POST", "/property_field_sections", json_data=section_data)
    assert result == {"id": 2, "name": "Financial Details"}

def test_retrieve_property_field_section_success(property_field_sections_api: PropertyFieldSectionsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a specific property field section."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "General Info"}}
    section_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_field_sections_api.retrieve_property_field_section(section_id=section_id)
        mock_method.assert_called_once_with("GET", f"/property_field_sections/{section_id}")
    assert result == {"id": 1, "name": "General Info"}

def test_update_property_field_section_success(property_field_sections_api: PropertyFieldSectionsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful update of a property field section."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "Key Information"}}
    section_id = 1
    update_data = {"name": "Key Information"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_field_sections_api.update_property_field_section(section_id=section_id, section_data=update_data)
        mock_method.assert_called_once_with("PUT", f"/property_field_sections/{section_id}", json_data=update_data)
    assert result == {"id": 1, "name": "Key Information"}

def test_delete_property_field_section_success_204(property_field_sections_api: PropertyFieldSectionsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a property field section with a 204 response."""
    mock_response = MagicMock()
    mock_response.status_code = 204
    section_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_field_sections_api.delete_property_field_section(section_id=section_id)
        mock_method.assert_called_once_with("DELETE", f"/property_field_sections/{section_id}")
    assert result == {}

def test_delete_property_field_section_success_json_response(property_field_sections_api: PropertyFieldSectionsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a property field section with a JSON response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Section deleted"}
    section_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_field_sections_api.delete_property_field_section(section_id=section_id)
        mock_method.assert_called_once_with("DELETE", f"/property_field_sections/{section_id}")
    assert result == {"message": "Section deleted"}

def test_list_property_field_sections_empty(property_field_sections_api: PropertyFieldSectionsAPI, client: OpenToCloseAPI) -> None:
    """Tests listing property field sections when API returns an empty list."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_field_sections_api.list_property_field_sections()
        mock_method.assert_called_once_with("GET", "/property_field_sections", params=None)
    assert result == []

def test_list_property_field_sections_no_data_key(property_field_sections_api: PropertyFieldSectionsAPI, client: OpenToCloseAPI) -> None:
    """Tests listing property field sections when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_field_sections_api.list_property_field_sections()
        mock_method.assert_called_once_with("GET", "/property_field_sections", params=None)
    assert result == []

def test_create_property_field_section_no_data_key(property_field_sections_api: PropertyFieldSectionsAPI, client: OpenToCloseAPI) -> None:
    """Tests creating a property field section when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {}
    section_data = {"name": "Contacts"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_field_sections_api.create_property_field_section(section_data)
        mock_method.assert_called_once_with("POST", "/property_field_sections", json_data=section_data)
    assert result == {}

def test_retrieve_property_field_section_no_data_key(property_field_sections_api: PropertyFieldSectionsAPI, client: OpenToCloseAPI) -> None:
    """Tests retrieving a property field section when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    section_id = 404
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_field_sections_api.retrieve_property_field_section(section_id)
        mock_method.assert_called_once_with("GET", f"/property_field_sections/{section_id}")
    assert result == {}

def test_update_property_field_section_no_data_key(property_field_sections_api: PropertyFieldSectionsAPI, client: OpenToCloseAPI) -> None:
    """Tests updating a property field section when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    section_id = 404
    update_data = {"name": "Important Contacts"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_field_sections_api.update_property_field_section(section_id, update_data)
        mock_method.assert_called_once_with("PUT", f"/property_field_sections/{section_id}", json_data=update_data)
    assert result == {} 