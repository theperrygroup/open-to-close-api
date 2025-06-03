"""Property notes client for Open To Close API."""

import logging
from typing import Any, Dict, List, Optional

from .base_client import BaseClient
from .exceptions import ValidationError

logger = logging.getLogger(__name__)


class PropertyNotesAPI(BaseClient):
    """Client for property notes API endpoints.

    This client provides methods to manage notes associated with specific properties
    in the Open To Close platform. All methods include comprehensive input validation
    and error handling.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the property notes client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API

        Raises:
            AuthenticationError: If API key is missing or invalid
            ConfigurationError: If configuration is invalid
        """
        super().__init__(api_key=api_key, base_url=base_url)
        logger.debug("Initialized PropertyNotesAPI client")

    def _validate_property_note_data(
        self, note_data: Dict[str, Any], operation: str
    ) -> None:
        """Validate property note data before sending to API.

        Args:
            note_data: Property note data to validate
            operation: Operation type for error context (create/update)

        Raises:
            ValidationError: If property note data is invalid
        """
        if not isinstance(note_data, dict):
            raise ValidationError(
                f"Property note data for {operation} must be a dictionary, got {type(note_data).__name__}"
            )

        if not note_data:
            raise ValidationError(f"Property note data for {operation} cannot be empty")

        # Validate required fields for create operations
        if operation == "create":
            required_fields = ["content"]
            missing_fields = [
                field for field in required_fields if field not in note_data
            ]
            if missing_fields:
                raise ValidationError(
                    f"Property note data for {operation} missing required fields: {', '.join(missing_fields)}"
                )

        # Validate content if provided
        if "content" in note_data:
            content = note_data["content"]
            if not isinstance(content, str) or len(content.strip()) == 0:
                raise ValidationError(
                    f"content must be a non-empty string, got: {content}"
                )

        # Validate author if provided
        if "author" in note_data:
            author = note_data["author"]
            if not isinstance(author, str) or len(author.strip()) == 0:
                raise ValidationError(
                    f"author must be a non-empty string, got: {author}"
                )

        # Validate priority if provided
        if "priority" in note_data:
            priority = note_data["priority"]
            if not isinstance(priority, str) or len(priority.strip()) == 0:
                raise ValidationError(
                    f"priority must be a non-empty string, got: {priority}"
                )

        # Validate visibility if provided
        if "visibility" in note_data:
            visibility = note_data["visibility"]
            if not isinstance(visibility, str) or len(visibility.strip()) == 0:
                raise ValidationError(
                    f"visibility must be a non-empty string, got: {visibility}"
                )

        # Validate is_private flag if provided
        if "is_private" in note_data:
            is_private = note_data["is_private"]
            if not isinstance(is_private, bool):
                raise ValidationError(
                    f"is_private must be a boolean, got {type(is_private).__name__}: {is_private}"
                )

        # Validate tags if provided
        if "tags" in note_data:
            tags = note_data["tags"]
            if not isinstance(tags, list):
                raise ValidationError(
                    f"tags must be a list, got {type(tags).__name__}: {tags}"
                )

            for i, tag in enumerate(tags):
                if not isinstance(tag, str) or len(tag.strip()) == 0:
                    raise ValidationError(
                        f"tags[{i}] must be a non-empty string, got: {tag}"
                    )

        logger.debug(f"Property note data validated for {operation} operation")

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

        # Validate author filter if provided
        if "author" in validated_params:
            author = validated_params["author"]
            if not isinstance(author, str) or len(author.strip()) == 0:
                raise ValidationError(
                    f"Author filter must be a non-empty string, got: {author}"
                )

        # Validate priority filter if provided
        if "priority" in validated_params:
            priority = validated_params["priority"]
            if not isinstance(priority, str) or len(priority.strip()) == 0:
                raise ValidationError(
                    f"Priority filter must be a non-empty string, got: {priority}"
                )

        logger.debug("List parameters validated", extra={"params": validated_params})
        return validated_params

    def list_property_notes(
        self, property_id: int, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of notes for a specific property with validation and error handling.

        Args:
            property_id: The ID of the property (must be a positive integer)
            params: Optional dictionary of query parameters for filtering.
                   Supported parameters may include:
                   - limit: Maximum number of property notes to return
                   - offset: Number of property notes to skip
                   - author: Filter by note author
                   - priority: Filter by note priority

        Returns:
            A list of dictionaries, where each dictionary represents a property note

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
            # Get all notes for a property
            notes = client.property_notes.list_property_notes(123)

            # Get notes with filtering
            notes = client.property_notes.list_property_notes(
                123, params={"author": "agent", "priority": "high"}
            )
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            validated_params = self._validate_list_params(params)

            logger.info(
                f"Listing notes for property {validated_property_id}",
                extra={"params": validated_params},
            )
            response = self.get(
                f"/properties/{validated_property_id}/notes", params=validated_params
            )
            result = self._process_list_response(
                response, f"/properties/{validated_property_id}/notes"
            )

            logger.info(
                f"Successfully retrieved {len(result)} notes for property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to list notes for property {property_id}: {str(e)}",
                extra={"params": params},
            )
            raise

    def create_property_note(
        self, property_id: int, note_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add a note to a specific property with comprehensive validation.

        Args:
            property_id: The ID of the property (must be a positive integer)
            note_data: A dictionary containing the note's information.
                      Must include content as a required field.
                      Common fields include:
                      - content: Note content (required)
                      - author: Note author
                      - priority: Note priority (e.g., 'low', 'medium', 'high')
                      - visibility: Note visibility
                      - is_private: Whether the note is private
                      - tags: List of tags

        Returns:
            A dictionary representing the newly added property note

        Raises:
            ValidationError: If property_id or note_data is invalid
            NotFoundError: If the property is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            note = client.property_notes.create_property_note(123, {
                "content": "Client showed strong interest in this property.",
                "author": "John Agent",
                "priority": "medium",
                "tags": ["client-interest", "follow-up"]
            })
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            self._validate_property_note_data(note_data, "create")

            logger.info(
                f"Creating note for property {validated_property_id}",
                extra={"content_length": len(note_data.get("content", ""))},
            )
            response = self.post(
                f"/properties/{validated_property_id}/notes", json_data=note_data
            )
            result = self._process_response_data(
                response, f"/properties/{validated_property_id}/notes"
            )

            logger.info(
                f"Successfully created note for property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to create note for property {property_id}: {str(e)}",
                extra={
                    "note_data_keys": (
                        list(note_data.keys())
                        if isinstance(note_data, dict)
                        else "invalid"
                    )
                },
            )
            raise

    def retrieve_property_note(self, property_id: int, note_id: int) -> Dict[str, Any]:
        """Retrieve a specific note for a specific property with validation.

        Args:
            property_id: The ID of the property (must be a positive integer)
            note_id: The ID of the note to retrieve (must be a positive integer)

        Returns:
            A dictionary representing the property note

        Raises:
            ValidationError: If property_id or note_id is invalid
            NotFoundError: If the property or note is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            note = client.property_notes.retrieve_property_note(123, 456)
            print(f"Note content: {note.get('content', 'N/A')}")
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            validated_note_id = self._validate_resource_id(note_id, "note")

            logger.info(
                f"Retrieving note {validated_note_id} for property {validated_property_id}"
            )
            response = self.get(
                f"/properties/{validated_property_id}/notes/{validated_note_id}"
            )
            result = self._process_response_data(
                response,
                f"/properties/{validated_property_id}/notes/{validated_note_id}",
            )

            logger.info(
                f"Successfully retrieved note {validated_note_id} for property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to retrieve note {note_id} for property {property_id}: {str(e)}"
            )
            raise

    def update_property_note(
        self, property_id: int, note_id: int, note_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a specific note for a specific property with validation.

        Args:
            property_id: The ID of the property (must be a positive integer)
            note_id: The ID of the note to update (must be a positive integer)
            note_data: A dictionary containing the fields to update.
                      Fields can include:
                      - content: Note content
                      - author: Note author
                      - priority: Note priority
                      - visibility: Note visibility
                      - is_private: Whether the note is private

        Returns:
            A dictionary representing the updated property note

        Raises:
            ValidationError: If property_id, note_id, or note_data is invalid
            NotFoundError: If the property or note is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            updated_note = client.property_notes.update_property_note(
                123, 456, {"priority": "high", "is_private": True}
            )
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            validated_note_id = self._validate_resource_id(note_id, "note")
            self._validate_property_note_data(note_data, "update")

            logger.info(
                f"Updating note {validated_note_id} for property {validated_property_id}",
                extra={"update_fields": list(note_data.keys())},
            )
            response = self.put(
                f"/properties/{validated_property_id}/notes/{validated_note_id}",
                json_data=note_data,
            )
            result = self._process_response_data(
                response,
                f"/properties/{validated_property_id}/notes/{validated_note_id}",
            )

            logger.info(
                f"Successfully updated note {validated_note_id} for property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to update note {note_id} for property {property_id}: {str(e)}",
                extra={
                    "note_data_keys": (
                        list(note_data.keys())
                        if isinstance(note_data, dict)
                        else "invalid"
                    )
                },
            )
            raise

    def delete_property_note(self, property_id: int, note_id: int) -> Dict[str, Any]:
        """Remove a note from a specific property with validation.

        Args:
            property_id: The ID of the property (must be a positive integer)
            note_id: The ID of the note to remove (must be a positive integer)

        Returns:
            A dictionary containing the API response (typically empty for successful deletions)

        Raises:
            ValidationError: If property_id or note_id is invalid
            NotFoundError: If the property or note is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            result = client.property_notes.delete_property_note(123, 456)
            print("Note removed from property successfully")
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            validated_note_id = self._validate_resource_id(note_id, "note")

            logger.info(
                f"Removing note {validated_note_id} from property {validated_property_id}"
            )
            result = self.delete(
                f"/properties/{validated_property_id}/notes/{validated_note_id}"
            )

            logger.info(
                f"Successfully removed note {validated_note_id} from property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to remove note {note_id} from property {property_id}: {str(e)}"
            )
            raise
