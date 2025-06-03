"""Properties client for Open To Close API."""

import logging
from typing import Any, Dict, List, Optional

from .base_client import BaseClient
from .exceptions import ValidationError

logger = logging.getLogger(__name__)


class PropertiesAPI(BaseClient):
    """Client for properties API endpoints.

    This client provides methods to manage properties in the Open To Close platform.
    All methods include comprehensive input validation and error handling.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the properties client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API

        Raises:
            AuthenticationError: If API key is missing or invalid
            ConfigurationError: If configuration is invalid
        """
        super().__init__(api_key=api_key, base_url=base_url)
        logger.debug("Initialized PropertiesAPI client")

    def _validate_property_data(
        self, property_data: Dict[str, Any], operation: str
    ) -> None:
        """Validate property data before sending to API.

        Args:
            property_data: Property data to validate
            operation: Operation type for error context (create/update)

        Raises:
            ValidationError: If property data is invalid
        """
        if not isinstance(property_data, dict):
            raise ValidationError(
                f"Property data for {operation} must be a dictionary, got {type(property_data).__name__}"
            )

        if not property_data:
            raise ValidationError(f"Property data for {operation} cannot be empty")

        # Validate required fields for create operations
        if operation == "create":
            required_fields = ["contract_title"]
            missing_fields = [
                field for field in required_fields if field not in property_data
            ]
            if missing_fields:
                raise ValidationError(
                    f"Property data for {operation} missing required fields: {', '.join(missing_fields)}"
                )

        # Validate contract_title if provided
        if "contract_title" in property_data:
            title = property_data["contract_title"]
            if not isinstance(title, str) or len(title.strip()) == 0:
                raise ValidationError(
                    f"contract_title must be a non-empty string, got: {title}"
                )

        # Validate address fields if provided
        address_fields = [
            "property_address",
            "property_city",
            "property_state",
            "property_zip",
        ]
        for field in address_fields:
            if field in property_data:
                value = property_data[field]
                if not isinstance(value, str) or len(value.strip()) == 0:
                    raise ValidationError(
                        f"{field} must be a non-empty string, got: {value}"
                    )

        # Validate numeric fields if provided
        numeric_fields = ["property_price", "sale_price", "list_price"]
        for field in numeric_fields:
            if field in property_data:
                value = property_data[field]
                if value is not None:
                    try:
                        float_value = float(value)
                        if float_value < 0:
                            raise ValidationError(
                                f"{field} must be non-negative, got: {float_value}"
                            )
                    except (ValueError, TypeError):
                        raise ValidationError(
                            f"{field} must be a number, got {type(value).__name__}: {value}"
                        )

        # Validate status if provided
        if "status" in property_data:
            status = property_data["status"]
            if not isinstance(status, str) or len(status.strip()) == 0:
                raise ValidationError(
                    f"status must be a non-empty string, got: {status}"
                )

        logger.debug(f"Property data validated for {operation} operation")

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

    def list_properties(
        self, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of properties with validation and error handling.

        Args:
            params: Optional dictionary of query parameters for filtering.
                   Supported parameters may include:
                   - limit: Maximum number of properties to return
                   - offset: Number of properties to skip
                   - status: Filter by property status (e.g., 'active', 'closed')
                   - search: Search term for filtering properties

        Returns:
            A list of dictionaries, where each dictionary represents a property

        Raises:
            ValidationError: If parameters are invalid
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            # Get all properties
            properties = client.properties.list_properties()

            # Get properties with custom parameters
            properties = client.properties.list_properties(params={"limit": 50, "status": "active"})
            ```
        """
        try:
            validated_params = self._validate_list_params(params)

            logger.info("Listing properties", extra={"params": validated_params})
            response = self.get("/properties", params=validated_params)
            result = self._process_list_response(response, "/properties")

            logger.info(f"Successfully retrieved {len(result)} properties")
            return result

        except Exception as e:
            logger.error(
                f"Failed to list properties: {str(e)}", extra={"params": params}
            )
            raise

    def create_property(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new property with comprehensive validation.

        Args:
            property_data: A dictionary containing the property's information.
                          Must include contract_title at minimum.
                          Common fields include:
                          - contract_title: Property title (required)
                          - property_address: Street address
                          - property_city: City
                          - property_state: State/province
                          - property_zip: ZIP/postal code
                          - property_price: Property price
                          - status: Property status

        Returns:
            A dictionary representing the newly created property

        Raises:
            ValidationError: If property data is invalid or missing required fields
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            property = client.properties.create_property({
                "contract_title": "Beautiful Family Home",
                "property_address": "123 Main St",
                "property_city": "Anytown",
                "property_state": "CA",
                "property_zip": "12345",
                "property_price": 450000
            })
            ```
        """
        try:
            self._validate_property_data(property_data, "create")

            logger.info(
                "Creating new property",
                extra={"title": property_data.get("contract_title", "Unknown")},
            )
            # Properties POST endpoint requires trailing slash (per docs.opentoclose.com)
            response = self.post("/properties/", json_data=property_data)
            result = self._process_response_data(response, "/properties/")

            property_id = result.get("id")
            logger.info(f"Successfully created property with ID: {property_id}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to create property: {str(e)}",
                extra={
                    "property_data_keys": (
                        list(property_data.keys())
                        if isinstance(property_data, dict)
                        else "invalid"
                    )
                },
            )
            raise

    def retrieve_property(self, property_id: int) -> Dict[str, Any]:
        """Retrieve a specific property by its ID with validation.

        Args:
            property_id: The ID of the property to retrieve (must be a positive integer)

        Returns:
            A dictionary representing the property

        Raises:
            ValidationError: If property_id is invalid
            NotFoundError: If the property is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            property = client.properties.retrieve_property(123)
            print(f"Property address: {property.get('property_address', 'N/A')}")
            ```
        """
        try:
            validated_id = self._validate_resource_id(property_id, "property")

            logger.info(f"Retrieving property with ID: {validated_id}")
            response = self.get(f"/properties/{validated_id}")
            result = self._process_response_data(
                response, f"/properties/{validated_id}"
            )

            logger.info(f"Successfully retrieved property: {validated_id}")
            return result

        except Exception as e:
            logger.error(f"Failed to retrieve property {property_id}: {str(e)}")
            raise

    def update_property(
        self, property_id: int, property_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing property with validation.

        Args:
            property_id: The ID of the property to update (must be a positive integer)
            property_data: A dictionary containing the fields to update.
                          Fields can include any valid property fields like:
                          - contract_title, property_address, property_city, status, etc.

        Returns:
            A dictionary representing the updated property

        Raises:
            ValidationError: If property_id or property_data is invalid
            NotFoundError: If the property is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            updated_property = client.properties.update_property(123, {
                "status": "sold",
                "sale_price": 350000,
                "closing_date": "2024-01-15"
            })
            ```
        """
        try:
            validated_id = self._validate_resource_id(property_id, "property")
            self._validate_property_data(property_data, "update")

            logger.info(
                f"Updating property with ID: {validated_id}",
                extra={"update_fields": list(property_data.keys())},
            )
            response = self.put(f"/properties/{validated_id}", json_data=property_data)
            result = self._process_response_data(
                response, f"/properties/{validated_id}"
            )

            logger.info(f"Successfully updated property: {validated_id}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to update property {property_id}: {str(e)}",
                extra={
                    "property_data_keys": (
                        list(property_data.keys())
                        if isinstance(property_data, dict)
                        else "invalid"
                    )
                },
            )
            raise

    def delete_property(self, property_id: int) -> Dict[str, Any]:
        """Delete a property by its ID with validation.

        Args:
            property_id: The ID of the property to delete (must be a positive integer)

        Returns:
            A dictionary containing the API response (typically empty for successful deletions)

        Raises:
            ValidationError: If property_id is invalid
            NotFoundError: If the property is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            result = client.properties.delete_property(123)
            print("Property deleted successfully")
            ```
        """
        try:
            validated_id = self._validate_resource_id(property_id, "property")

            logger.info(f"Deleting property with ID: {validated_id}")
            result = self.delete(f"/properties/{validated_id}")

            logger.info(f"Successfully deleted property: {validated_id}")
            return result

        except Exception as e:
            logger.error(f"Failed to delete property {property_id}: {str(e)}")
            raise
