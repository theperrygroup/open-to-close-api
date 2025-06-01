"""Property emails client for Open To Close API."""

from typing import Any, Dict, List, Optional

from .base_client import BaseClient


class PropertyEmailsAPI(BaseClient):
    """Client for property emails API endpoints.
    
    This client provides methods to manage emails associated with specific properties
    in the Open To Close platform.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the property emails client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API
        """
        super().__init__(api_key=api_key, base_url=base_url)

    def list_property_emails(
        self, property_id: int, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of emails for a specific property.

        Args:
            property_id: The ID of the property
            params: Optional dictionary of query parameters for filtering

        Returns:
            A list of dictionaries, where each dictionary represents a property email

        Raises:
            OpenToCloseAPIError: If the API request fails
            NotFoundError: If the property is not found
            ValidationError: If parameters are invalid
            AuthenticationError: If authentication fails

        Example:
            ```python
            # Get all emails for a property
            emails = client.property_emails.list_property_emails(123)

            # Get emails with filtering
            emails = client.property_emails.list_property_emails(
                123, params={"limit": 10}
            )
            ```
        """
        response = self.get(f"/properties/{property_id}/emails", params=params)
        if isinstance(response, list):
            return response
        elif isinstance(response, dict):
            data = response.get("data", [])
            return data if isinstance(data, list) else []
        return []

    def create_property_email(
        self, property_id: int, email_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add an email to a specific property.

        Args:
            property_id: The ID of the property
            email_data: A dictionary containing the email's information to be added

        Returns:
            A dictionary representing the newly added property email

        Raises:
            OpenToCloseAPIError: If the API request fails
            ValidationError: If email data is invalid
            NotFoundError: If the property is not found
            AuthenticationError: If authentication fails

        Example:
            ```python
            email = client.property_emails.create_property_email(123, {
                "subject": "Property Update",
                "body": "Property status has been updated."
            })
            ```
        """
        response = self.post(f"/properties/{property_id}/emails", json_data=email_data)
        if isinstance(response, dict) and response.get("id"):
            return response
        if isinstance(response, dict):
            data = response.get("data", {})
            return data if isinstance(data, dict) else {}
        return {}

    def retrieve_property_email(
        self, property_id: int, email_id: int
    ) -> Dict[str, Any]:
        """Retrieve a specific email for a specific property.

        Args:
            property_id: The ID of the property
            email_id: The ID of the email to retrieve

        Returns:
            A dictionary representing the property email

        Raises:
            NotFoundError: If the property or email is not found
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            email = client.property_emails.retrieve_property_email(123, 456)
            print(f"Email subject: {email['subject']}")
            ```
        """
        response = self.get(f"/properties/{property_id}/emails/{email_id}")
        if isinstance(response, dict) and response.get("id"):
            return response
        if isinstance(response, dict):
            data = response.get("data", {})
            return data if isinstance(data, dict) else {}
        return {}

    def update_property_email(
        self, property_id: int, email_id: int, email_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a specific email for a specific property.

        Args:
            property_id: The ID of the property
            email_id: The ID of the email to update
            email_data: A dictionary containing the fields to update

        Returns:
            A dictionary representing the updated property email

        Raises:
            NotFoundError: If the property or email is not found
            ValidationError: If email data is invalid
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            updated_email = client.property_emails.update_property_email(
                123, 456, {"subject": "Updated Property Status"}
            )
            ```
        """
        response = self.put(
            f"/properties/{property_id}/emails/{email_id}", json_data=email_data
        )
        if isinstance(response, dict) and response.get("id"):
            return response
        if isinstance(response, dict):
            data = response.get("data", {})
            return data if isinstance(data, dict) else {}
        return {}

    def delete_property_email(
        self, property_id: int, email_id: int
    ) -> Dict[str, Any]:
        """Remove an email from a specific property.

        Args:
            property_id: The ID of the property
            email_id: The ID of the email to remove

        Returns:
            A dictionary containing the API response

        Raises:
            NotFoundError: If the property or email is not found
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            result = client.property_emails.delete_property_email(123, 456)
            ```
        """
        return self.delete(f"/properties/{property_id}/emails/{email_id}")
