from typing import Dict, Any, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .client import OpenToCloseAPI # Import for type hinting only

class AgentsAPI:
    """Handles API requests for Agent related endpoints."""

    def __init__(self, client: 'OpenToCloseAPI'): # Use string literal for type hint
        """Initializes the AgentsAPI with a client instance.

        Args:
            client: The OpenToCloseAPI client instance.
        """
        self._client = client

    def list_agents(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Retrieves a list of agents.

        Args:
            params: Optional dictionary of query parameters.

        Returns:
            A list of dictionaries, where each dictionary represents an agent.
        """
        response = self._client._request("GET", "/agents", params=params)
        json_response = response.json()
        if isinstance(json_response, list):
            return json_response
        elif isinstance(json_response, dict):
            return json_response.get("data", []) # Standard case for object with a data key
        return [] # Should not happen if API is consistent, but a safe default

    def create_agent(self, user_data_for_agent: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new Agent (likely as a specific type of User).
        Assumes the API uses a general user creation endpoint with a type identifier for agents.
        The exact payload (e.g. user_type_id, role_id) needs to be confirmed from API docs.

        Args:
            user_data_for_agent: A dictionary containing the user/agent's information.

        Returns:
            A dictionary representing the newly created user/agent.
        """
        # Path changed from /agents to /users based on typical API design for typed users
        response = self._client._request("POST", "/users", json_data=user_data_for_agent)
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get('id'): 
            return json_response
        return json_response.get("data", {}) # Fallback

    def retrieve_agent(self, agent_id: int) -> Dict[str, Any]:
        """Retrieves a specific agent by its ID.

        Args:
            agent_id: The ID of the agent to retrieve.

        Returns:
            A dictionary representing the agent.
        """
        response = self._client._request("GET", f"/agents/{agent_id}")
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get('id'): return json_response
        return json_response.get("data", {})

    def update_agent(self, agent_id: int, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Updates an existing agent.

        Args:
            agent_id: The ID of the agent to update.
            agent_data: A dictionary containing the fields to update.

        Returns:
            A dictionary representing the updated agent.
        """
        response = self._client._request("PUT", f"/agents/{agent_id}", json_data=agent_data)
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get('id'): return json_response
        return json_response.get("data", {})

    def delete_agent(self, agent_id: int) -> Dict[str, Any]:
        """Deletes an agent by its ID.

        Args:
            agent_id: The ID of the agent to delete.
        
        Returns:
            A dictionary containing the API response (often empty or a success message for deletes).
        """
        # Delete typically returns 204 No Content, or sometimes a confirmation
        response = self._client._request("DELETE", f"/agents/{agent_id}")
        # If 204, response.json() will fail. Check status code.
        if response.status_code == 204:
            return {}
        return response.json() # Or handle based on actual API behavior 