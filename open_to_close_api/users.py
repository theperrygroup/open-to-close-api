"""Users client for Open To Close API."""

from typing import Any, Dict, List, Optional

from .base_client import BaseClient


class UsersAPI(BaseClient):
    """Client for users API endpoints.

    This client provides methods to manage users in the Open To Close platform.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the users client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API
        """
        super().__init__(api_key=api_key, base_url=base_url)

    def list_users(
        self, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of users.

        Args:
            params: Optional dictionary of query parameters for filtering

        Returns:
            A list of dictionaries, where each dictionary represents a user

        Raises:
            OpenToCloseAPIError: If the API request fails
            ValidationError: If parameters are invalid
            AuthenticationError: If authentication fails

        Example:
            ```python
            # Get all users
            users = client.users.list_users()

            # Get users with custom parameters
            users = client.users.list_users(params={"limit": 50})
            ```
        """
        response = self.get("/users", params=params)
        return self._process_list_response(response)

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user.

        Args:
            user_data: A dictionary containing the user's information

        Returns:
            A dictionary representing the newly created user

        Raises:
            OpenToCloseAPIError: If the API request fails
            ValidationError: If user data is invalid
            AuthenticationError: If authentication fails

        Example:
            ```python
            user = client.users.create_user({
                "name": "John Doe",
                "email": "john@example.com",
                "role": "agent"
            })
            ```
        """
        response = self.post("/users", json_data=user_data)
        return self._process_response_data(response)

    def retrieve_user(self, user_id: int) -> Dict[str, Any]:
        """Retrieve a specific user by their ID.

        Args:
            user_id: The ID of the user to retrieve

        Returns:
            A dictionary representing the user

        Raises:
            NotFoundError: If the user is not found
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            user = client.users.retrieve_user(123)
            print(f"User name: {user['name']}")
            ```
        """
        response = self.get(f"/users/{user_id}")
        return self._process_response_data(response)

    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing user.

        Args:
            user_id: The ID of the user to update
            user_data: A dictionary containing the fields to update

        Returns:
            A dictionary representing the updated user

        Raises:
            NotFoundError: If the user is not found
            ValidationError: If user data is invalid
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            updated_user = client.users.update_user(123, {
                "name": "Jane Doe",
                "email": "jane@example.com"
            })
            ```
        """
        response = self.put(f"/users/{user_id}", json_data=user_data)
        return self._process_response_data(response)

    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """Delete a user by their ID.

        Args:
            user_id: The ID of the user to delete

        Returns:
            A dictionary containing the API response

        Raises:
            NotFoundError: If the user is not found
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            result = client.users.delete_user(123)
            ```
        """
        return self.delete(f"/users/{user_id}")
