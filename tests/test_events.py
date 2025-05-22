import pytest
from unittest.mock import MagicMock, patch
from open_to_close_api.client import OpenToCloseAPI
from open_to_close_api.events import EventsAPI

@pytest.fixture
def client() -> OpenToCloseAPI:
    """Provides an OpenToCloseAPI client instance for testing."""
    return OpenToCloseAPI(api_key="test_api_key")

@pytest.fixture
def events_api(client: OpenToCloseAPI) -> EventsAPI:
    """Provides an EventsAPI instance for testing."""
    return EventsAPI(client)

def test_list_events_success(events_api: EventsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a list of events."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1, "name": "Open House"}]}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        params = {"type": "showing"}
        result = events_api.list_events(params=params)
        mock_method.assert_called_once_with("GET", "/events", params=params)
    assert result == [{"id": 1, "name": "Open House"}]

def test_create_event_success(events_api: EventsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful creation of an event."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"data": {"id": 2, "name": "Closing Day"}}
    event_data = {"name": "Closing Day", "date": "2024-12-31"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = events_api.create_event(event_data=event_data)
        mock_method.assert_called_once_with("POST", "/events", json_data=event_data)
    assert result == {"id": 2, "name": "Closing Day"}

def test_retrieve_event_success(events_api: EventsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a specific event."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "Open House"}}
    event_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = events_api.retrieve_event(event_id=event_id)
        mock_method.assert_called_once_with("GET", f"/events/{event_id}")
    assert result == {"id": 1, "name": "Open House"}

def test_update_event_success(events_api: EventsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful update of an event."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "Weekend Open House"}}
    event_id = 1
    update_data = {"name": "Weekend Open House"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = events_api.update_event(event_id=event_id, event_data=update_data)
        mock_method.assert_called_once_with("PUT", f"/events/{event_id}", json_data=update_data)
    assert result == {"id": 1, "name": "Weekend Open House"}

def test_delete_event_success_204(events_api: EventsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of an event with a 204 response."""
    mock_response = MagicMock()
    mock_response.status_code = 204
    event_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = events_api.delete_event(event_id=event_id)
        mock_method.assert_called_once_with("DELETE", f"/events/{event_id}")
    assert result == {}

def test_delete_event_success_json_response(events_api: EventsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of an event with a JSON response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Event deleted"}
    event_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = events_api.delete_event(event_id=event_id)
        mock_method.assert_called_once_with("DELETE", f"/events/{event_id}")
    assert result == {"message": "Event deleted"}

def test_list_events_empty(events_api: EventsAPI, client: OpenToCloseAPI) -> None:
    """Tests listing events when API returns an empty list."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = events_api.list_events()
        mock_method.assert_called_once_with("GET", "/events", params=None)
    assert result == []

def test_list_events_no_data_key(events_api: EventsAPI, client: OpenToCloseAPI) -> None:
    """Tests listing events when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = events_api.list_events()
        mock_method.assert_called_once_with("GET", "/events", params=None)
    assert result == []

def test_create_event_no_data_key(events_api: EventsAPI, client: OpenToCloseAPI) -> None:
    """Tests creating an event when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {}
    event_data = {"name": "Meeting"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = events_api.create_event(event_data)
        mock_method.assert_called_once_with("POST", "/events", json_data=event_data)
    assert result == {}

def test_retrieve_event_no_data_key(events_api: EventsAPI, client: OpenToCloseAPI) -> None:
    """Tests retrieving an event when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    event_id = 404
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = events_api.retrieve_event(event_id)
        mock_method.assert_called_once_with("GET", f"/events/{event_id}")
    assert result == {}

def test_update_event_no_data_key(events_api: EventsAPI, client: OpenToCloseAPI) -> None:
    """Tests updating an event when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    event_id = 404
    update_data = {"name": "Rescheduled Meeting"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = events_api.update_event(event_id, update_data)
        mock_method.assert_called_once_with("PUT", f"/events/{event_id}", json_data=update_data)
    assert result == {} 