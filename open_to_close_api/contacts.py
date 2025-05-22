from typing import Dict, Any, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .client import OpenToCloseAPI

class ContactsAPI:
    """Handles API requests for Contact related endpoints."""

    def __init__(self, client: 'OpenToCloseAPI'):
        """Initializes the ContactsAPI with a client instance.

        Args:
            client: The OpenToCloseAPI client instance.
        """
        self._client = client

    def list_contacts(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Retrieves a list of contacts.

        Args:
            params: Optional dictionary of query parameters.

        Returns:
            A list of dictionaries, where each dictionary represents a contact.
        """
        response = self._client._request("GET", "/contacts", params=params)
        json_response = response.json()
        if isinstance(json_response, list):
            return json_response
        elif isinstance(json_response, dict):
            return json_response.get("data", [])
        return []

    def create_contact(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new contact."""
        response = self._client._request("POST", "/contacts", json_data=contact_data)
        json_response = response.json()
        # If the response itself is the created object (common for POST returning the new resource)
        if isinstance(json_response, dict) and json_response.get('id'): # Check if it looks like the resource itself
            return json_response
        # Fallback to checking a "data" key
        return json_response.get("data", {})

    def retrieve_contact(self, contact_id: int) -> Dict[str, Any]:
        """Retrieves a specific contact by its ID."""
        response = self._client._request("GET", f"/contacts/{contact_id}")
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get('id'):
            return json_response
        return json_response.get("data", {})

    def update_contact(self, contact_id: int, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Updates an existing contact."""
        response = self._client._request("PUT", f"/contacts/{contact_id}", json_data=contact_data)
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get('id'): # Or check for a success message/status if applicable
            return json_response
        return json_response.get("data", {})

    def delete_contact(self, contact_id: int) -> Dict[str, Any]:
        """Deletes a contact by its ID.

        Args:
            contact_id: The ID of the contact to delete.
        
        Returns:
            A dictionary containing the API response.
        """
        response = self._client._request("DELETE", f"/contacts/{contact_id}")
        if response.status_code == 204:
            return {}
        return response.json() 