"""Contacts client for Open To Close API."""

from typing import Any, Dict, List, Optional

from .base_client import BaseClient


class ContactsAPI(BaseClient):
    """Client for contacts API endpoints.

    This client provides methods to manage contacts in the Open To Close platform.
    """

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
        """Retrieve a list of contacts.

        Args:
            params: Optional dictionary of query parameters for filtering

        Returns:
            A list of dictionaries, where each dictionary represents a contact

        Raises:
            OpenToCloseAPIError: If the API request fails
            ValidationError: If parameters are invalid
            AuthenticationError: If authentication fails

        Example:
            ```python
            # Get all contacts
            contacts = client.contacts.list_contacts()

            # Get contacts with custom parameters
            contacts = client.contacts.list_contacts(params={"limit": 50})
            ```
        """
        response = self.get("/contacts", params=params)
        return self._process_list_response(response)

    def create_contact(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new contact.

        Args:
            contact_data: A dictionary containing the contact's information

        Returns:
            A dictionary representing the newly created contact

        Raises:
            OpenToCloseAPIError: If the API request fails
            ValidationError: If contact data is invalid
            AuthenticationError: If authentication fails

        Example:
            ```python
            contact = client.contacts.create_contact({
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "+1234567890"
            })
            ```
        """
        response = self.post("/contacts", json_data=contact_data)
        return self._process_response_data(response)

    def retrieve_contact(self, contact_id: int) -> Dict[str, Any]:
        """Retrieve a specific contact by their ID.

        Args:
            contact_id: The ID of the contact to retrieve

        Returns:
            A dictionary representing the contact

        Raises:
            NotFoundError: If the contact is not found
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            contact = client.contacts.retrieve_contact(123)
            print(f"Contact name: {contact['name']}")
            ```
        """
        response = self.get(f"/contacts/{contact_id}")
        return self._process_response_data(response)

    def update_contact(
        self, contact_id: int, contact_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing contact.

        Args:
            contact_id: The ID of the contact to update
            contact_data: A dictionary containing the fields to update

        Returns:
            A dictionary representing the updated contact

        Raises:
            NotFoundError: If the contact is not found
            ValidationError: If contact data is invalid
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            updated_contact = client.contacts.update_contact(123, {
                "name": "Jane Doe",
                "email": "jane@example.com"
            })
            ```
        """
        response = self.put(f"/contacts/{contact_id}", json_data=contact_data)
        return self._process_response_data(response)

    def delete_contact(self, contact_id: int) -> Dict[str, Any]:
        """Delete a contact by their ID.

        Args:
            contact_id: The ID of the contact to delete

        Returns:
            A dictionary containing the API response

        Raises:
            NotFoundError: If the contact is not found
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            result = client.contacts.delete_contact(123)
            ```
        """
        return self.delete(f"/contacts/{contact_id}")
