from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:  # pragma: no cover
    from .client import OpenToCloseAPI


class PropertyEmailsAPI:
    """Handles API requests for Property Email related endpoints."""

    def __init__(self, client: "OpenToCloseAPI"):
        """Initializes the PropertyEmailsAPI with a client instance.

        Args:
            client: The OpenToCloseAPI client instance.
        """
        self._client = client

    def list_property_emails(
        self, property_id: int, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieves a list of emails for a specific property.

        Args:
            property_id: The ID of the property.
            params: Optional dictionary of query parameters.

        Returns:
            A list of dictionaries, where each dictionary represents a property email.
        """
        response = self._client._request(
            "GET", f"/properties/{property_id}/emails", params=params
        )
        json_response = response.json()
        if isinstance(json_response, list):
            return json_response
        elif isinstance(json_response, dict):
            return json_response.get("data", [])
        return []

    def create_property_email(
        self, property_id: int, email_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Adds an email to a specific property.

        Args:
            property_id: The ID of the property.
            email_data: A dictionary containing the email's information.

        Returns:
            A dictionary representing the newly added property email.
        """
        response = self._client._request(
            "POST", f"/properties/{property_id}/emails", json_data=email_data
        )
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get("id"):
            return json_response
        return json_response.get("data", {})

    def retrieve_property_email(
        self, property_id: int, email_id: int
    ) -> Dict[str, Any]:
        """Retrieves a specific email for a specific property.

        Args:
            property_id: The ID of the property.
            email_id: The ID of the email to retrieve.

        Returns:
            A dictionary representing the property email.
        """
        response = self._client._request(
            "GET", f"/properties/{property_id}/emails/{email_id}"
        )
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get("id"):
            return json_response
        return json_response.get("data", {})

    def update_property_email(
        self, property_id: int, email_id: int, email_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Updates a specific email for a specific property.

        Args:
            property_id: The ID of the property.
            email_id: The ID of the email to update.
            email_data: A dictionary containing the fields to update.

        Returns:
            A dictionary representing the updated property email.
        """
        response = self._client._request(
            "PUT", f"/properties/{property_id}/emails/{email_id}", json_data=email_data
        )
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get("id"):
            return json_response
        return json_response.get("data", {})

    def delete_property_email(self, property_id: int, email_id: int) -> Dict[str, Any]:
        """Removes an email from a specific property.

        Args:
            property_id: The ID of the property.
            email_id: The ID of the email to remove.

        Returns:
            A dictionary containing the API response.
        """
        response = self._client._request(
            "DELETE", f"/properties/{property_id}/emails/{email_id}"
        )
        if response.status_code == 204:
            return {}
        return response.json()
