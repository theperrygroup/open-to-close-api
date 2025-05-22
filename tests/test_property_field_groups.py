import pytest
from unittest.mock import MagicMock, patch
from open_to_close_api.client import OpenToCloseAPI
from open_to_close_api.property_field_groups import PropertyFieldGroupsAPI

@pytest.fixture
def client() -> OpenToCloseAPI:
    """Provides an OpenToCloseAPI client instance for testing."""
    return OpenToCloseAPI(api_key="test_api_key")

@pytest.fixture
def property_field_groups_api(client: OpenToCloseAPI) -> PropertyFieldGroupsAPI:
    """Provides a PropertyFieldGroupsAPI instance for testing."""
    return PropertyFieldGroupsAPI(client)

def test_list_property_field_groups_success(property_field_groups_api: PropertyFieldGroupsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a list of property field groups."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1, "name": "Closing Costs"}]}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        params = {"type": "financial"}
        result = property_field_groups_api.list_property_field_groups(params=params)
        mock_method.assert_called_once_with("GET", "/property_field_groups", params=params)
    assert result == [{"id": 1, "name": "Closing Costs"}]

def test_create_property_field_group_success(property_field_groups_api: PropertyFieldGroupsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful creation of a property field group."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"data": {"id": 2, "name": "Inspection Details"}}
    group_data = {"name": "Inspection Details", "order": 2}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_field_groups_api.create_property_field_group(group_data=group_data)
        mock_method.assert_called_once_with("POST", "/property_field_groups", json_data=group_data)
    assert result == {"id": 2, "name": "Inspection Details"}

def test_retrieve_property_field_group_success(property_field_groups_api: PropertyFieldGroupsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a specific property field group."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "Closing Costs"}}
    group_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_field_groups_api.retrieve_property_field_group(group_id=group_id)
        mock_method.assert_called_once_with("GET", f"/property_field_groups/{group_id}")
    assert result == {"id": 1, "name": "Closing Costs"}

def test_update_property_field_group_success(property_field_groups_api: PropertyFieldGroupsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful update of a property field group."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "Final Closing Costs"}}
    group_id = 1
    update_data = {"name": "Final Closing Costs"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_field_groups_api.update_property_field_group(group_id=group_id, group_data=update_data)
        mock_method.assert_called_once_with("PUT", f"/property_field_groups/{group_id}", json_data=update_data)
    assert result == {"id": 1, "name": "Final Closing Costs"}

def test_delete_property_field_group_success_204(property_field_groups_api: PropertyFieldGroupsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a property field group with a 204 response."""
    mock_response = MagicMock()
    mock_response.status_code = 204
    group_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_field_groups_api.delete_property_field_group(group_id=group_id)
        mock_method.assert_called_once_with("DELETE", f"/property_field_groups/{group_id}")
    assert result == {}

def test_delete_property_field_group_success_json_response(property_field_groups_api: PropertyFieldGroupsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a property field group with a JSON response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Group deleted"}
    group_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_field_groups_api.delete_property_field_group(group_id=group_id)
        mock_method.assert_called_once_with("DELETE", f"/property_field_groups/{group_id}")
    assert result == {"message": "Group deleted"}

def test_list_property_field_groups_empty(property_field_groups_api: PropertyFieldGroupsAPI, client: OpenToCloseAPI) -> None:
    """Tests listing property field groups when API returns an empty list."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_field_groups_api.list_property_field_groups()
        mock_method.assert_called_once_with("GET", "/property_field_groups", params=None)
    assert result == []

def test_list_property_field_groups_no_data_key(property_field_groups_api: PropertyFieldGroupsAPI, client: OpenToCloseAPI) -> None:
    """Tests listing property field groups when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_field_groups_api.list_property_field_groups()
        mock_method.assert_called_once_with("GET", "/property_field_groups", params=None)
    assert result == []

def test_create_property_field_group_no_data_key(property_field_groups_api: PropertyFieldGroupsAPI, client: OpenToCloseAPI) -> None:
    """Tests creating a property field group when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {}
    group_data = {"name": "Utilities"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_field_groups_api.create_property_field_group(group_data)
        mock_method.assert_called_once_with("POST", "/property_field_groups", json_data=group_data)
    assert result == {}

def test_retrieve_property_field_group_no_data_key(property_field_groups_api: PropertyFieldGroupsAPI, client: OpenToCloseAPI) -> None:
    """Tests retrieving a property field group when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    group_id = 404
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_field_groups_api.retrieve_property_field_group(group_id)
        mock_method.assert_called_once_with("GET", f"/property_field_groups/{group_id}")
    assert result == {}

def test_update_property_field_group_no_data_key(property_field_groups_api: PropertyFieldGroupsAPI, client: OpenToCloseAPI) -> None:
    """Tests updating a property field group when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    group_id = 404
    update_data = {"name": "Monthly Utilities"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_field_groups_api.update_property_field_group(group_id, update_data)
        mock_method.assert_called_once_with("PUT", f"/property_field_groups/{group_id}", json_data=update_data)
    assert result == {} 