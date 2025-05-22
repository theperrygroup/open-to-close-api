from typing import Dict, Any, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .client import OpenToCloseAPI

class PropertyTasksAPI:
    """Handles API requests for Property Task related endpoints."""

    def __init__(self, client: 'OpenToCloseAPI'):
        """Initializes the PropertyTasksAPI with a client instance.

        Args:
            client: The OpenToCloseAPI client instance.
        """
        self._client = client

    def list_property_tasks(self, property_id: int, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Retrieves a list of tasks for a specific property.

        Args:
            property_id: The ID of the property.
            params: Optional dictionary of query parameters.

        Returns:
            A list of dictionaries, where each dictionary represents a property task.
        """
        response = self._client._request("GET", f"/properties/{property_id}/tasks", params=params)
        json_response = response.json()
        if isinstance(json_response, list):
            return json_response
        elif isinstance(json_response, dict):
            return json_response.get("data", [])
        return []

    def create_property_task(self, property_id: int, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Adds a task to a specific property.

        Args:
            property_id: The ID of the property.
            task_data: A dictionary containing the task's information.

        Returns:
            A dictionary representing the newly added property task.
        """
        response = self._client._request("POST", f"/properties/{property_id}/tasks", json_data=task_data)
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get('id'): return json_response
        return json_response.get("data", {})

    def retrieve_property_task(self, property_id: int, task_id: int) -> Dict[str, Any]:
        """Retrieves a specific task for a specific property.

        Args:
            property_id: The ID of the property.
            task_id: The ID of the task to retrieve.

        Returns:
            A dictionary representing the property task.
        """
        response = self._client._request("GET", f"/properties/{property_id}/tasks/{task_id}")
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get('id'): return json_response
        return json_response.get("data", {})

    def update_property_task(self, property_id: int, task_id: int, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Updates a specific task for a specific property.

        Args:
            property_id: The ID of the property.
            task_id: The ID of the task to update.
            task_data: A dictionary containing the fields to update.

        Returns:
            A dictionary representing the updated property task.
        """
        response = self._client._request("PUT", f"/properties/{property_id}/tasks/{task_id}", json_data=task_data)
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get('id'): return json_response
        return json_response.get("data", {})

    def delete_property_task(self, property_id: int, task_id: int) -> Dict[str, Any]:
        """Removes a task from a specific property.

        Args:
            property_id: The ID of the property.
            task_id: The ID of the task to remove.
        
        Returns:
            A dictionary containing the API response.
        """
        response = self._client._request("DELETE", f"/properties/{property_id}/tasks/{task_id}")
        if response.status_code == 204:
            return {}
        return response.json() 