import pytest
from unittest.mock import MagicMock, patch
from open_to_close_api.client import OpenToCloseAPI
from open_to_close_api.agents import AgentsAPI

@pytest.fixture
def client() -> OpenToCloseAPI:
    """Provides an OpenToCloseAPI client instance for testing."""
    return OpenToCloseAPI(api_key="test_api_key")

@pytest.fixture
def agents_api(client: OpenToCloseAPI) -> AgentsAPI:
    """Provides an AgentsAPI instance for testing."""
    return AgentsAPI(client)

def test_list_agents_success(agents_api: AgentsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a list of agents."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1, "name": "Agent 007"}]}
    
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        params = {"status": "active"}
        result = agents_api.list_agents(params=params)
        mock_method.assert_called_once_with("GET", "/agents", params=params)
    assert result == [{"id": 1, "name": "Agent 007"}]

def test_create_agent_success(agents_api: AgentsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful creation of an agent."""
    mock_response = MagicMock()
    mock_response.status_code = 201 
    mock_response.json.return_value = {"data": {"id": 2, "name": "New Agent"}}
    
    agent_data = {"name": "New Agent", "email": "new@agent.com"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = agents_api.create_agent(agent_data=agent_data)
        mock_method.assert_called_once_with("POST", "/agents", json_data=agent_data)
    assert result == {"id": 2, "name": "New Agent"}

def test_retrieve_agent_success(agents_api: AgentsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a specific agent."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "Agent 007"}}
    
    agent_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = agents_api.retrieve_agent(agent_id=agent_id)
        mock_method.assert_called_once_with("GET", f"/agents/{agent_id}")
    assert result == {"id": 1, "name": "Agent 007"}

def test_update_agent_success(agents_api: AgentsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful update of an agent."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "name": "Updated Agent"}}
    
    agent_id = 1
    update_data = {"name": "Updated Agent"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = agents_api.update_agent(agent_id=agent_id, agent_data=update_data)
        mock_method.assert_called_once_with("PUT", f"/agents/{agent_id}", json_data=update_data)
    assert result == {"id": 1, "name": "Updated Agent"}

def test_delete_agent_success_204(agents_api: AgentsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of an agent with a 204 response."""
    mock_response = MagicMock()
    mock_response.status_code = 204
    
    agent_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = agents_api.delete_agent(agent_id=agent_id)
        mock_method.assert_called_once_with("DELETE", f"/agents/{agent_id}")
    assert result == {}

def test_delete_agent_success_json_response(agents_api: AgentsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of an agent with a JSON response."""
    mock_response = MagicMock()
    mock_response.status_code = 200 
    mock_response.json.return_value = {"message": "Agent deleted successfully"}
    
    agent_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = agents_api.delete_agent(agent_id=agent_id)
        mock_method.assert_called_once_with("DELETE", f"/agents/{agent_id}")
    assert result == {"message": "Agent deleted successfully"}

def test_list_agents_empty(agents_api: AgentsAPI, client: OpenToCloseAPI) -> None:
    """Tests listing agents when API returns an empty list within data key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []} 
    
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = agents_api.list_agents()
        mock_method.assert_called_once_with("GET", "/agents", params=None)
    assert result == []

def test_list_agents_no_data_key(agents_api: AgentsAPI, client: OpenToCloseAPI) -> None:
    """Tests listing agents when API response is missing the 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {} 
    
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = agents_api.list_agents()
        mock_method.assert_called_once_with("GET", "/agents", params=None)
    assert result == [] # Expect default empty list

def test_create_agent_no_data_key(agents_api: AgentsAPI, client: OpenToCloseAPI) -> None:
    """Tests creating an agent when API response is missing the 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {} 
    
    agent_data = {"name": "Test Agent"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = agents_api.create_agent(agent_data)
        mock_method.assert_called_once_with("POST", "/agents", json_data=agent_data)
    assert result == {} # Expect default empty dict

def test_retrieve_agent_no_data_key(agents_api: AgentsAPI, client: OpenToCloseAPI) -> None:
    """Tests retrieving an agent when API response is missing the 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {} 
    
    agent_id = 99
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = agents_api.retrieve_agent(agent_id)
        mock_method.assert_called_once_with("GET", f"/agents/{agent_id}")
    assert result == {} # Expect default empty dict

def test_update_agent_no_data_key(agents_api: AgentsAPI, client: OpenToCloseAPI) -> None:
    """Tests updating an agent when API response is missing the 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {} 
    
    agent_id = 99
    update_data = {"name": "Updated Name"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = agents_api.update_agent(agent_id, update_data)
        mock_method.assert_called_once_with("PUT", f"/agents/{agent_id}", json_data=update_data)
    assert result == {} # Expect default empty dict 