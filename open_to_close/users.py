"""Users client for Open To Close API."""

import logging
from typing import Any, Dict, List, Optional

from .base_client import BaseClient
from .exceptions import ValidationError

logger = logging.getLogger(__name__)


class UsersAPI(BaseClient):
    """Client for users API endpoints.

    This client provides methods to manage users in the Open To Close platform.
    All methods include comprehensive input validation and error handling.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the users client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API

        Raises:
            AuthenticationError: If API key is missing or invalid
            ConfigurationError: If configuration is invalid
        """
        super().__init__(api_key=api_key, base_url=base_url)
        logger.debug("Initialized UsersAPI client")

    def _validate_user_data(self, user_data: Dict[str, Any], operation: str) -> None:
        """Validate user data before sending to API.

        Args:
            user_data: User data to validate
            operation: Operation type for error context (create/update)

        Raises:
            ValidationError: If user data is invalid
        """
        if not isinstance(user_data, dict):
            raise ValidationError(
                f"User data for {operation} must be a dictionary, got {type(user_data).__name__}"
            )

        if not user_data:
            raise ValidationError(f"User data for {operation} cannot be empty")

        # Validate required fields for create operations
        if operation == "create":
            required_fields = ["email"]
            missing_fields = [
                field for field in required_fields if field not in user_data
            ]
            if missing_fields:
                raise ValidationError(
                    f"User data for {operation} missing required fields: {', '.join(missing_fields)}"
                )

        # Validate email format if provided
        if "email" in user_data:
            email = user_data["email"]
            if not isinstance(email, str) or "@" not in email:
                raise ValidationError(f"Invalid email format: {email}")

        # Validate phone format if provided
        if "phone" in user_data:
            phone = user_data["phone"]
            if not isinstance(phone, str) or len(phone.strip()) == 0:
                raise ValidationError(f"Phone must be a non-empty string, got: {phone}")

        # Validate name fields if provided
        for name_field in ["name", "first_name", "last_name"]:
            if name_field in user_data:
                name_value = user_data[name_field]
                if not isinstance(name_value, str) or len(name_value.strip()) == 0:
                    raise ValidationError(
                        f"{name_field} must be a non-empty string, got: {name_value}"
                    )

        # Validate role if provided
        if "role" in user_data:
            role = user_data["role"]
            if not isinstance(role, str) or len(role.strip()) == 0:
                raise ValidationError(f"role must be a non-empty string, got: {role}")

        # Validate status if provided
        if "status" in user_data:
            status = user_data["status"]
            if not isinstance(status, str) or len(status.strip()) == 0:
                raise ValidationError(
                    f"status must be a non-empty string, got: {status}"
                )

        logger.debug(f"User data validated for {operation} operation")

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

    def list_users(
        self, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of users with validation and error handling.

        Args:
            params: Optional dictionary of query parameters for filtering.
                   Supported parameters may include:
                   - limit: Maximum number of users to return
                   - offset: Number of users to skip
                   - role: Filter by user role
                   - status: Filter by user status

        Returns:
            A list of dictionaries, where each dictionary represents a user

        Raises:
            ValidationError: If parameters are invalid
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            # Get all users
            users = client.users.list_users()

            # Get users with custom parameters
            users = client.users.list_users(params={"limit": 50, "role": "admin"})
            ```
        """
        try:
            validated_params = self._validate_list_params(params)

            logger.info("Listing users", extra={"params": validated_params})
            response = self.get("/users", params=validated_params)
            result = self._process_list_response(response, "/users")

            logger.info(f"Successfully retrieved {len(result)} users")
            return result

        except Exception as e:
            logger.error(f"Failed to list users: {str(e)}", extra={"params": params})
            raise

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user with comprehensive validation.

        Args:
            user_data: A dictionary containing the user's information.
                      Must include email as a required field.
                      Common fields include:
                      - email: User email address (required)
                      - phone: User phone number
                      - name: Full name (or use first_name/last_name)
                      - first_name: First name
                      - last_name: Last name
                      - role: User role (e.g., 'admin', 'agent', 'user')
                      - status: User status

        Returns:
            A dictionary representing the newly created user

        Raises:
            ValidationError: If user data is invalid or missing required fields
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            user = client.users.create_user({
                "email": "user@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "role": "agent"
            })
            ```
        """
        try:
            self._validate_user_data(user_data, "create")

            logger.info(
                "Creating new user", extra={"email": user_data.get("email", "unknown")}
            )
            response = self.post("/users", json_data=user_data)
            result = self._process_response_data(response, "/users")

            user_id = result.get("id")
            logger.info(f"Successfully created user with ID: {user_id}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to create user: {str(e)}",
                extra={
                    "user_data_keys": (
                        list(user_data.keys())
                        if isinstance(user_data, dict)
                        else "invalid"
                    )
                },
            )
            raise

    def retrieve_user(self, user_id: int) -> Dict[str, Any]:
        """Retrieve a specific user by their ID with validation.

        Args:
            user_id: The ID of the user to retrieve (must be a positive integer)

        Returns:
            A dictionary representing the user

        Raises:
            ValidationError: If user_id is invalid
            NotFoundError: If the user is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            user = client.users.retrieve_user(123)
            print(f"User email: {user.get('email', 'N/A')}")
            ```
        """
        try:
            validated_id = self._validate_resource_id(user_id, "user")

            logger.info(f"Retrieving user with ID: {validated_id}")
            response = self.get(f"/users/{validated_id}")
            result = self._process_response_data(response, f"/users/{validated_id}")

            logger.info(f"Successfully retrieved user: {validated_id}")
            return result

        except Exception as e:
            logger.error(f"Failed to retrieve user {user_id}: {str(e)}")
            raise

    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing user with validation.

        Args:
            user_id: The ID of the user to update (must be a positive integer)
            user_data: A dictionary containing the fields to update.
                      Fields can include any valid user fields like:
                      - email, phone, name, first_name, last_name, role, status, etc.

        Returns:
            A dictionary representing the updated user

        Raises:
            ValidationError: If user_id or user_data is invalid
            NotFoundError: If the user is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            updated_user = client.users.update_user(123, {
                "first_name": "Jane",
                "last_name": "Smith",
                "role": "admin"
            })
            ```
        """
        try:
            validated_id = self._validate_resource_id(user_id, "user")
            self._validate_user_data(user_data, "update")

            logger.info(
                f"Updating user with ID: {validated_id}",
                extra={"update_fields": list(user_data.keys())},
            )
            response = self.put(f"/users/{validated_id}", json_data=user_data)
            result = self._process_response_data(response, f"/users/{validated_id}")

            logger.info(f"Successfully updated user: {validated_id}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to update user {user_id}: {str(e)}",
                extra={
                    "user_data_keys": (
                        list(user_data.keys())
                        if isinstance(user_data, dict)
                        else "invalid"
                    )
                },
            )
            raise

    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """Delete a user by their ID with validation.

        Args:
            user_id: The ID of the user to delete (must be a positive integer)

        Returns:
            A dictionary containing the API response (typically empty for successful deletions)

        Raises:
            ValidationError: If user_id is invalid
            NotFoundError: If the user is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            result = client.users.delete_user(123)
            print("User deleted successfully")
            ```
        """
        try:
            validated_id = self._validate_resource_id(user_id, "user")

            logger.info(f"Deleting user with ID: {validated_id}")
            result = self.delete(f"/users/{validated_id}")

            logger.info(f"Successfully deleted user: {validated_id}")
            return result

        except Exception as e:
            logger.error(f"Failed to delete user {user_id}: {str(e)}")
            raise
