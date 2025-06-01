"""Property tasks client for Open To Close API."""

from typing import Any, Dict, List, Optional

from .base_client import BaseClient


class PropertyTasksAPI(BaseClient):
    """Client for property tasks API endpoints.
    
    This client provides methods to manage tasks associated with specific properties
    in the Open To Close platform.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the property tasks client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API
        """
        super().__init__(api_key=api_key, base_url=base_url)

    def list_property_tasks(
        self, property_id: int, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of tasks for a specific property.

        Args:
            property_id: The ID of the property
            params: Optional dictionary of query parameters for filtering

        Returns:
            A list of dictionaries, where each dictionary represents a property task

        Raises:
            OpenToCloseAPIError: If the API request fails
            NotFoundError: If the property is not found
            ValidationError: If parameters are invalid
            AuthenticationError: If authentication fails

        Example:
            ```python
            # Get all tasks for a property
            tasks = client.property_tasks.list_property_tasks(123)

            # Get tasks with filtering
            tasks = client.property_tasks.list_property_tasks(
                123, params={"status": "pending"}
            )
            ```
        """
        response = self.get(f"/properties/{property_id}/tasks", params=params)
        if isinstance(response, list):
            return response
        elif isinstance(response, dict):
            data = response.get("data", [])
            return data if isinstance(data, list) else []
        return []

    def create_property_task(
        self, property_id: int, task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add a task to a specific property.

        Args:
            property_id: The ID of the property
            task_data: A dictionary containing the task's information

        Returns:
            A dictionary representing the newly added property task

        Raises:
            OpenToCloseAPIError: If the API request fails
            ValidationError: If task data is invalid
            NotFoundError: If the property is not found
            AuthenticationError: If authentication fails

        Example:
            ```python
            task = client.property_tasks.create_property_task(123, {
                "title": "Schedule inspection",
                "description": "Arrange property inspection with buyer.",
                "due_date": "2024-01-15"
            })
            ```
        """
        response = self.post(f"/properties/{property_id}/tasks", json_data=task_data)
        if isinstance(response, dict) and response.get("id"):
            return response
        if isinstance(response, dict):
            data = response.get("data", {})
            return data if isinstance(data, dict) else {}
        return {}

    def retrieve_property_task(self, property_id: int, task_id: int) -> Dict[str, Any]:
        """Retrieve a specific task for a specific property.

        Args:
            property_id: The ID of the property
            task_id: The ID of the task to retrieve

        Returns:
            A dictionary representing the property task

        Raises:
            NotFoundError: If the property or task is not found
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            task = client.property_tasks.retrieve_property_task(123, 456)
            print(f"Task title: {task['title']}")
            ```
        """
        response = self.get(f"/properties/{property_id}/tasks/{task_id}")
        if isinstance(response, dict) and response.get("id"):
            return response
        if isinstance(response, dict):
            data = response.get("data", {})
            return data if isinstance(data, dict) else {}
        return {}

    def update_property_task(
        self, property_id: int, task_id: int, task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a specific task for a specific property.

        Args:
            property_id: The ID of the property
            task_id: The ID of the task to update
            task_data: A dictionary containing the fields to update

        Returns:
            A dictionary representing the updated property task

        Raises:
            NotFoundError: If the property or task is not found
            ValidationError: If task data is invalid
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            updated_task = client.property_tasks.update_property_task(
                123, 456, {"status": "completed"}
            )
            ```
        """
        response = self.put(f"/properties/{property_id}/tasks/{task_id}", json_data=task_data)
        if isinstance(response, dict) and response.get("id"):
            return response
        if isinstance(response, dict):
            data = response.get("data", {})
            return data if isinstance(data, dict) else {}
        return {}

    def delete_property_task(self, property_id: int, task_id: int) -> Dict[str, Any]:
        """Remove a task from a specific property.

        Args:
            property_id: The ID of the property
            task_id: The ID of the task to remove

        Returns:
            A dictionary containing the API response

        Raises:
            NotFoundError: If the property or task is not found
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            result = client.property_tasks.delete_property_task(123, 456)
            ```
        """
        return self.delete(f"/properties/{property_id}/tasks/{task_id}")
