"""Property contacts client for Open To Close API."""

import logging
from typing import Any, Dict, List, Optional

from .base_client import BaseClient
from .exceptions import ValidationError

logger = logging.getLogger(__name__)


class PropertyContactsAPI(BaseClient):
    """Client for property contacts API endpoints.

    This client provides methods to manage contacts associated with specific properties
    in the Open To Close platform. All methods include comprehensive input validation
    and error handling.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the property contacts client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API

        Raises:
            AuthenticationError: If API key is missing or invalid
            ConfigurationError: If configuration is invalid
        """
        super().__init__(api_key=api_key, base_url=base_url)
        logger.debug("Initialized PropertyContactsAPI client")

    def _validate_property_contact_data(
        self, contact_data: Dict[str, Any], operation: str
    ) -> None:
        """Validate property contact data before sending to API.

        Args:
            contact_data: Property contact data to validate
            operation: Operation type for error context (create/update)

        Raises:
            ValidationError: If property contact data is invalid
        """
        if not isinstance(contact_data, dict):
            raise ValidationError(
                f"Property contact data for {operation} must be a dictionary, got {type(contact_data).__name__}"
            )

        if not contact_data:
            raise ValidationError(
                f"Property contact data for {operation} cannot be empty"
            )

        # Validate contact_id if provided (required for create operations typically)
        if "contact_id" in contact_data:
            contact_id = contact_data["contact_id"]
            try:
                contact_id_int = int(contact_id)
                if contact_id_int <= 0:
                    raise ValidationError(
                        f"contact_id must be a positive integer, got {contact_id_int}"
                    )
            except (ValueError, TypeError):
                raise ValidationError(
                    f"contact_id must be an integer, got {type(contact_id).__name__}: {contact_id}"
                )

        # Validate role if provided
        if "role" in contact_data:
            role = contact_data["role"]
            if not isinstance(role, str) or len(role.strip()) == 0:
                raise ValidationError(f"role must be a non-empty string, got: {role}")

        # Validate primary flag if provided
        if "is_primary" in contact_data:
            is_primary = contact_data["is_primary"]
            if not isinstance(is_primary, bool):
                raise ValidationError(
                    f"is_primary must be a boolean, got {type(is_primary).__name__}: {is_primary}"
                )

        logger.debug(f"Property contact data validated for {operation} operation")

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

    def list_property_contacts(
        self, property_id: int, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of contacts for a specific property with validation and error handling.

        Args:
            property_id: The ID of the property (must be a positive integer)
            params: Optional dictionary of query parameters for filtering.
                   Supported parameters may include:
                   - limit: Maximum number of property contacts to return
                   - offset: Number of property contacts to skip
                   - role: Filter by contact role

        Returns:
            A list of dictionaries, where each dictionary represents a property contact

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
            # Get all contacts for a property
            contacts = client.property_contacts.list_property_contacts(123)

            # Get contacts with filtering
            contacts = client.property_contacts.list_property_contacts(
                123, params={"limit": 10, "role": "buyer"}
            )
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            validated_params = self._validate_list_params(params)

            logger.info(
                f"Listing contacts for property {validated_property_id}",
                extra={"params": validated_params},
            )
            response = self.get(
                f"/properties/{validated_property_id}/contacts", params=validated_params
            )
            result = self._process_list_response(
                response, f"/properties/{validated_property_id}/contacts"
            )

            logger.info(
                f"Successfully retrieved {len(result)} contacts for property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to list contacts for property {property_id}: {str(e)}",
                extra={"params": params},
            )
            raise

    def create_property_contact(
        self, property_id: int, contact_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add a contact to a specific property with comprehensive validation.

        Args:
            property_id: The ID of the property (must be a positive integer)
            contact_data: A dictionary containing the contact's information to be added.
                         Common fields include:
                         - contact_id: ID of the contact to associate (typically required)
                         - role: Role of the contact (e.g., 'buyer', 'seller', 'agent')
                         - is_primary: Whether this is the primary contact

        Returns:
            A dictionary representing the newly added property contact

        Raises:
            ValidationError: If property_id or contact_data is invalid
            NotFoundError: If the property or contact is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            contact = client.property_contacts.create_property_contact(123, {
                "contact_id": 456,
                "role": "buyer",
                "is_primary": True
            })
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            self._validate_property_contact_data(contact_data, "create")

            logger.info(
                f"Creating contact association for property {validated_property_id}",
                extra={"contact_id": contact_data.get("contact_id", "unknown")},
            )
            response = self.post(
                f"/properties/{validated_property_id}/contacts", json_data=contact_data
            )
            result = self._process_response_data(
                response, f"/properties/{validated_property_id}/contacts"
            )

            logger.info(
                f"Successfully created contact association for property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to create contact association for property {property_id}: {str(e)}",
                extra={
                    "contact_data_keys": (
                        list(contact_data.keys())
                        if isinstance(contact_data, dict)
                        else "invalid"
                    )
                },
            )
            raise

    def retrieve_property_contact(
        self, property_id: int, contact_id: int
    ) -> Dict[str, Any]:
        """Retrieve a specific contact for a specific property with validation.

        Args:
            property_id: The ID of the property (must be a positive integer)
            contact_id: The ID of the contact to retrieve (must be a positive integer)

        Returns:
            A dictionary representing the property contact

        Raises:
            ValidationError: If property_id or contact_id is invalid
            NotFoundError: If the property or contact is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            contact = client.property_contacts.retrieve_property_contact(123, 456)
            print(f"Contact role: {contact.get('role', 'N/A')}")
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            validated_contact_id = self._validate_resource_id(contact_id, "contact")

            logger.info(
                f"Retrieving contact {validated_contact_id} for property {validated_property_id}"
            )
            response = self.get(
                f"/properties/{validated_property_id}/contacts/{validated_contact_id}"
            )
            result = self._process_response_data(
                response,
                f"/properties/{validated_property_id}/contacts/{validated_contact_id}",
            )

            logger.info(
                f"Successfully retrieved contact {validated_contact_id} for property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to retrieve contact {contact_id} for property {property_id}: {str(e)}"
            )
            raise

    def update_property_contact(
        self, property_id: int, contact_id: int, contact_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a specific contact for a specific property with validation.

        Args:
            property_id: The ID of the property (must be a positive integer)
            contact_id: The ID of the contact to update (must be a positive integer)
            contact_data: A dictionary containing the fields to update.
                         Fields can include:
                         - role: Contact role
                         - is_primary: Primary contact flag
                         - notes: Contact notes

        Returns:
            A dictionary representing the updated property contact

        Raises:
            ValidationError: If property_id, contact_id, or contact_data is invalid
            NotFoundError: If the property or contact is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            updated_contact = client.property_contacts.update_property_contact(
                123, 456, {"role": "seller", "is_primary": False}
            )
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            validated_contact_id = self._validate_resource_id(contact_id, "contact")
            self._validate_property_contact_data(contact_data, "update")

            logger.info(
                f"Updating contact {validated_contact_id} for property {validated_property_id}",
                extra={"update_fields": list(contact_data.keys())},
            )
            response = self.put(
                f"/properties/{validated_property_id}/contacts/{validated_contact_id}",
                json_data=contact_data,
            )
            result = self._process_response_data(
                response,
                f"/properties/{validated_property_id}/contacts/{validated_contact_id}",
            )

            logger.info(
                f"Successfully updated contact {validated_contact_id} for property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to update contact {contact_id} for property {property_id}: {str(e)}",
                extra={
                    "contact_data_keys": (
                        list(contact_data.keys())
                        if isinstance(contact_data, dict)
                        else "invalid"
                    )
                },
            )
            raise

    def delete_property_contact(
        self, property_id: int, contact_id: int
    ) -> Dict[str, Any]:
        """Remove a contact from a specific property with validation.

        Args:
            property_id: The ID of the property (must be a positive integer)
            contact_id: The ID of the contact to remove (must be a positive integer)

        Returns:
            A dictionary containing the API response (typically empty for successful deletions)

        Raises:
            ValidationError: If property_id or contact_id is invalid
            NotFoundError: If the property or contact is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            result = client.property_contacts.delete_property_contact(123, 456)
            print("Contact removed from property successfully")
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            validated_contact_id = self._validate_resource_id(contact_id, "contact")

            logger.info(
                f"Removing contact {validated_contact_id} from property {validated_property_id}"
            )
            result = self.delete(
                f"/properties/{validated_property_id}/contacts/{validated_contact_id}"
            )

            logger.info(
                f"Successfully removed contact {validated_contact_id} from property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to remove contact {contact_id} from property {property_id}: {str(e)}"
            )
            raise
