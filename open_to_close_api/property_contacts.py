from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:  # pragma: no cover
    from .client import OpenToCloseAPI


class PropertyContactsAPI:
    """Handles API requests for Property Contact related endpoints."""

    def __init__(self, client: "OpenToCloseAPI"):
        """Initializes the PropertyContactsAPI with a client instance.

        Args:
            client: The OpenToCloseAPI client instance.
        """
        self._client = client

    def list_property_contacts(
        self, property_id: int, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieves a list of contacts for a specific property.

        Args:
            property_id: The ID of the property.
            params: Optional dictionary of query parameters.

        Returns:
            A list of dictionaries, where each dictionary represents a property contact.
        """
        response = self._client._request(
            "GET", f"/properties/{property_id}/contacts", params=params
        )
        json_response = response.json()
        if isinstance(json_response, list):
            return json_response
        elif isinstance(json_response, dict):
            return json_response.get("data", [])
        return []

    def create_property_contact(
        self, property_id: int, contact_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Adds a contact to a specific property.

        Args:
            property_id: The ID of the property.
            contact_data: A dictionary containing the contact's information to be added.

        Returns:
            A dictionary representing the newly added property contact.
        """
        response = self._client._request(
            "POST", f"/properties/{property_id}/contacts", json_data=contact_data
        )
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get("id"):
            return json_response
        return json_response.get("data", {})

    def retrieve_property_contact(
        self, property_id: int, contact_id: int
    ) -> Dict[str, Any]:
        """Retrieves a specific contact for a specific property.

        Args:
            property_id: The ID of the property.
            contact_id: The ID of the contact to retrieve.

        Returns:
            A dictionary representing the property contact.
        """
        response = self._client._request(
            "GET", f"/properties/{property_id}/contacts/{contact_id}"
        )
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get("id"):
            return json_response
        return json_response.get("data", {})

    def update_property_contact(
        self, property_id: int, contact_id: int, contact_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Updates a specific contact for a specific property.

        Args:
            property_id: The ID of the property.
            contact_id: The ID of the contact to update.
            contact_data: A dictionary containing the fields to update.

        Returns:
            A dictionary representing the updated property contact.
        """
        response = self._client._request(
            "PUT",
            f"/properties/{property_id}/contacts/{contact_id}",
            json_data=contact_data,
        )
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get("id"):
            return json_response
        return json_response.get("data", {})

    def delete_property_contact(
        self, property_id: int, contact_id: int
    ) -> Dict[str, Any]:
        """Removes a contact from a specific property.

        Args:
            property_id: The ID of the property.
            contact_id: The ID of the contact to remove.

        Returns:
            A dictionary containing the API response.
        """
        response = self._client._request(
            "DELETE", f"/properties/{property_id}/contacts/{contact_id}"
        )
        if response.status_code == 204:
            return {}
        return response.json()
