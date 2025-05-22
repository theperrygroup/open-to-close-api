import pytest
from unittest.mock import MagicMock, patch
from open_to_close_api.client import OpenToCloseAPI
from open_to_close_api.tags import TagsAPI

@pytest.fixture
def client() -> OpenToCloseAPI:
    """Provides an OpenToCloseAPI client instance for testing."""
    return OpenToCloseAPI(api_key="test_api_key")

@pytest.fixture
def tags_api(client: OpenToCloseAPI) -> TagsAPI:
    """Provides a TagsAPI instance for testing."""
    return TagsAPI(client)

def test_list_tags_success(tags_api: TagsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a list of tags."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1, "name": "Hot Lead"}]}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        params = {"category": "lead_status"}
        result = tags_api.list_tags(params=params)
        mock_method.assert_called_once_with("GET", "/tags", params=params)
    assert result == [{"id": 1, "name": "Hot Lead"}]

def test_create_tag_success(tags_api: TagsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful creation of a tag."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"data": {"id": 2, "name": "Past Client"}}
    tag_data = {"name": "Past Client", "color": "#FF0000"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = tags_api.create_tag(tag_data=tag_data)
        mock_method.assert_called_once_with("POST", "/tags", json_data=tag_data)
    assert result == {"id": 2, "name": "Past Client"}

def test_retrieve_tag_success(tags_api: TagsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a specific tag."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "Hot Lead"}}
    tag_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = tags_api.retrieve_tag(tag_id=tag_id)
        mock_method.assert_called_once_with("GET", f"/tags/{tag_id}")
    assert result == {"id": 1, "name": "Hot Lead"}

def test_update_tag_success(tags_api: TagsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful update of a tag."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "Very Hot Lead"}}
    tag_id = 1
    update_data = {"name": "Very Hot Lead"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = tags_api.update_tag(tag_id=tag_id, tag_data=update_data)
        mock_method.assert_called_once_with("PUT", f"/tags/{tag_id}", json_data=update_data)
    assert result == {"id": 1, "name": "Very Hot Lead"}

def test_delete_tag_success_204(tags_api: TagsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a tag with a 204 response."""
    mock_response = MagicMock()
    mock_response.status_code = 204
    tag_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = tags_api.delete_tag(tag_id=tag_id)
        mock_method.assert_called_once_with("DELETE", f"/tags/{tag_id}")
    assert result == {}

def test_delete_tag_success_json_response(tags_api: TagsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a tag with a JSON response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Tag deleted"}
    tag_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = tags_api.delete_tag(tag_id=tag_id)
        mock_method.assert_called_once_with("DELETE", f"/tags/{tag_id}")
    assert result == {"message": "Tag deleted"}

def test_list_tags_empty(tags_api: TagsAPI, client: OpenToCloseAPI) -> None:
    """Tests listing tags when API returns an empty list."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = tags_api.list_tags()
        mock_method.assert_called_once_with("GET", "/tags", params=None)
    assert result == []

def test_list_tags_no_data_key(tags_api: TagsAPI, client: OpenToCloseAPI) -> None:
    """Tests listing tags when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = tags_api.list_tags()
        mock_method.assert_called_once_with("GET", "/tags", params=None)
    assert result == []

def test_create_tag_no_data_key(tags_api: TagsAPI, client: OpenToCloseAPI) -> None:
    """Tests creating a tag when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {}
    tag_data = {"name": "Sphere"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = tags_api.create_tag(tag_data)
        mock_method.assert_called_once_with("POST", "/tags", json_data=tag_data)
    assert result == {}

def test_retrieve_tag_no_data_key(tags_api: TagsAPI, client: OpenToCloseAPI) -> None:
    """Tests retrieving a tag when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    tag_id = 404
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = tags_api.retrieve_tag(tag_id)
        mock_method.assert_called_once_with("GET", f"/tags/{tag_id}")
    assert result == {}

def test_update_tag_no_data_key(tags_api: TagsAPI, client: OpenToCloseAPI) -> None:
    """Tests updating a tag when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    tag_id = 404
    update_data = {"name": "Important Sphere"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = tags_api.update_tag(tag_id, update_data)
        mock_method.assert_called_once_with("PUT", f"/tags/{tag_id}", json_data=update_data)
    assert result == {} 