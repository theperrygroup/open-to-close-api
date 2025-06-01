"""Contacts client for Open To Close API."""

from typing import Any, Dict, List, Optional

from .base_client import BaseClient


class ContactsAPI(BaseClient):
    """Client for contacts API endpoints."""

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the contacts client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API
        """
        super().__init__(api_key=api_key, base_url=base_url)

    def list_contacts(
        self, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of contacts."""
        response = self.get("/contacts", params=params)
        if isinstance(response, list):
            return response
        elif isinstance(response, dict):
            return response.get("data", [])
        return []

    def create_contact(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new contact."""
        response = self.post("/contacts", json_data=contact_data)
        if isinstance(response, dict) and response.get("id"):
            return response
        return response.get("data", {}) if isinstance(response, dict) else {}

    def retrieve_contact(self, contact_id: int) -> Dict[str, Any]:
        """Retrieve a specific contact by ID."""
        response = self.get(f"/contacts/{contact_id}")
        if isinstance(response, dict) and response.get("id"):
            return response
        return response.get("data", {}) if isinstance(response, dict) else {}

    def update_contact(
        self, contact_id: int, contact_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing contact."""
        response = self.put(f"/contacts/{contact_id}", json_data=contact_data)
        if isinstance(response, dict) and response.get("id"):
            return response
        return response.get("data", {}) if isinstance(response, dict) else {}

    def delete_contact(self, contact_id: int) -> Dict[str, Any]:
        """Delete a contact by ID."""
        return self.delete(f"/contacts/{contact_id}")
