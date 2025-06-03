"""Tags client for Open To Close API."""

import logging
from typing import Any, Dict, List, Optional

from .base_client import BaseClient
from .exceptions import ValidationError

logger = logging.getLogger(__name__)


class TagsAPI(BaseClient):
    """Client for tags API endpoints.

    This client provides methods to manage tags in the Open To Close platform.
    All methods include comprehensive input validation and error handling.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the tags client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API

        Raises:
            AuthenticationError: If API key is missing or invalid
            ConfigurationError: If configuration is invalid
        """
        super().__init__(api_key=api_key, base_url=base_url)
        logger.debug("Initialized TagsAPI client")

    def _validate_tag_data(self, tag_data: Dict[str, Any], operation: str) -> None:
        """Validate tag data before sending to API.

        Args:
            tag_data: Tag data to validate
            operation: Operation type for error context (create/update)

        Raises:
            ValidationError: If tag data is invalid
        """
        if not isinstance(tag_data, dict):
            raise ValidationError(
                f"Tag data for {operation} must be a dictionary, got {type(tag_data).__name__}"
            )

        if not tag_data:
            raise ValidationError(f"Tag data for {operation} cannot be empty")

        # Validate required fields for create operations
        if operation == "create":
            required_fields = ["name"]
            missing_fields = [
                field for field in required_fields if field not in tag_data
            ]
            if missing_fields:
                raise ValidationError(
                    f"Tag data for {operation} missing required fields: {', '.join(missing_fields)}"
                )

        # Validate name if provided
        if "name" in tag_data:
            name = tag_data["name"]
            if not isinstance(name, str) or len(name.strip()) == 0:
                raise ValidationError(f"name must be a non-empty string, got: {name}")

        # Validate color if provided (should be a hex color code)
        if "color" in tag_data:
            color = tag_data["color"]
            if not isinstance(color, str) or len(color.strip()) == 0:
                raise ValidationError(f"color must be a non-empty string, got: {color}")
            # Basic hex color validation
            if not color.startswith("#") or len(color) not in [4, 7]:  # #RGB or #RRGGBB
                raise ValidationError(
                    f"color must be a valid hex color code (e.g., #FF0000), got: {color}"
                )

        # Validate description if provided
        if "description" in tag_data:
            description = tag_data["description"]
            if not isinstance(description, str):
                raise ValidationError(
                    f"description must be a string, got {type(description).__name__}: {description}"
                )

        # Validate category if provided
        if "category" in tag_data:
            category = tag_data["category"]
            if not isinstance(category, str) or len(category.strip()) == 0:
                raise ValidationError(
                    f"category must be a non-empty string, got: {category}"
                )

        # Validate is_active flag if provided
        if "is_active" in tag_data:
            is_active = tag_data["is_active"]
            if not isinstance(is_active, bool):
                raise ValidationError(
                    f"is_active must be a boolean, got {type(is_active).__name__}: {is_active}"
                )

        # Validate sort_order if provided
        if "sort_order" in tag_data:
            sort_order = tag_data["sort_order"]
            try:
                sort_order_int = int(sort_order)
                if sort_order_int < 0:
                    raise ValidationError(
                        f"sort_order must be non-negative, got {sort_order_int}"
                    )
            except (ValueError, TypeError):
                raise ValidationError(
                    f"sort_order must be an integer, got {type(sort_order).__name__}: {sort_order}"
                )

        logger.debug(f"Tag data validated for {operation} operation")

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

        # Validate category filter if provided
        if "category" in validated_params:
            category = validated_params["category"]
            if not isinstance(category, str) or len(category.strip()) == 0:
                raise ValidationError(
                    f"Category filter must be a non-empty string, got: {category}"
                )

        # Validate is_active filter if provided
        if "is_active" in validated_params:
            is_active = validated_params["is_active"]
            if not isinstance(is_active, bool):
                raise ValidationError(
                    f"is_active filter must be a boolean, got {type(is_active).__name__}: {is_active}"
                )

        logger.debug("List parameters validated", extra={"params": validated_params})
        return validated_params

    def list_tags(
        self, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of tags with validation and error handling.

        Args:
            params: Optional dictionary of query parameters for filtering.
                   Supported parameters may include:
                   - limit: Maximum number of tags to return
                   - offset: Number of tags to skip
                   - category: Filter by tag category
                   - is_active: Filter by active status

        Returns:
            A list of dictionaries, where each dictionary represents a tag

        Raises:
            ValidationError: If parameters are invalid
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            # Get all tags
            tags = client.tags.list_tags()

            # Get tags with custom parameters
            tags = client.tags.list_tags(params={"limit": 50, "category": "priority"})
            ```
        """
        try:
            validated_params = self._validate_list_params(params)

            logger.info("Listing tags", extra={"params": validated_params})
            response = self.get("/tags", params=validated_params)
            result = self._process_list_response(response, "/tags")

            logger.info(f"Successfully retrieved {len(result)} tags")
            return result

        except Exception as e:
            logger.error(f"Failed to list tags: {str(e)}", extra={"params": params})
            raise

    def create_tag(self, tag_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new tag with comprehensive validation.

        Args:
            tag_data: A dictionary containing the tag's information.
                     Must include name as a required field.
                     Common fields include:
                     - name: Tag name (required)
                     - color: Tag color as hex code (e.g., #FF0000)
                     - description: Tag description
                     - category: Tag category
                     - is_active: Whether the tag is active
                     - sort_order: Sort order for the tag

        Returns:
            A dictionary representing the newly created tag

        Raises:
            ValidationError: If tag_data is invalid or missing required fields
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            tag = client.tags.create_tag({
                "name": "High Priority",
                "color": "#FF0000",
                "description": "High priority items",
                "category": "priority"
            })
            ```
        """
        try:
            self._validate_tag_data(tag_data, "create")

            logger.info(
                "Creating new tag", extra={"name": tag_data.get("name", "unknown")}
            )
            response = self.post("/tags", json_data=tag_data)
            result = self._process_response_data(response, "/tags")

            tag_id = result.get("id")
            logger.info(f"Successfully created tag with ID: {tag_id}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to create tag: {str(e)}",
                extra={
                    "tag_data_keys": (
                        list(tag_data.keys())
                        if isinstance(tag_data, dict)
                        else "invalid"
                    )
                },
            )
            raise

    def retrieve_tag(self, tag_id: int) -> Dict[str, Any]:
        """Retrieve a specific tag by its ID with validation.

        Args:
            tag_id: The ID of the tag to retrieve (must be a positive integer)

        Returns:
            A dictionary representing the tag

        Raises:
            ValidationError: If tag_id is invalid
            NotFoundError: If the tag is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            tag = client.tags.retrieve_tag(123)
            print(f"Tag name: {tag.get('name', 'N/A')}")
            ```
        """
        try:
            validated_id = self._validate_resource_id(tag_id, "tag")

            logger.info(f"Retrieving tag with ID: {validated_id}")
            response = self.get(f"/tags/{validated_id}")
            result = self._process_response_data(response, f"/tags/{validated_id}")

            logger.info(f"Successfully retrieved tag: {validated_id}")
            return result

        except Exception as e:
            logger.error(f"Failed to retrieve tag {tag_id}: {str(e)}")
            raise

    def update_tag(self, tag_id: int, tag_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing tag with validation.

        Args:
            tag_id: The ID of the tag to update (must be a positive integer)
            tag_data: A dictionary containing the fields to update.
                     Fields can include any valid tag fields like:
                     - name, color, description, category, is_active, sort_order, etc.

        Returns:
            A dictionary representing the updated tag

        Raises:
            ValidationError: If tag_id or tag_data is invalid
            NotFoundError: If the tag is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            updated_tag = client.tags.update_tag(123, {
                "name": "Updated Priority",
                "color": "#00FF00",
                "is_active": True
            })
            ```
        """
        try:
            validated_id = self._validate_resource_id(tag_id, "tag")
            self._validate_tag_data(tag_data, "update")

            logger.info(
                f"Updating tag with ID: {validated_id}",
                extra={"update_fields": list(tag_data.keys())},
            )
            response = self.put(f"/tags/{validated_id}", json_data=tag_data)
            result = self._process_response_data(response, f"/tags/{validated_id}")

            logger.info(f"Successfully updated tag: {validated_id}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to update tag {tag_id}: {str(e)}",
                extra={
                    "tag_data_keys": (
                        list(tag_data.keys())
                        if isinstance(tag_data, dict)
                        else "invalid"
                    )
                },
            )
            raise

    def delete_tag(self, tag_id: int) -> Dict[str, Any]:
        """Delete a tag by its ID with validation.

        Args:
            tag_id: The ID of the tag to delete (must be a positive integer)

        Returns:
            A dictionary containing the API response (typically empty for successful deletions)

        Raises:
            ValidationError: If tag_id is invalid
            NotFoundError: If the tag is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            result = client.tags.delete_tag(123)
            print("Tag deleted successfully")
            ```
        """
        try:
            validated_id = self._validate_resource_id(tag_id, "tag")

            logger.info(f"Deleting tag with ID: {validated_id}")
            result = self.delete(f"/tags/{validated_id}")

            logger.info(f"Successfully deleted tag: {validated_id}")
            return result

        except Exception as e:
            logger.error(f"Failed to delete tag {tag_id}: {str(e)}")
            raise
