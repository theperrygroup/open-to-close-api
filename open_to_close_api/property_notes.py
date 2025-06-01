from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:  # pragma: no cover
    from .client import OpenToCloseAPI


class PropertyNotesAPI:
    """Handles API requests for Property Note related endpoints."""

    def __init__(self, client: "OpenToCloseAPI"):
        """Initializes the PropertyNotesAPI with a client instance.

        Args:
            client: The OpenToCloseAPI client instance.
        """
        self._client = client

    def list_property_notes(
        self, property_id: int, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieves a list of notes for a specific property.

        Args:
            property_id: The ID of the property.
            params: Optional dictionary of query parameters.

        Returns:
            A list of dictionaries, where each dictionary represents a property note.
        """
        response = self._client._request(
            "GET", f"/properties/{property_id}/notes", params=params
        )
        json_response = response.json()
        if isinstance(json_response, list):
            return json_response
        elif isinstance(json_response, dict):
            return json_response.get("data", [])
        return []

    def create_property_note(
        self, property_id: int, note_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Adds a note to a specific property.

        Args:
            property_id: The ID of the property.
            note_data: A dictionary containing the note's information.

        Returns:
            A dictionary representing the newly added property note.
        """
        response = self._client._request(
            "POST", f"/properties/{property_id}/notes", json_data=note_data
        )
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get("id"):
            return json_response
        return json_response.get("data", {})

    def retrieve_property_note(self, property_id: int, note_id: int) -> Dict[str, Any]:
        """Retrieves a specific note for a specific property.

        Args:
            property_id: The ID of the property.
            note_id: The ID of the note to retrieve.

        Returns:
            A dictionary representing the property note.
        """
        response = self._client._request(
            "GET", f"/properties/{property_id}/notes/{note_id}"
        )
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get("id"):
            return json_response
        return json_response.get("data", {})

    def update_property_note(
        self, property_id: int, note_id: int, note_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Updates a specific note for a specific property.

        Args:
            property_id: The ID of the property.
            note_id: The ID of the note to update.
            note_data: A dictionary containing the fields to update.

        Returns:
            A dictionary representing the updated property note.
        """
        response = self._client._request(
            "PUT", f"/properties/{property_id}/notes/{note_id}", json_data=note_data
        )
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get("id"):
            return json_response
        return json_response.get("data", {})

    def delete_property_note(self, property_id: int, note_id: int) -> Dict[str, Any]:
        """Removes a note from a specific property.

        Args:
            property_id: The ID of the property.
            note_id: The ID of the note to remove.

        Returns:
            A dictionary containing the API response.
        """
        response = self._client._request(
            "DELETE", f"/properties/{property_id}/notes/{note_id}"
        )
        if response.status_code == 204:
            return {}
        return response.json()
