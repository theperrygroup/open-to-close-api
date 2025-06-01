"""Teams client for Open To Close API."""

from typing import Any, Dict, List, Optional

from .base_client import BaseClient


class TeamsAPI(BaseClient):
    """Client for teams API endpoints.

    This client provides methods to manage teams in the Open To Close platform.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the teams client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API
        """
        super().__init__(api_key=api_key, base_url=base_url)

    def list_teams(
        self, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of teams.

        Args:
            params: Optional dictionary of query parameters for filtering

        Returns:
            A list of dictionaries, where each dictionary represents a team

        Raises:
            OpenToCloseAPIError: If the API request fails
            ValidationError: If parameters are invalid
            AuthenticationError: If authentication fails

        Example:
            ```python
            # Get all teams
            teams = client.teams.list_teams()

            # Get teams with custom parameters
            teams = client.teams.list_teams(params={"limit": 50})
            ```
        """
        response = self.get("/teams", params=params)
        return self._process_list_response(response)

    def create_team(self, team_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new team.

        Args:
            team_data: A dictionary containing the team's information

        Returns:
            A dictionary representing the newly created team

        Raises:
            OpenToCloseAPIError: If the API request fails
            ValidationError: If team data is invalid
            AuthenticationError: If authentication fails

        Example:
            ```python
            team = client.teams.create_team({
                "name": "Sales Team",
                "description": "Primary sales team"
            })
            ```
        """
        response = self.post("/teams", json_data=team_data)
        return self._process_response_data(response)

    def retrieve_team(self, team_id: int) -> Dict[str, Any]:
        """Retrieve a specific team by its ID.

        Args:
            team_id: The ID of the team to retrieve

        Returns:
            A dictionary representing the team

        Raises:
            NotFoundError: If the team is not found
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            team = client.teams.retrieve_team(123)
            print(f"Team name: {team['name']}")
            ```
        """
        response = self.get(f"/teams/{team_id}")
        return self._process_response_data(response)

    def update_team(self, team_id: int, team_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing team.

        Args:
            team_id: The ID of the team to update
            team_data: A dictionary containing the fields to update

        Returns:
            A dictionary representing the updated team

        Raises:
            NotFoundError: If the team is not found
            ValidationError: If team data is invalid
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            updated_team = client.teams.update_team(123, {
                "name": "Updated Sales Team",
                "description": "Updated description"
            })
            ```
        """
        response = self.put(f"/teams/{team_id}", json_data=team_data)
        return self._process_response_data(response)

    def delete_team(self, team_id: int) -> Dict[str, Any]:
        """Delete a team by its ID.

        Args:
            team_id: The ID of the team to delete

        Returns:
            A dictionary containing the API response

        Raises:
            NotFoundError: If the team is not found
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            result = client.teams.delete_team(123)
            ```
        """
        return self.delete(f"/teams/{team_id}")
