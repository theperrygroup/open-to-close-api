from typing import Dict, Any, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .client import OpenToCloseAPI

class UsersAPI:
    """Handles API requests for User related endpoints."""

    def __init__(self, client: 'OpenToCloseAPI'):
        """Initializes the UsersAPI with a client instance.

        Args:
            client: The OpenToCloseAPI client instance.
        """
        self._client = client

    def list_users(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Retrieves a list of users.

        Args:
            params: Optional dictionary of query parameters.

        Returns:
            A list of dictionaries, where each dictionary represents a user.
        """
        response = self._client._request("GET", "/users", params=params)
        json_response = response.json()
        if isinstance(json_response, list):
            return json_response
        elif isinstance(json_response, dict):
            return json_response.get("data", [])
        return []

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new user.

        Args:
            user_data: A dictionary containing the user's information.

        Returns:
            A dictionary representing the newly created user.
        """
        response = self._client._request("POST", "/users", json_data=user_data)
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get('id'): return json_response
        return json_response.get("data", {})

    def retrieve_user(self, user_id: int) -> Dict[str, Any]:
        """Retrieves a specific user by their ID.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            A dictionary representing the user.
        """
        response = self._client._request("GET", f"/users/{user_id}")
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get('id'): return json_response
        return json_response.get("data", {})

    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Updates an existing user.

        Args:
            user_id: The ID of the user to update.
            user_data: A dictionary containing the fields to update.

        Returns:
            A dictionary representing the updated user.
        """
        response = self._client._request("PUT", f"/users/{user_id}", json_data=user_data)
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get('id'): return json_response
        return json_response.get("data", {})

    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """Deletes a user by their ID.

        Args:
            user_id: The ID of the user to delete.
        
        Returns:
            A dictionary containing the API response.
        """
        response = self._client._request("DELETE", f"/users/{user_id}")
        if response.status_code == 204:
            return {}
        return response.json() 