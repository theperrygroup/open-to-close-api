import pytest
from unittest.mock import MagicMock, patch
from open_to_close_api.client import OpenToCloseAPI
from open_to_close_api.time_zones import TimeZonesAPI

@pytest.fixture
def client() -> OpenToCloseAPI:
    """Provides an OpenToCloseAPI client instance for testing."""
    return OpenToCloseAPI(api_key="test_api_key")

@pytest.fixture
def time_zones_api(client: OpenToCloseAPI) -> TimeZonesAPI:
    """Provides a TimeZonesAPI instance for testing."""
    return TimeZonesAPI(client)

def test_list_time_zones_success(time_zones_api: TimeZonesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a list of time zones."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1, "name": "Eastern Time (US & Canada)"}]}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        params = {"offset": "-05:00"}
        result = time_zones_api.list_time_zones(params=params)
        mock_method.assert_called_once_with("GET", "/time_zones", params=params)
    assert result == [{"id": 1, "name": "Eastern Time (US & Canada)"}]

def test_create_time_zone_success(time_zones_api: TimeZonesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful creation of a time zone."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"data": {"id": 2, "name": "Pacific Time (US & Canada)"}}
    time_zone_data = {"name": "Pacific Time (US & Canada)", "offset": "-08:00"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = time_zones_api.create_time_zone(time_zone_data=time_zone_data)
        mock_method.assert_called_once_with("POST", "/time_zones", json_data=time_zone_data)
    assert result == {"id": 2, "name": "Pacific Time (US & Canada)"}

def test_retrieve_time_zone_success(time_zones_api: TimeZonesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a specific time zone."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "Eastern Time (US & Canada)"}}
    time_zone_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = time_zones_api.retrieve_time_zone(time_zone_id=time_zone_id)
        mock_method.assert_called_once_with("GET", f"/time_zones/{time_zone_id}")
    assert result == {"id": 1, "name": "Eastern Time (US & Canada)"}

def test_update_time_zone_success(time_zones_api: TimeZonesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful update of a time zone."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "ET"}}
    time_zone_id = 1
    update_data = {"name": "ET"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = time_zones_api.update_time_zone(time_zone_id=time_zone_id, time_zone_data=update_data)
        mock_method.assert_called_once_with("PUT", f"/time_zones/{time_zone_id}", json_data=update_data)
    assert result == {"id": 1, "name": "ET"}

def test_delete_time_zone_success_204(time_zones_api: TimeZonesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a time zone with a 204 response."""
    mock_response = MagicMock()
    mock_response.status_code = 204
    time_zone_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = time_zones_api.delete_time_zone(time_zone_id=time_zone_id)
        mock_method.assert_called_once_with("DELETE", f"/time_zones/{time_zone_id}")
    assert result == {}

def test_delete_time_zone_success_json_response(time_zones_api: TimeZonesAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a time zone with a JSON response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Time zone deleted"}
    time_zone_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = time_zones_api.delete_time_zone(time_zone_id=time_zone_id)
        mock_method.assert_called_once_with("DELETE", f"/time_zones/{time_zone_id}")
    assert result == {"message": "Time zone deleted"}

def test_list_time_zones_empty(time_zones_api: TimeZonesAPI, client: OpenToCloseAPI) -> None:
    """Tests listing time zones when API returns an empty list."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = time_zones_api.list_time_zones()
        mock_method.assert_called_once_with("GET", "/time_zones", params=None)
    assert result == []

def test_list_time_zones_no_data_key(time_zones_api: TimeZonesAPI, client: OpenToCloseAPI) -> None:
    """Tests listing time zones when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = time_zones_api.list_time_zones()
        mock_method.assert_called_once_with("GET", "/time_zones", params=None)
    assert result == []

def test_create_time_zone_no_data_key(time_zones_api: TimeZonesAPI, client: OpenToCloseAPI) -> None:
    """Tests creating a time zone when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {}
    time_zone_data = {"name": "Central Time"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = time_zones_api.create_time_zone(time_zone_data)
        mock_method.assert_called_once_with("POST", "/time_zones", json_data=time_zone_data)
    assert result == {}

def test_retrieve_time_zone_no_data_key(time_zones_api: TimeZonesAPI, client: OpenToCloseAPI) -> None:
    """Tests retrieving a time zone when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    time_zone_id = 404
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = time_zones_api.retrieve_time_zone(time_zone_id)
        mock_method.assert_called_once_with("GET", f"/time_zones/{time_zone_id}")
    assert result == {}

def test_update_time_zone_no_data_key(time_zones_api: TimeZonesAPI, client: OpenToCloseAPI) -> None:
    """Tests updating a time zone when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    time_zone_id = 404
    update_data = {"name": "Mountain Time"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = time_zones_api.update_time_zone(time_zone_id, update_data)
        mock_method.assert_called_once_with("PUT", f"/time_zones/{time_zone_id}", json_data=update_data)
    assert result == {} 