"""Property contacts client for Open To Close API."""

from typing import Any, Dict, List, Optional

from .base_client import BaseClient


class PropertyContactsAPI(BaseClient):
    """Client for property contacts API endpoints.

    This client provides methods to manage contacts associated with specific properties
    in the Open To Close platform.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the property contacts client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API
        """
        super().__init__(api_key=api_key, base_url=base_url)

    def list_property_contacts(
        self, property_id: int, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of contacts for a specific property.

        Args:
            property_id: The ID of the property
            params: Optional dictionary of query parameters for filtering

        Returns:
            A list of dictionaries, where each dictionary represents a property contact

        Raises:
            OpenToCloseAPIError: If the API request fails
            NotFoundError: If the property is not found
            ValidationError: If parameters are invalid
            AuthenticationError: If authentication fails

        Example:
            ```python
            # Get all contacts for a property
            contacts = client.property_contacts.list_property_contacts(123)

            # Get contacts with filtering
            contacts = client.property_contacts.list_property_contacts(
                123, params={"limit": 10}
            )
            ```
        """
        response = self.get(f"/properties/{property_id}/contacts", params=params)
        return self._process_list_response(response)

    def create_property_contact(
        self, property_id: int, contact_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add a contact to a specific property.

        Args:
            property_id: The ID of the property
            contact_data: A dictionary containing the contact's information to be added

        Returns:
            A dictionary representing the newly added property contact

        Raises:
            OpenToCloseAPIError: If the API request fails
            ValidationError: If contact data is invalid
            NotFoundError: If the property is not found
            AuthenticationError: If authentication fails

        Example:
            ```python
            contact = client.property_contacts.create_property_contact(123, {
                "contact_id": 456,
                "role": "buyer"
            })
            ```
        """
        response = self.post(
            f"/properties/{property_id}/contacts", json_data=contact_data
        )
        return self._process_response_data(response)

    def retrieve_property_contact(
        self, property_id: int, contact_id: int
    ) -> Dict[str, Any]:
        """Retrieve a specific contact for a specific property.

        Args:
            property_id: The ID of the property
            contact_id: The ID of the contact to retrieve

        Returns:
            A dictionary representing the property contact

        Raises:
            NotFoundError: If the property or contact is not found
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            contact = client.property_contacts.retrieve_property_contact(123, 456)
            print(f"Contact role: {contact['role']}")
            ```
        """
        response = self.get(f"/properties/{property_id}/contacts/{contact_id}")
        return self._process_response_data(response)

    def update_property_contact(
        self, property_id: int, contact_id: int, contact_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a specific contact for a specific property.

        Args:
            property_id: The ID of the property
            contact_id: The ID of the contact to update
            contact_data: A dictionary containing the fields to update

        Returns:
            A dictionary representing the updated property contact

        Raises:
            NotFoundError: If the property or contact is not found
            ValidationError: If contact data is invalid
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            updated_contact = client.property_contacts.update_property_contact(
                123, 456, {"role": "seller"}
            )
            ```
        """
        response = self.put(
            f"/properties/{property_id}/contacts/{contact_id}", json_data=contact_data
        )
        return self._process_response_data(response)

    def delete_property_contact(
        self, property_id: int, contact_id: int
    ) -> Dict[str, Any]:
        """Remove a contact from a specific property.

        Args:
            property_id: The ID of the property
            contact_id: The ID of the contact to remove

        Returns:
            A dictionary containing the API response

        Raises:
            NotFoundError: If the property or contact is not found
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            result = client.property_contacts.delete_property_contact(123, 456)
            ```
        """
        return self.delete(f"/properties/{property_id}/contacts/{contact_id}")
