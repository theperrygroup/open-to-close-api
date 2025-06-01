from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:  # pragma: no cover
    from .client import OpenToCloseAPI


class TeamsAPI:
    """Handles API requests for Team related endpoints."""

    def __init__(self, client: "OpenToCloseAPI"):
        """Initializes the TeamsAPI with a client instance.

        Args:
            client: The OpenToCloseAPI client instance.
        """
        self._client = client

    def list_teams(
        self, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieves a list of teams.

        Args:
            params: Optional dictionary of query parameters.

        Returns:
            A list of dictionaries, where each dictionary represents a team.
        """
        response = self._client._request("GET", "/teams", params=params)
        json_response = response.json()
        if isinstance(json_response, list):
            return json_response
        elif isinstance(json_response, dict):
            return json_response.get("data", [])
        return []

    def create_team(self, team_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new team.

        Args:
            team_data: A dictionary containing the team's information.

        Returns:
            A dictionary representing the newly created team.
        """
        response = self._client._request("POST", "/teams", json_data=team_data)
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get("id"):
            return json_response
        return json_response.get("data", {})

    def retrieve_team(self, team_id: int) -> Dict[str, Any]:
        """Retrieves a specific team by its ID.

        Args:
            team_id: The ID of the team to retrieve.

        Returns:
            A dictionary representing the team.
        """
        response = self._client._request("GET", f"/teams/{team_id}")
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get("id"):
            return json_response
        return json_response.get("data", {})

    def update_team(self, team_id: int, team_data: Dict[str, Any]) -> Dict[str, Any]:
        """Updates an existing team.

        Args:
            team_id: The ID of the team to update.
            team_data: A dictionary containing the fields to update.

        Returns:
            A dictionary representing the updated team.
        """
        response = self._client._request(
            "PUT", f"/teams/{team_id}", json_data=team_data
        )
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get("id"):
            return json_response
        return json_response.get("data", {})

    def delete_team(self, team_id: int) -> Dict[str, Any]:
        """Deletes a team by its ID.

        Args:
            team_id: The ID of the team to delete.

        Returns:
            A dictionary containing the API response.
        """
        response = self._client._request("DELETE", f"/teams/{team_id}")
        if response.status_code == 204:
            return {}
        return response.json()
