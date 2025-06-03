"""Property tasks client for Open To Close API."""

import logging
from typing import Any, Dict, List, Optional

from .base_client import BaseClient
from .exceptions import ValidationError

logger = logging.getLogger(__name__)


class PropertyTasksAPI(BaseClient):
    """Client for property tasks API endpoints.

    This client provides methods to manage tasks associated with specific properties
    in the Open To Close platform. All methods include comprehensive input validation
    and error handling.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the property tasks client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API

        Raises:
            AuthenticationError: If API key is missing or invalid
            ConfigurationError: If configuration is invalid
        """
        super().__init__(api_key=api_key, base_url=base_url)
        logger.debug("Initialized PropertyTasksAPI client")

    def _validate_property_task_data(
        self, task_data: Dict[str, Any], operation: str
    ) -> None:
        """Validate property task data before sending to API.

        Args:
            task_data: Property task data to validate
            operation: Operation type for error context (create/update)

        Raises:
            ValidationError: If property task data is invalid
        """
        if not isinstance(task_data, dict):
            raise ValidationError(
                f"Property task data for {operation} must be a dictionary, got {type(task_data).__name__}"
            )

        if not task_data:
            raise ValidationError(f"Property task data for {operation} cannot be empty")

        # Validate required fields for create operations
        if operation == "create":
            required_fields = ["title"]
            missing_fields = [
                field for field in required_fields if field not in task_data
            ]
            if missing_fields:
                raise ValidationError(
                    f"Property task data for {operation} missing required fields: {', '.join(missing_fields)}"
                )

        # Validate title if provided
        if "title" in task_data:
            title = task_data["title"]
            if not isinstance(title, str) or len(title.strip()) == 0:
                raise ValidationError(f"title must be a non-empty string, got: {title}")

        # Validate description if provided
        if "description" in task_data:
            description = task_data["description"]
            if not isinstance(description, str):
                raise ValidationError(
                    f"description must be a string, got {type(description).__name__}: {description}"
                )

        # Validate status if provided
        if "status" in task_data:
            status = task_data["status"]
            if not isinstance(status, str) or len(status.strip()) == 0:
                raise ValidationError(
                    f"status must be a non-empty string, got: {status}"
                )

        # Validate priority if provided
        if "priority" in task_data:
            priority = task_data["priority"]
            if not isinstance(priority, str) or len(priority.strip()) == 0:
                raise ValidationError(
                    f"priority must be a non-empty string, got: {priority}"
                )

        # Validate assignee if provided
        if "assignee" in task_data:
            assignee = task_data["assignee"]
            if not isinstance(assignee, str) or len(assignee.strip()) == 0:
                raise ValidationError(
                    f"assignee must be a non-empty string, got: {assignee}"
                )

        # Validate assignee_id if provided
        if "assignee_id" in task_data:
            assignee_id = task_data["assignee_id"]
            try:
                assignee_id_int = int(assignee_id)
                if assignee_id_int <= 0:
                    raise ValidationError(
                        f"assignee_id must be a positive integer, got {assignee_id_int}"
                    )
            except (ValueError, TypeError):
                raise ValidationError(
                    f"assignee_id must be an integer, got {type(assignee_id).__name__}: {assignee_id}"
                )

        # Validate due_date if provided (basic validation - should be a string that can be parsed as date)
        if "due_date" in task_data:
            due_date = task_data["due_date"]
            if not isinstance(due_date, str) or len(due_date.strip()) == 0:
                raise ValidationError(
                    f"due_date must be a non-empty string, got: {due_date}"
                )

        # Validate is_completed flag if provided
        if "is_completed" in task_data:
            is_completed = task_data["is_completed"]
            if not isinstance(is_completed, bool):
                raise ValidationError(
                    f"is_completed must be a boolean, got {type(is_completed).__name__}: {is_completed}"
                )

        logger.debug(f"Property task data validated for {operation} operation")

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

        # Validate priority filter if provided
        if "priority" in validated_params:
            priority = validated_params["priority"]
            if not isinstance(priority, str) or len(priority.strip()) == 0:
                raise ValidationError(
                    f"Priority filter must be a non-empty string, got: {priority}"
                )

        logger.debug("List parameters validated", extra={"params": validated_params})
        return validated_params

    def list_property_tasks(
        self, property_id: int, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of tasks for a specific property with validation and error handling.

        Args:
            property_id: The ID of the property (must be a positive integer)
            params: Optional dictionary of query parameters for filtering.
                   Supported parameters may include:
                   - limit: Maximum number of property tasks to return
                   - offset: Number of property tasks to skip
                   - status: Filter by task status (e.g., 'pending', 'completed', 'in_progress')
                   - priority: Filter by task priority

        Returns:
            A list of dictionaries, where each dictionary represents a property task

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
            # Get all tasks for a property
            tasks = client.property_tasks.list_property_tasks(123)

            # Get tasks with filtering
            tasks = client.property_tasks.list_property_tasks(
                123, params={"status": "pending", "priority": "high"}
            )
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            validated_params = self._validate_list_params(params)

            logger.info(
                f"Listing tasks for property {validated_property_id}",
                extra={"params": validated_params},
            )
            response = self.get(
                f"/properties/{validated_property_id}/tasks", params=validated_params
            )
            result = self._process_list_response(
                response, f"/properties/{validated_property_id}/tasks"
            )

            logger.info(
                f"Successfully retrieved {len(result)} tasks for property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to list tasks for property {property_id}: {str(e)}",
                extra={"params": params},
            )
            raise

    def create_property_task(
        self, property_id: int, task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add a task to a specific property with comprehensive validation.

        Args:
            property_id: The ID of the property (must be a positive integer)
            task_data: A dictionary containing the task's information.
                      Must include title as a required field.
                      Common fields include:
                      - title: Task title (required)
                      - description: Task description
                      - status: Task status
                      - priority: Task priority
                      - assignee: Task assignee name
                      - assignee_id: Task assignee ID
                      - due_date: Task due date

        Returns:
            A dictionary representing the newly added property task

        Raises:
            ValidationError: If property_id or task_data is invalid
            NotFoundError: If the property is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            task = client.property_tasks.create_property_task(123, {
                "title": "Schedule inspection",
                "description": "Arrange property inspection with buyer.",
                "due_date": "2024-01-15",
                "priority": "high"
            })
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            self._validate_property_task_data(task_data, "create")

            logger.info(
                f"Creating task for property {validated_property_id}",
                extra={"title": task_data.get("title", "unknown")},
            )
            response = self.post(
                f"/properties/{validated_property_id}/tasks", json_data=task_data
            )
            result = self._process_response_data(
                response, f"/properties/{validated_property_id}/tasks"
            )

            logger.info(
                f"Successfully created task for property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to create task for property {property_id}: {str(e)}",
                extra={
                    "task_data_keys": (
                        list(task_data.keys())
                        if isinstance(task_data, dict)
                        else "invalid"
                    )
                },
            )
            raise

    def retrieve_property_task(self, property_id: int, task_id: int) -> Dict[str, Any]:
        """Retrieve a specific task for a specific property with validation.

        Args:
            property_id: The ID of the property (must be a positive integer)
            task_id: The ID of the task to retrieve (must be a positive integer)

        Returns:
            A dictionary representing the property task

        Raises:
            ValidationError: If property_id or task_id is invalid
            NotFoundError: If the property or task is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            task = client.property_tasks.retrieve_property_task(123, 456)
            print(f"Task title: {task.get('title', 'N/A')}")
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            validated_task_id = self._validate_resource_id(task_id, "task")

            logger.info(
                f"Retrieving task {validated_task_id} for property {validated_property_id}"
            )
            response = self.get(
                f"/properties/{validated_property_id}/tasks/{validated_task_id}"
            )
            result = self._process_response_data(
                response,
                f"/properties/{validated_property_id}/tasks/{validated_task_id}",
            )

            logger.info(
                f"Successfully retrieved task {validated_task_id} for property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to retrieve task {task_id} for property {property_id}: {str(e)}"
            )
            raise

    def update_property_task(
        self, property_id: int, task_id: int, task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a specific task for a specific property with validation.

        Args:
            property_id: The ID of the property (must be a positive integer)
            task_id: The ID of the task to update (must be a positive integer)
            task_data: A dictionary containing the fields to update.
                      Fields can include:
                      - title: Task title
                      - description: Task description
                      - status: Task status
                      - priority: Task priority
                      - assignee: Task assignee
                      - due_date: Task due date

        Returns:
            A dictionary representing the updated property task

        Raises:
            ValidationError: If property_id, task_id, or task_data is invalid
            NotFoundError: If the property or task is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            updated_task = client.property_tasks.update_property_task(
                123, 456, {"status": "completed", "priority": "low"}
            )
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            validated_task_id = self._validate_resource_id(task_id, "task")
            self._validate_property_task_data(task_data, "update")

            logger.info(
                f"Updating task {validated_task_id} for property {validated_property_id}",
                extra={"update_fields": list(task_data.keys())},
            )
            response = self.put(
                f"/properties/{validated_property_id}/tasks/{validated_task_id}",
                json_data=task_data,
            )
            result = self._process_response_data(
                response,
                f"/properties/{validated_property_id}/tasks/{validated_task_id}",
            )

            logger.info(
                f"Successfully updated task {validated_task_id} for property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to update task {task_id} for property {property_id}: {str(e)}",
                extra={
                    "task_data_keys": (
                        list(task_data.keys())
                        if isinstance(task_data, dict)
                        else "invalid"
                    )
                },
            )
            raise

    def delete_property_task(self, property_id: int, task_id: int) -> Dict[str, Any]:
        """Remove a task from a specific property with validation.

        Args:
            property_id: The ID of the property (must be a positive integer)
            task_id: The ID of the task to remove (must be a positive integer)

        Returns:
            A dictionary containing the API response (typically empty for successful deletions)

        Raises:
            ValidationError: If property_id or task_id is invalid
            NotFoundError: If the property or task is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            result = client.property_tasks.delete_property_task(123, 456)
            print("Task removed from property successfully")
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            validated_task_id = self._validate_resource_id(task_id, "task")

            logger.info(
                f"Removing task {validated_task_id} from property {validated_property_id}"
            )
            result = self.delete(
                f"/properties/{validated_property_id}/tasks/{validated_task_id}"
            )

            logger.info(
                f"Successfully removed task {validated_task_id} from property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to remove task {task_id} from property {property_id}: {str(e)}"
            )
            raise
