import pytest
from unittest.mock import MagicMock, patch
from open_to_close_api.client import OpenToCloseAPI
from open_to_close_api.teams import TeamsAPI

@pytest.fixture
def client() -> OpenToCloseAPI:
    """Provides an OpenToCloseAPI client instance for testing."""
    return OpenToCloseAPI(api_key="test_api_key")

@pytest.fixture
def teams_api(client: OpenToCloseAPI) -> TeamsAPI:
    """Provides a TeamsAPI instance for testing."""
    return TeamsAPI(client)

def test_list_teams_success(teams_api: TeamsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a list of teams."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1, "name": "Sales Team"}]}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        params = {"is_active": True}
        result = teams_api.list_teams(params=params)
        mock_method.assert_called_once_with("GET", "/teams", params=params)
    assert result == [{"id": 1, "name": "Sales Team"}]

def test_create_team_success(teams_api: TeamsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful creation of a team."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"data": {"id": 2, "name": "Marketing Team"}}
    team_data = {"name": "Marketing Team", "leader_id": 5}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = teams_api.create_team(team_data=team_data)
        mock_method.assert_called_once_with("POST", "/teams", json_data=team_data)
    assert result == {"id": 2, "name": "Marketing Team"}

def test_retrieve_team_success(teams_api: TeamsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a specific team."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "Sales Team"}}
    team_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = teams_api.retrieve_team(team_id=team_id)
        mock_method.assert_called_once_with("GET", f"/teams/{team_id}")
    assert result == {"id": 1, "name": "Sales Team"}

def test_update_team_success(teams_api: TeamsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful update of a team."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "Alpha Sales Team"}}
    team_id = 1
    update_data = {"name": "Alpha Sales Team"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = teams_api.update_team(team_id=team_id, team_data=update_data)
        mock_method.assert_called_once_with("PUT", f"/teams/{team_id}", json_data=update_data)
    assert result == {"id": 1, "name": "Alpha Sales Team"}

def test_delete_team_success_204(teams_api: TeamsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a team with a 204 response."""
    mock_response = MagicMock()
    mock_response.status_code = 204
    team_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = teams_api.delete_team(team_id=team_id)
        mock_method.assert_called_once_with("DELETE", f"/teams/{team_id}")
    assert result == {}

def test_delete_team_success_json_response(teams_api: TeamsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a team with a JSON response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Team deleted"}
    team_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = teams_api.delete_team(team_id=team_id)
        mock_method.assert_called_once_with("DELETE", f"/teams/{team_id}")
    assert result == {"message": "Team deleted"}

def test_list_teams_empty(teams_api: TeamsAPI, client: OpenToCloseAPI) -> None:
    """Tests listing teams when API returns an empty list."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = teams_api.list_teams()
        mock_method.assert_called_once_with("GET", "/teams", params=None)
    assert result == []

def test_list_teams_no_data_key(teams_api: TeamsAPI, client: OpenToCloseAPI) -> None:
    """Tests listing teams when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = teams_api.list_teams()
        mock_method.assert_called_once_with("GET", "/teams", params=None)
    assert result == []

def test_create_team_no_data_key(teams_api: TeamsAPI, client: OpenToCloseAPI) -> None:
    """Tests creating a team when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {}
    team_data = {"name": "Support Team"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = teams_api.create_team(team_data)
        mock_method.assert_called_once_with("POST", "/teams", json_data=team_data)
    assert result == {}

def test_retrieve_team_no_data_key(teams_api: TeamsAPI, client: OpenToCloseAPI) -> None:
    """Tests retrieving a team when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    team_id = 404
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = teams_api.retrieve_team(team_id)
        mock_method.assert_called_once_with("GET", f"/teams/{team_id}")
    assert result == {}

def test_update_team_no_data_key(teams_api: TeamsAPI, client: OpenToCloseAPI) -> None:
    """Tests updating a team when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    team_id = 404
    update_data = {"name": "Beta Support Team"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = teams_api.update_team(team_id, update_data)
        mock_method.assert_called_once_with("PUT", f"/teams/{team_id}", json_data=update_data)
    assert result == {} 