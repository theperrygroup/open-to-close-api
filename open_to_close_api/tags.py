from typing import Dict, Any, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .client import OpenToCloseAPI

class TagsAPI:
    """Handles API requests for Tag related endpoints."""

    def __init__(self, client: 'OpenToCloseAPI'):
        """Initializes the TagsAPI with a client instance.

        Args:
            client: The OpenToCloseAPI client instance.
        """
        self._client = client

    def list_tags(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Retrieves a list of tags.

        Args:
            params: Optional dictionary of query parameters.

        Returns:
            A list of dictionaries, where each dictionary represents a tag.
        """
        response = self._client._request("GET", "/tags", params=params)
        json_response = response.json()
        if isinstance(json_response, list):
            return json_response
        elif isinstance(json_response, dict):
            return json_response.get("data", [])
        return []

    def create_tag(self, tag_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new tag.

        Args:
            tag_data: A dictionary containing the tag's information.

        Returns:
            A dictionary representing the newly created tag.
        """
        response = self._client._request("POST", "/tags", json_data=tag_data)
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get('id'): return json_response
        return json_response.get("data", {})

    def retrieve_tag(self, tag_id: int) -> Dict[str, Any]:
        """Retrieves a specific tag by its ID.

        Args:
            tag_id: The ID of the tag to retrieve.

        Returns:
            A dictionary representing the tag.
        """
        response = self._client._request("GET", f"/tags/{tag_id}")
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get('id'): return json_response
        return json_response.get("data", {})

    def update_tag(self, tag_id: int, tag_data: Dict[str, Any]) -> Dict[str, Any]:
        """Updates an existing tag.

        Args:
            tag_id: The ID of the tag to update.
            tag_data: A dictionary containing the fields to update.

        Returns:
            A dictionary representing the updated tag.
        """
        response = self._client._request("PUT", f"/tags/{tag_id}", json_data=tag_data)
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get('id'): return json_response
        return json_response.get("data", {})

    def delete_tag(self, tag_id: int) -> Dict[str, Any]:
        """Deletes a tag by its ID.

        Args:
            tag_id: The ID of the tag to delete.
        
        Returns:
            A dictionary containing the API response.
        """
        response = self._client._request("DELETE", f"/tags/{tag_id}")
        if response.status_code == 204:
            return {}
        return response.json() 