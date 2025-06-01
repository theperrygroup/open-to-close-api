"""Agents client for Open To Close API."""

from typing import Any, Dict, List, Optional

from .base_client import BaseClient


class AgentsAPI(BaseClient):
    """Client for agents API endpoints.

    This client provides methods to manage agents in the Open To Close platform.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the agents client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API
        """
        super().__init__(api_key=api_key, base_url=base_url)

    def list_agents(
        self, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of agents.

        Args:
            params: Optional dictionary of query parameters for filtering

        Returns:
            A list of dictionaries, where each dictionary represents an agent

        Raises:
            OpenToCloseAPIError: If the API request fails
            ValidationError: If parameters are invalid
            AuthenticationError: If authentication fails

        Example:
            ```python
            # Get all agents
            agents = client.agents.list_agents()

            # Get agents with custom parameters
            agents = client.agents.list_agents(params={"limit": 50})
            ```
        """
        response = self.get("/agents", params=params)
        if isinstance(response, list):
            return response
        elif isinstance(response, dict):
            data = response.get("data", [])
            return data if isinstance(data, list) else []
        return []

    def create_agent(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new agent.

        Args:
            agent_data: A dictionary containing the agent's information

        Returns:
            A dictionary representing the newly created agent

        Raises:
            OpenToCloseAPIError: If the API request fails
            ValidationError: If agent data is invalid
            AuthenticationError: If authentication fails

        Example:
            ```python
            agent = client.agents.create_agent({
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "+1234567890"
            })
            ```
        """
        response = self.post("/agents", json_data=agent_data)
        if isinstance(response, dict) and response.get("id"):
            return response
        if isinstance(response, dict):
            data = response.get("data", {})
            return data if isinstance(data, dict) else {}
        return {}

    def retrieve_agent(self, agent_id: int) -> Dict[str, Any]:
        """Retrieve a specific agent by their ID.

        Args:
            agent_id: The ID of the agent to retrieve

        Returns:
            A dictionary representing the agent

        Raises:
            NotFoundError: If the agent is not found
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            agent = client.agents.retrieve_agent(123)
            print(f"Agent name: {agent['name']}")
            ```
        """
        response = self.get(f"/agents/{agent_id}")
        if isinstance(response, dict) and response.get("id"):
            return response
        if isinstance(response, dict):
            data = response.get("data", {})
            return data if isinstance(data, dict) else {}
        return {}

    def update_agent(self, agent_id: int, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing agent.

        Args:
            agent_id: The ID of the agent to update
            agent_data: A dictionary containing the fields to update

        Returns:
            A dictionary representing the updated agent

        Raises:
            NotFoundError: If the agent is not found
            ValidationError: If agent data is invalid
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            updated_agent = client.agents.update_agent(123, {
                "name": "Jane Doe",
                "email": "jane@example.com"
            })
            ```
        """
        response = self.put(f"/agents/{agent_id}", json_data=agent_data)
        if isinstance(response, dict) and response.get("id"):
            return response
        if isinstance(response, dict):
            data = response.get("data", {})
            return data if isinstance(data, dict) else {}
        return {}

    def delete_agent(self, agent_id: int) -> Dict[str, Any]:
        """Delete an agent by their ID.

        Args:
            agent_id: The ID of the agent to delete

        Returns:
            A dictionary containing the API response

        Raises:
            NotFoundError: If the agent is not found
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            result = client.agents.delete_agent(123)
            ```
        """
        return self.delete(f"/agents/{agent_id}")
