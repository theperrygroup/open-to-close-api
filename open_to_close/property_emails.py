"""Property emails client for Open To Close API."""

import logging
from typing import Any, Dict, List, Optional

from .base_client import BaseClient
from .exceptions import ValidationError

logger = logging.getLogger(__name__)


class PropertyEmailsAPI(BaseClient):
    """Client for property emails API endpoints.

    This client provides methods to manage emails associated with specific properties
    in the Open To Close platform. All methods include comprehensive input validation
    and error handling.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the property emails client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API

        Raises:
            AuthenticationError: If API key is missing or invalid
            ConfigurationError: If configuration is invalid
        """
        super().__init__(api_key=api_key, base_url=base_url)
        logger.debug("Initialized PropertyEmailsAPI client")

    def _validate_property_email_data(
        self, email_data: Dict[str, Any], operation: str
    ) -> None:
        """Validate property email data before sending to API.

        Args:
            email_data: Property email data to validate
            operation: Operation type for error context (create/update)

        Raises:
            ValidationError: If property email data is invalid
        """
        if not isinstance(email_data, dict):
            raise ValidationError(
                f"Property email data for {operation} must be a dictionary, got {type(email_data).__name__}"
            )

        if not email_data:
            raise ValidationError(
                f"Property email data for {operation} cannot be empty"
            )

        # Validate subject if provided
        if "subject" in email_data:
            subject = email_data["subject"]
            if not isinstance(subject, str) or len(subject.strip()) == 0:
                raise ValidationError(
                    f"subject must be a non-empty string, got: {subject}"
                )

        # Validate body if provided
        if "body" in email_data:
            body = email_data["body"]
            if not isinstance(body, str):
                raise ValidationError(
                    f"body must be a string, got {type(body).__name__}: {body}"
                )

        # Validate recipient email if provided
        if "recipient" in email_data:
            recipient = email_data["recipient"]
            if not isinstance(recipient, str) or "@" not in recipient:
                raise ValidationError(
                    f"recipient must be a valid email address, got: {recipient}"
                )

        # Validate sender email if provided
        if "sender" in email_data:
            sender = email_data["sender"]
            if not isinstance(sender, str) or "@" not in sender:
                raise ValidationError(
                    f"sender must be a valid email address, got: {sender}"
                )

        # Validate status if provided
        if "status" in email_data:
            status = email_data["status"]
            if not isinstance(status, str) or len(status.strip()) == 0:
                raise ValidationError(
                    f"status must be a non-empty string, got: {status}"
                )

        # Validate priority if provided
        if "priority" in email_data:
            priority = email_data["priority"]
            if not isinstance(priority, str) or len(priority.strip()) == 0:
                raise ValidationError(
                    f"priority must be a non-empty string, got: {priority}"
                )

        # Validate recipients list if provided (for multiple recipients)
        if "recipients" in email_data:
            recipients = email_data["recipients"]
            if not isinstance(recipients, list):
                raise ValidationError(
                    f"recipients must be a list, got {type(recipients).__name__}: {recipients}"
                )

            for i, recipient in enumerate(recipients):
                if not isinstance(recipient, str) or "@" not in recipient:
                    raise ValidationError(
                        f"recipients[{i}] must be a valid email address, got: {recipient}"
                    )

        logger.debug(f"Property email data validated for {operation} operation")

    def _validate_list_params(self, params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate and normalize parameters for list operations.

        Args:
            params: Parameters to validate

        Returns:
            Validated and normalized parameters

        Raises:
            ValidationError: If parameters are invalid
        """
        if params is None:
            return {}

        if not isinstance(params, dict):
            raise ValidationError(
                f"List parameters must be a dictionary, got {type(params).__name__}"
            )

        validated_params = params.copy()

        # Validate limit parameter
        if "limit" in validated_params:
            limit = validated_params["limit"]
            try:
                limit_int = int(limit)
                if limit_int <= 0:
                    raise ValidationError(
                        f"Limit must be a positive integer, got {limit_int}"
                    )
                if limit_int > 1000:  # Reasonable upper bound
                    logger.warning(
                        f"Large limit value: {limit_int}. Consider using pagination."
                    )
                validated_params["limit"] = limit_int
            except (ValueError, TypeError):
                raise ValidationError(
                    f"Limit must be an integer, got {type(limit).__name__}: {limit}"
                )

        # Validate offset parameter
        if "offset" in validated_params:
            offset = validated_params["offset"]
            try:
                offset_int = int(offset)
                if offset_int < 0:
                    raise ValidationError(
                        f"Offset must be non-negative, got {offset_int}"
                    )
                validated_params["offset"] = offset_int
            except (ValueError, TypeError):
                raise ValidationError(
                    f"Offset must be an integer, got {type(offset).__name__}: {offset}"
                )

        # Validate status filter if provided
        if "status" in validated_params:
            status = validated_params["status"]
            if not isinstance(status, str) or len(status.strip()) == 0:
                raise ValidationError(
                    f"Status filter must be a non-empty string, got: {status}"
                )

        logger.debug("List parameters validated", extra={"params": validated_params})
        return validated_params

    def list_property_emails(
        self, property_id: int, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of emails for a specific property with validation and error handling.

        Args:
            property_id: The ID of the property (must be a positive integer)
            params: Optional dictionary of query parameters for filtering.
                   Supported parameters may include:
                   - limit: Maximum number of property emails to return
                   - offset: Number of property emails to skip
                   - status: Filter by email status (e.g., 'sent', 'draft', 'failed')

        Returns:
            A list of dictionaries, where each dictionary represents a property email

        Raises:
            ValidationError: If property_id or parameters are invalid
            NotFoundError: If the property is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            # Get all emails for a property
            emails = client.property_emails.list_property_emails(123)

            # Get emails with filtering
            emails = client.property_emails.list_property_emails(
                123, params={"status": "sent", "limit": 10}
            )
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            validated_params = self._validate_list_params(params)

            logger.info(
                f"Listing emails for property {validated_property_id}",
                extra={"params": validated_params},
            )
            response = self.get(
                f"/properties/{validated_property_id}/emails", params=validated_params
            )
            result = self._process_list_response(
                response, f"/properties/{validated_property_id}/emails"
            )

            logger.info(
                f"Successfully retrieved {len(result)} emails for property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to list emails for property {property_id}: {str(e)}",
                extra={"params": params},
            )
            raise

    def create_property_email(
        self, property_id: int, email_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add an email to a specific property with comprehensive validation.

        Args:
            property_id: The ID of the property (must be a positive integer)
            email_data: A dictionary containing the email's information.
                       Common fields include:
                       - subject: Email subject
                       - body: Email body content
                       - recipient: Recipient email address
                       - sender: Sender email address
                       - status: Email status
                       - priority: Email priority

        Returns:
            A dictionary representing the newly added property email

        Raises:
            ValidationError: If property_id or email_data is invalid
            NotFoundError: If the property is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            email = client.property_emails.create_property_email(123, {
                "subject": "Property Update",
                "body": "The property status has been updated.",
                "recipient": "client@example.com",
                "status": "draft"
            })
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            self._validate_property_email_data(email_data, "create")

            logger.info(
                f"Creating email for property {validated_property_id}",
                extra={"subject": email_data.get("subject", "unknown")},
            )
            response = self.post(
                f"/properties/{validated_property_id}/emails", json_data=email_data
            )
            result = self._process_response_data(
                response, f"/properties/{validated_property_id}/emails"
            )

            logger.info(
                f"Successfully created email for property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to create email for property {property_id}: {str(e)}",
                extra={
                    "email_data_keys": (
                        list(email_data.keys())
                        if isinstance(email_data, dict)
                        else "invalid"
                    )
                },
            )
            raise

    def retrieve_property_email(
        self, property_id: int, email_id: int
    ) -> Dict[str, Any]:
        """Retrieve a specific email for a specific property with validation.

        Args:
            property_id: The ID of the property (must be a positive integer)
            email_id: The ID of the email to retrieve (must be a positive integer)

        Returns:
            A dictionary representing the property email

        Raises:
            ValidationError: If property_id or email_id is invalid
            NotFoundError: If the property or email is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            email = client.property_emails.retrieve_property_email(123, 456)
            print(f"Email subject: {email.get('subject', 'N/A')}")
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            validated_email_id = self._validate_resource_id(email_id, "email")

            logger.info(
                f"Retrieving email {validated_email_id} for property {validated_property_id}"
            )
            response = self.get(
                f"/properties/{validated_property_id}/emails/{validated_email_id}"
            )
            result = self._process_response_data(
                response,
                f"/properties/{validated_property_id}/emails/{validated_email_id}",
            )

            logger.info(
                f"Successfully retrieved email {validated_email_id} for property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to retrieve email {email_id} for property {property_id}: {str(e)}"
            )
            raise

    def update_property_email(
        self, property_id: int, email_id: int, email_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a specific email for a specific property with validation.

        Args:
            property_id: The ID of the property (must be a positive integer)
            email_id: The ID of the email to update (must be a positive integer)
            email_data: A dictionary containing the fields to update.
                       Fields can include:
                       - subject: Email subject
                       - body: Email body content
                       - status: Email status
                       - priority: Email priority

        Returns:
            A dictionary representing the updated property email

        Raises:
            ValidationError: If property_id, email_id, or email_data is invalid
            NotFoundError: If the property or email is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            updated_email = client.property_emails.update_property_email(
                123, 456, {"status": "sent", "priority": "high"}
            )
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            validated_email_id = self._validate_resource_id(email_id, "email")
            self._validate_property_email_data(email_data, "update")

            logger.info(
                f"Updating email {validated_email_id} for property {validated_property_id}",
                extra={"update_fields": list(email_data.keys())},
            )
            response = self.put(
                f"/properties/{validated_property_id}/emails/{validated_email_id}",
                json_data=email_data,
            )
            result = self._process_response_data(
                response,
                f"/properties/{validated_property_id}/emails/{validated_email_id}",
            )

            logger.info(
                f"Successfully updated email {validated_email_id} for property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to update email {email_id} for property {property_id}: {str(e)}",
                extra={
                    "email_data_keys": (
                        list(email_data.keys())
                        if isinstance(email_data, dict)
                        else "invalid"
                    )
                },
            )
            raise

    def delete_property_email(self, property_id: int, email_id: int) -> Dict[str, Any]:
        """Remove an email from a specific property with validation.

        Args:
            property_id: The ID of the property (must be a positive integer)
            email_id: The ID of the email to remove (must be a positive integer)

        Returns:
            A dictionary containing the API response (typically empty for successful deletions)

        Raises:
            ValidationError: If property_id or email_id is invalid
            NotFoundError: If the property or email is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            result = client.property_emails.delete_property_email(123, 456)
            print("Email removed from property successfully")
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            validated_email_id = self._validate_resource_id(email_id, "email")

            logger.info(
                f"Removing email {validated_email_id} from property {validated_property_id}"
            )
            result = self.delete(
                f"/properties/{validated_property_id}/emails/{validated_email_id}"
            )

            logger.info(
                f"Successfully removed email {validated_email_id} from property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to remove email {email_id} from property {property_id}: {str(e)}"
            )
            raise
