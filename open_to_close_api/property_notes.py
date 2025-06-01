"""Property notes client for Open To Close API."""

from typing import Any, Dict, List, Optional

from .base_client import BaseClient


class PropertyNotesAPI(BaseClient):
    """Client for property notes API endpoints.
    
    This client provides methods to manage notes associated with specific properties
    in the Open To Close platform.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the property notes client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API
        """
        super().__init__(api_key=api_key, base_url=base_url)

    def list_property_notes(
        self, property_id: int, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of notes for a specific property.

        Args:
            property_id: The ID of the property
            params: Optional dictionary of query parameters for filtering

        Returns:
            A list of dictionaries, where each dictionary represents a property note

        Raises:
            OpenToCloseAPIError: If the API request fails
            NotFoundError: If the property is not found
            ValidationError: If parameters are invalid
            AuthenticationError: If authentication fails

        Example:
            ```python
            # Get all notes for a property
            notes = client.property_notes.list_property_notes(123)

            # Get notes with filtering
            notes = client.property_notes.list_property_notes(
                123, params={"limit": 10}
            )
            ```
        """
        response = self.get(f"/properties/{property_id}/notes", params=params)
        if isinstance(response, list):
            return response
        elif isinstance(response, dict):
            data = response.get("data", [])
            return data if isinstance(data, list) else []
        return []

    def create_property_note(
        self, property_id: int, note_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add a note to a specific property.

        Args:
            property_id: The ID of the property
            note_data: A dictionary containing the note's information to be added

        Returns:
            A dictionary representing the newly added property note

        Raises:
            OpenToCloseAPIError: If the API request fails
            ValidationError: If note data is invalid
            NotFoundError: If the property is not found
            AuthenticationError: If authentication fails

        Example:
            ```python
            note = client.property_notes.create_property_note(123, {
                "content": "Property inspection completed successfully.",
                "private": False
            })
            ```
        """
        response = self.post(f"/properties/{property_id}/notes", json_data=note_data)
        if isinstance(response, dict) and response.get("id"):
            return response
        if isinstance(response, dict):
            data = response.get("data", {})
            return data if isinstance(data, dict) else {}
        return {}

    def retrieve_property_note(
        self, property_id: int, note_id: int
    ) -> Dict[str, Any]:
        """Retrieve a specific note for a specific property.

        Args:
            property_id: The ID of the property
            note_id: The ID of the note to retrieve

        Returns:
            A dictionary representing the property note

        Raises:
            NotFoundError: If the property or note is not found
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            note = client.property_notes.retrieve_property_note(123, 456)
            print(f"Note content: {note['content']}")
            ```
        """
        response = self.get(f"/properties/{property_id}/notes/{note_id}")
        if isinstance(response, dict) and response.get("id"):
            return response
        if isinstance(response, dict):
            data = response.get("data", {})
            return data if isinstance(data, dict) else {}
        return {}

    def update_property_note(
        self, property_id: int, note_id: int, note_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a specific note for a specific property.

        Args:
            property_id: The ID of the property
            note_id: The ID of the note to update
            note_data: A dictionary containing the fields to update

        Returns:
            A dictionary representing the updated property note

        Raises:
            NotFoundError: If the property or note is not found
            ValidationError: If note data is invalid
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            updated_note = client.property_notes.update_property_note(
                123, 456, {"content": "Updated note content"}
            )
            ```
        """
        response = self.put(
            f"/properties/{property_id}/notes/{note_id}", json_data=note_data
        )
        if isinstance(response, dict) and response.get("id"):
            return response
        if isinstance(response, dict):
            data = response.get("data", {})
            return data if isinstance(data, dict) else {}
        return {}

    def delete_property_note(
        self, property_id: int, note_id: int
    ) -> Dict[str, Any]:
        """Remove a note from a specific property.

        Args:
            property_id: The ID of the property
            note_id: The ID of the note to remove

        Returns:
            A dictionary containing the API response

        Raises:
            NotFoundError: If the property or note is not found
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            result = client.property_notes.delete_property_note(123, 456)
            ```
        """
        return self.delete(f"/properties/{property_id}/notes/{note_id}")
