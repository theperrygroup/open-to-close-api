"""Tags client for Open To Close API."""

from typing import Any, Dict, List, Optional

from .base_client import BaseClient


class TagsAPI(BaseClient):
    """Client for tags API endpoints.

    This client provides methods to manage tags in the Open To Close platform.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the tags client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API
        """
        super().__init__(api_key=api_key, base_url=base_url)

    def list_tags(
        self, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of tags.

        Args:
            params: Optional dictionary of query parameters for filtering

        Returns:
            A list of dictionaries, where each dictionary represents a tag

        Raises:
            OpenToCloseAPIError: If the API request fails
            ValidationError: If parameters are invalid
            AuthenticationError: If authentication fails

        Example:
            ```python
            # Get all tags
            tags = client.tags.list_tags()

            # Get tags with custom parameters
            tags = client.tags.list_tags(params={"limit": 50})
            ```
        """
        response = self.get("/tags", params=params)
        return self._process_list_response(response)

    def create_tag(self, tag_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new tag.

        Args:
            tag_data: A dictionary containing the tag's information

        Returns:
            A dictionary representing the newly created tag

        Raises:
            OpenToCloseAPIError: If the API request fails
            ValidationError: If tag data is invalid
            AuthenticationError: If authentication fails

        Example:
            ```python
            tag = client.tags.create_tag({
                "name": "High Priority",
                "color": "#FF0000"
            })
            ```
        """
        response = self.post("/tags", json_data=tag_data)
        return self._process_response_data(response)

    def retrieve_tag(self, tag_id: int) -> Dict[str, Any]:
        """Retrieve a specific tag by its ID.

        Args:
            tag_id: The ID of the tag to retrieve

        Returns:
            A dictionary representing the tag

        Raises:
            NotFoundError: If the tag is not found
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            tag = client.tags.retrieve_tag(123)
            print(f"Tag name: {tag['name']}")
            ```
        """
        response = self.get(f"/tags/{tag_id}")
        return self._process_response_data(response)

    def update_tag(self, tag_id: int, tag_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing tag.

        Args:
            tag_id: The ID of the tag to update
            tag_data: A dictionary containing the fields to update

        Returns:
            A dictionary representing the updated tag

        Raises:
            NotFoundError: If the tag is not found
            ValidationError: If tag data is invalid
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            updated_tag = client.tags.update_tag(123, {
                "name": "Updated Priority",
                "color": "#00FF00"
            })
            ```
        """
        response = self.put(f"/tags/{tag_id}", json_data=tag_data)
        return self._process_response_data(response)

    def delete_tag(self, tag_id: int) -> Dict[str, Any]:
        """Delete a tag by its ID.

        Args:
            tag_id: The ID of the tag to delete

        Returns:
            A dictionary containing the API response

        Raises:
            NotFoundError: If the tag is not found
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            result = client.tags.delete_tag(123)
            ```
        """
        return self.delete(f"/tags/{tag_id}")
