"""Contacts client for Open To Close API."""

import logging
from typing import Any, Dict, List, Optional

from .base_client import BaseClient
from .exceptions import ValidationError

logger = logging.getLogger(__name__)


class ContactsAPI(BaseClient):
    """Client for contacts API endpoints.

    This client provides methods to manage contacts in the Open To Close platform.
    All methods include comprehensive input validation and error handling.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the contacts client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API

        Raises:
            AuthenticationError: If API key is missing or invalid
            ConfigurationError: If configuration is invalid
        """
        super().__init__(api_key=api_key, base_url=base_url)
        logger.debug("Initialized ContactsAPI client")

    def _validate_contact_data(
        self, contact_data: Dict[str, Any], operation: str
    ) -> None:
        """Validate contact data before sending to API.

        Args:
            contact_data: Contact data to validate
            operation: Operation type for error context (create/update)

        Raises:
            ValidationError: If contact data is invalid
        """
        if not isinstance(contact_data, dict):
            raise ValidationError(
                f"Contact data for {operation} must be a dictionary, got {type(contact_data).__name__}"
            )

        if not contact_data:
            raise ValidationError(f"Contact data for {operation} cannot be empty")

        # Validate required fields for create operations
        if operation == "create":
            # Check for at least one identifier field
            # NOTE: The 'name' field is NOT supported by the API - use first_name/last_name instead
            identifier_fields = ["email", "phone", "first_name", "last_name"]
            if not any(field in contact_data for field in identifier_fields):
                raise ValidationError(
                    f"Contact data for {operation} must include at least one of: {', '.join(identifier_fields)}"
                )

            # Warn if unsupported 'name' field is used
            if "name" in contact_data:
                raise ValidationError(
                    "The 'name' field is not supported by the API. "
                    "Use 'first_name' and 'last_name' fields instead."
                )

        # Validate email format if provided
        if "email" in contact_data:
            email = contact_data["email"]
            if not isinstance(email, str) or "@" not in email:
                raise ValidationError(f"Invalid email format: {email}")

        # Validate phone format if provided
        if "phone" in contact_data:
            phone = contact_data["phone"]
            if not isinstance(phone, str) or len(phone.strip()) == 0:
                raise ValidationError(f"Phone must be a non-empty string, got: {phone}")

        # Validate name fields if provided
        for name_field in ["first_name", "last_name"]:
            if name_field in contact_data:
                name_value = contact_data[name_field]
                if not isinstance(name_value, str) or len(name_value.strip()) == 0:
                    raise ValidationError(
                        f"{name_field} must be a non-empty string, got: {name_value}"
                    )

        logger.debug(f"Contact data validated for {operation} operation")

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

        logger.debug("List parameters validated", extra={"params": validated_params})
        return validated_params

    def list_contacts(
        self, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of contacts with validation and error handling.

        Args:
            params: Optional dictionary of query parameters for filtering.
                   Supported parameters may include:
                   - limit: Maximum number of contacts to return
                   - offset: Number of contacts to skip
                   - search: Search term for filtering contacts

        Returns:
            A list of dictionaries, where each dictionary represents a contact

        Raises:
            ValidationError: If parameters are invalid
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            # Get all contacts
            contacts = client.contacts.list_contacts()

            # Get contacts with custom parameters
            contacts = client.contacts.list_contacts(params={"limit": 50, "offset": 100})
            ```
        """
        try:
            validated_params = self._validate_list_params(params)

            logger.info("Listing contacts", extra={"params": validated_params})
            response = self.get("/contacts", params=validated_params)
            result = self._process_list_response(response, "/contacts")

            logger.info(f"Successfully retrieved {len(result)} contacts")
            return result

        except Exception as e:
            logger.error(f"Failed to list contacts: {str(e)}", extra={"params": params})
            raise

    def create_contact(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new contact with comprehensive validation.

        **Important:** The API requires separate first_name and last_name fields.
        The 'name' field is NOT supported and will cause validation errors.

        Args:
            contact_data: A dictionary containing the contact's information.
                         Must include at least one of: email, phone, first_name, last_name.
                         Supported fields include:
                         - email: Contact email address
                         - phone: Contact phone number
                         - first_name: First name (required if no email/phone)
                         - last_name: Last name (required if no email/phone)

                         **Unsupported fields** (will cause API errors):
                         - name: Not supported - use first_name/last_name instead
                         - company: Not supported in basic contact creation
                         - title: Not supported in basic contact creation

        Returns:
            A dictionary representing the newly created contact

        Raises:
            ValidationError: If contact data is invalid or missing required fields
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            # Correct usage with first_name and last_name
            contact = client.contacts.create_contact({
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "phone": "+1234567890"
            })

            # Minimal contact with just email
            contact = client.contacts.create_contact({
                "email": "jane@example.com"
            })

            # Contact with just phone
            contact = client.contacts.create_contact({
                "phone": "+1555123456"
            })
            ```
        """
        try:
            self._validate_contact_data(contact_data, "create")

            logger.info(
                "Creating new contact", extra={"has_email": "email" in contact_data}
            )
            response = self.post("/contacts", json_data=contact_data)
            result = self._process_response_data(response, "/contacts")

            contact_id = result.get("id")
            logger.info(f"Successfully created contact with ID: {contact_id}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to create contact: {str(e)}",
                extra={
                    "contact_data_keys": (
                        list(contact_data.keys())
                        if isinstance(contact_data, dict)
                        else "invalid"
                    )
                },
            )
            raise

    def retrieve_contact(self, contact_id: int) -> Dict[str, Any]:
        """Retrieve a specific contact by their ID with validation.

        Args:
            contact_id: The ID of the contact to retrieve (must be a positive integer)

        Returns:
            A dictionary representing the contact

        Raises:
            ValidationError: If contact_id is invalid
            NotFoundError: If the contact is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            contact = client.contacts.retrieve_contact(123)
            first_name = contact.get('first_name', '')
            last_name = contact.get('last_name', '')
            full_name = f"{first_name} {last_name}".strip() or 'N/A'
            print(f"Contact name: {full_name}")
            ```
        """
        try:
            validated_id = self._validate_resource_id(contact_id, "contact")

            logger.info(f"Retrieving contact with ID: {validated_id}")
            response = self.get(f"/contacts/{validated_id}")
            result = self._process_response_data(response, f"/contacts/{validated_id}")

            logger.info(f"Successfully retrieved contact: {validated_id}")
            return result

        except Exception as e:
            logger.error(f"Failed to retrieve contact {contact_id}: {str(e)}")
            raise

    def update_contact(
        self, contact_id: int, contact_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing contact with validation.

        Args:
            contact_id: The ID of the contact to update (must be a positive integer)
            contact_data: A dictionary containing the fields to update.
                         Supported fields include:
                         - email, phone, first_name, last_name

                         **Note:** The 'name' field is not supported - use first_name/last_name instead.

        Returns:
            A dictionary representing the updated contact

        Raises:
            ValidationError: If contact_id or contact_data is invalid
            NotFoundError: If the contact is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            updated_contact = client.contacts.update_contact(123, {
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "jane@example.com"
            })
            ```
        """
        try:
            validated_id = self._validate_resource_id(contact_id, "contact")
            self._validate_contact_data(contact_data, "update")

            logger.info(
                f"Updating contact with ID: {validated_id}",
                extra={"update_fields": list(contact_data.keys())},
            )
            response = self.put(f"/contacts/{validated_id}", json_data=contact_data)
            result = self._process_response_data(response, f"/contacts/{validated_id}")

            logger.info(f"Successfully updated contact: {validated_id}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to update contact {contact_id}: {str(e)}",
                extra={
                    "contact_data_keys": (
                        list(contact_data.keys())
                        if isinstance(contact_data, dict)
                        else "invalid"
                    )
                },
            )
            raise

    def delete_contact(self, contact_id: int) -> Dict[str, Any]:
        """Delete a contact by their ID with validation.

        Args:
            contact_id: The ID of the contact to delete (must be a positive integer)

        Returns:
            A dictionary containing the API response (typically empty for successful deletions)

        Raises:
            ValidationError: If contact_id is invalid
            NotFoundError: If the contact is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            result = client.contacts.delete_contact(123)
            print("Contact deleted successfully")
            ```
        """
        try:
            validated_id = self._validate_resource_id(contact_id, "contact")

            logger.info(f"Deleting contact with ID: {validated_id}")
            result = self.delete(f"/contacts/{validated_id}")

            logger.info(f"Successfully deleted contact: {validated_id}")
            return result

        except Exception as e:
            logger.error(f"Failed to delete contact {contact_id}: {str(e)}")
            raise
