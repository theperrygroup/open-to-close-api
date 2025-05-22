import pytest
from unittest.mock import MagicMock, patch
from open_to_close_api.client import OpenToCloseAPI
from open_to_close_api.property_notes import PropertyNotesAPI

@pytest.fixture
def client() -> OpenToCloseAPI:
    """Provides an OpenToCloseAPI client instance for testing."""
    return OpenToCloseAPI(api_key="test_api_key")

@pytest.fixture
def property_notes_api(client: OpenToCloseAPI) -> PropertyNotesAPI:
    """Provides a PropertyNotesAPI instance for testing."""
    return PropertyNotesAPI(client)

def test_list_property_notes_success(property_notes_api: PropertyNotesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a list of notes for a property."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1, "content": "Call plumber."}]}
    property_id = 500
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        params = {"visibility": "private"}
        result = property_notes_api.list_property_notes(property_id=property_id, params=params)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/notes", params=params)
    assert result == [{"id": 1, "content": "Call plumber."}]

def test_create_property_note_success(property_notes_api: PropertyNotesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful creation of a property note."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"data": {"id": 2, "content": "Schedule showing."}}
    property_id = 500
    note_data = {"content": "Schedule showing.", "is_important": True}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_notes_api.create_property_note(property_id=property_id, note_data=note_data)
        mock_method.assert_called_once_with("POST", f"/properties/{property_id}/notes", json_data=note_data)
    assert result == {"id": 2, "content": "Schedule showing."}

def test_retrieve_property_note_success(property_notes_api: PropertyNotesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a specific property note."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "content": "Call plumber."}}
    property_id = 500
    note_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_notes_api.retrieve_property_note(property_id=property_id, note_id=note_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/notes/{note_id}")
    assert result == {"id": 1, "content": "Call plumber."}

def test_update_property_note_success(property_notes_api: PropertyNotesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful update of a property note."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "content": "Plumber called - appointment set."}}
    property_id = 500
    note_id = 1
    update_data = {"content": "Plumber called - appointment set."}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_notes_api.update_property_note(property_id=property_id, note_id=note_id, note_data=update_data)
        mock_method.assert_called_once_with("PUT", f"/properties/{property_id}/notes/{note_id}", json_data=update_data)
    assert result == {"id": 1, "content": "Plumber called - appointment set."}

def test_delete_property_note_success_204(property_notes_api: PropertyNotesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a property note with a 204 response."""
    mock_response = MagicMock()
    mock_response.status_code = 204
    property_id = 500
    note_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_notes_api.delete_property_note(property_id=property_id, note_id=note_id)
        mock_method.assert_called_once_with("DELETE", f"/properties/{property_id}/notes/{note_id}")
    assert result == {}

def test_delete_property_note_success_json_response(property_notes_api: PropertyNotesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a property note with a JSON response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Note deleted"}
    property_id = 500
    note_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_notes_api.delete_property_note(property_id=property_id, note_id=note_id)
        mock_method.assert_called_once_with("DELETE", f"/properties/{property_id}/notes/{note_id}")
    assert result == {"message": "Note deleted"}

def test_list_property_notes_empty(property_notes_api: PropertyNotesAPI, client: OpenToCloseAPI) -> None:
    """Tests listing property notes when API returns an empty list."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    property_id = 501
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_notes_api.list_property_notes(property_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/notes", params=None)
    assert result == []

def test_list_property_notes_no_data_key(property_notes_api: PropertyNotesAPI, client: OpenToCloseAPI) -> None:
    """Tests listing property notes when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    property_id = 502
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_notes_api.list_property_notes(property_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/notes", params=None)
    assert result == []

def test_create_property_note_no_data_key(property_notes_api: PropertyNotesAPI, client: OpenToCloseAPI) -> None:
    """Tests creating a property note when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {}
    property_id = 503
    note_data = {"content": "Reminder."}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_notes_api.create_property_note(property_id, note_data)
        mock_method.assert_called_once_with("POST", f"/properties/{property_id}/notes", json_data=note_data)
    assert result == {}

def test_retrieve_property_note_no_data_key(property_notes_api: PropertyNotesAPI, client: OpenToCloseAPI) -> None:
    """Tests retrieving a property note when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    property_id = 504
    note_id = 50
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_notes_api.retrieve_property_note(property_id, note_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/notes/{note_id}")
    assert result == {}

def test_update_property_note_no_data_key(property_notes_api: PropertyNotesAPI, client: OpenToCloseAPI) -> None:
    """Tests updating a property note when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    property_id = 505
    note_id = 51
    update_data = {"content": "Updated reminder."}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_notes_api.update_property_note(property_id, note_id, update_data)
        mock_method.assert_called_once_with("PUT", f"/properties/{property_id}/notes/{note_id}", json_data=update_data)
    assert result == {} 