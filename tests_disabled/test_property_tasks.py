import pytest
from unittest.mock import MagicMock, patch
from open_to_close_api.client import OpenToCloseAPI
from open_to_close_api.property_tasks import PropertyTasksAPI

@pytest.fixture
def client() -> OpenToCloseAPI:
    """Provides an OpenToCloseAPI client instance for testing."""
    return OpenToCloseAPI(api_key="test_api_key")

@pytest.fixture
def property_tasks_api(client: OpenToCloseAPI) -> PropertyTasksAPI:
    """Provides a PropertyTasksAPI instance for testing."""
    return PropertyTasksAPI(client)

def test_list_property_tasks_success(property_tasks_api: PropertyTasksAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a list of tasks for a property."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1, "title": "Order appraisal"}]}
    property_id = 600
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        params = {"status": "pending"}
        result = property_tasks_api.list_property_tasks(property_id=property_id, params=params)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/tasks", params=params)
    assert result == [{"id": 1, "title": "Order appraisal"}]

def test_create_property_task_success(property_tasks_api: PropertyTasksAPI, client: OpenToCloseAPI) -> None:
    """Tests successful creation of a property task."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"data": {"id": 2, "title": "Schedule inspection"}}
    property_id = 600
    task_data = {"title": "Schedule inspection", "due_date": "2024-12-31"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_tasks_api.create_property_task(property_id=property_id, task_data=task_data)
        mock_method.assert_called_once_with("POST", f"/properties/{property_id}/tasks", json_data=task_data)
    assert result == {"id": 2, "title": "Schedule inspection"}

def test_retrieve_property_task_success(property_tasks_api: PropertyTasksAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a specific property task."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "title": "Order appraisal"}}
    property_id = 600
    task_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_tasks_api.retrieve_property_task(property_id=property_id, task_id=task_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/tasks/{task_id}")
    assert result == {"id": 1, "title": "Order appraisal"}

def test_update_property_task_success(property_tasks_api: PropertyTasksAPI, client: OpenToCloseAPI) -> None:
    """Tests successful update of a property task."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "title": "Order appraisal - URGENT"}}
    property_id = 600
    task_id = 1
    update_data = {"title": "Order appraisal - URGENT"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_tasks_api.update_property_task(property_id=property_id, task_id=task_id, task_data=update_data)
        mock_method.assert_called_once_with("PUT", f"/properties/{property_id}/tasks/{task_id}", json_data=update_data)
    assert result == {"id": 1, "title": "Order appraisal - URGENT"}

def test_delete_property_task_success_204(property_tasks_api: PropertyTasksAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a property task with a 204 response."""
    mock_response = MagicMock()
    mock_response.status_code = 204
    property_id = 600
    task_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_tasks_api.delete_property_task(property_id=property_id, task_id=task_id)
        mock_method.assert_called_once_with("DELETE", f"/properties/{property_id}/tasks/{task_id}")
    assert result == {}

def test_delete_property_task_success_json_response(property_tasks_api: PropertyTasksAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a property task with a JSON response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Task deleted"}
    property_id = 600
    task_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_tasks_api.delete_property_task(property_id=property_id, task_id=task_id)
        mock_method.assert_called_once_with("DELETE", f"/properties/{property_id}/tasks/{task_id}")
    assert result == {"message": "Task deleted"}

def test_list_property_tasks_empty(property_tasks_api: PropertyTasksAPI, client: OpenToCloseAPI) -> None:
    """Tests listing property tasks when API returns an empty list."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    property_id = 601
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_tasks_api.list_property_tasks(property_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/tasks", params=None)
    assert result == []

def test_list_property_tasks_no_data_key(property_tasks_api: PropertyTasksAPI, client: OpenToCloseAPI) -> None:
    """Tests listing property tasks when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    property_id = 602
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_tasks_api.list_property_tasks(property_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/tasks", params=None)
    assert result == []

def test_create_property_task_no_data_key(property_tasks_api: PropertyTasksAPI, client: OpenToCloseAPI) -> None:
    """Tests creating a property task when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {}
    property_id = 603
    task_data = {"title": "Follow up"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_tasks_api.create_property_task(property_id, task_data)
        mock_method.assert_called_once_with("POST", f"/properties/{property_id}/tasks", json_data=task_data)
    assert result == {}

def test_retrieve_property_task_no_data_key(property_tasks_api: PropertyTasksAPI, client: OpenToCloseAPI) -> None:
    """Tests retrieving a property task when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    property_id = 604
    task_id = 50
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_tasks_api.retrieve_property_task(property_id, task_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/tasks/{task_id}")
    assert result == {}

def test_update_property_task_no_data_key(property_tasks_api: PropertyTasksAPI, client: OpenToCloseAPI) -> None:
    """Tests updating a property task when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    property_id = 605
    task_id = 51
    update_data = {"title": "Final follow up"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_tasks_api.update_property_task(property_id, task_id, update_data)
        mock_method.assert_called_once_with("PUT", f"/properties/{property_id}/tasks/{task_id}", json_data=update_data)
    assert result == {} 