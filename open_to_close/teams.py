"""Teams client for Open To Close API."""

import logging
from typing import Any, Dict, List, Optional

from .base_client import BaseClient
from .exceptions import ValidationError

logger = logging.getLogger(__name__)


class TeamsAPI(BaseClient):
    """Client for teams API endpoints.

    This client provides methods to manage teams in the Open To Close platform.
    All methods include comprehensive input validation and error handling.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the teams client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API

        Raises:
            AuthenticationError: If API key is missing or invalid
            ConfigurationError: If configuration is invalid
        """
        super().__init__(api_key=api_key, base_url=base_url)
        logger.debug("Initialized TeamsAPI client")

    def _validate_team_data(self, team_data: Dict[str, Any], operation: str) -> None:
        """Validate team data before sending to API.

        Args:
            team_data: Team data to validate
            operation: Operation type for error context (create/update)

        Raises:
            ValidationError: If team data is invalid
        """
        if not isinstance(team_data, dict):
            raise ValidationError(
                f"Team data for {operation} must be a dictionary, got {type(team_data).__name__}"
            )

        if not team_data:
            raise ValidationError(f"Team data for {operation} cannot be empty")

        # Validate required fields for create operations
        if operation == "create":
            required_fields = ["name"]
            missing_fields = [
                field for field in required_fields if field not in team_data
            ]
            if missing_fields:
                raise ValidationError(
                    f"Team data for {operation} missing required fields: {', '.join(missing_fields)}"
                )

        # Validate name if provided
        if "name" in team_data:
            name = team_data["name"]
            if not isinstance(name, str) or len(name.strip()) == 0:
                raise ValidationError(f"name must be a non-empty string, got: {name}")

        # Validate description if provided
        if "description" in team_data:
            description = team_data["description"]
            if not isinstance(description, str):
                raise ValidationError(
                    f"description must be a string, got {type(description).__name__}: {description}"
                )

        # Validate status if provided
        if "status" in team_data:
            status = team_data["status"]
            if not isinstance(status, str) or len(status.strip()) == 0:
                raise ValidationError(
                    f"status must be a non-empty string, got: {status}"
                )

        # Validate members list if provided
        if "members" in team_data:
            members = team_data["members"]
            if not isinstance(members, list):
                raise ValidationError(
                    f"members must be a list, got {type(members).__name__}: {members}"
                )

            # Validate each member
            for i, member in enumerate(members):
                if not isinstance(member, (int, dict)):
                    raise ValidationError(
                        f"members[{i}] must be an integer (user ID) or dictionary, got {type(member).__name__}"
                    )

                if isinstance(member, dict) and "user_id" in member:
                    user_id = member["user_id"]
                    try:
                        int(user_id)
                    except (ValueError, TypeError):
                        raise ValidationError(
                            f"members[{i}].user_id must be an integer, got {type(user_id).__name__}: {user_id}"
                        )

        logger.debug(f"Team data validated for {operation} operation")

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

    def list_teams(
        self, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of teams with validation and error handling.

        Args:
            params: Optional dictionary of query parameters for filtering.
                   Supported parameters may include:
                   - limit: Maximum number of teams to return
                   - offset: Number of teams to skip
                   - status: Filter by team status

        Returns:
            A list of dictionaries, where each dictionary represents a team

        Raises:
            ValidationError: If parameters are invalid
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            # Get all teams
            teams = client.teams.list_teams()

            # Get teams with custom parameters
            teams = client.teams.list_teams(params={"limit": 50, "status": "active"})
            ```
        """
        try:
            validated_params = self._validate_list_params(params)

            logger.info("Listing teams", extra={"params": validated_params})
            response = self.get("/teams", params=validated_params)
            result = self._process_list_response(response, "/teams")

            logger.info(f"Successfully retrieved {len(result)} teams")
            return result

        except Exception as e:
            logger.error(f"Failed to list teams: {str(e)}", extra={"params": params})
            raise

    def create_team(self, team_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new team with comprehensive validation.

        Args:
            team_data: A dictionary containing the team's information.
                      Must include name as a required field.
                      Common fields include:
                      - name: Team name (required)
                      - description: Team description
                      - status: Team status
                      - members: List of team members (user IDs or member objects)

        Returns:
            A dictionary representing the newly created team

        Raises:
            ValidationError: If team data is invalid or missing required fields
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            team = client.teams.create_team({
                "name": "Sales Team Alpha",
                "description": "Primary sales team for the East region",
                "status": "active",
                "members": [123, 456, 789]  # User IDs
            })
            ```
        """
        try:
            self._validate_team_data(team_data, "create")

            logger.info(
                "Creating new team", extra={"name": team_data.get("name", "unknown")}
            )
            response = self.post("/teams", json_data=team_data)
            result = self._process_response_data(response, "/teams")

            team_id = result.get("id")
            logger.info(f"Successfully created team with ID: {team_id}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to create team: {str(e)}",
                extra={
                    "team_data_keys": (
                        list(team_data.keys())
                        if isinstance(team_data, dict)
                        else "invalid"
                    )
                },
            )
            raise

    def retrieve_team(self, team_id: int) -> Dict[str, Any]:
        """Retrieve a specific team by its ID with validation.

        Args:
            team_id: The ID of the team to retrieve (must be a positive integer)

        Returns:
            A dictionary representing the team

        Raises:
            ValidationError: If team_id is invalid
            NotFoundError: If the team is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            team = client.teams.retrieve_team(123)
            print(f"Team name: {team.get('name', 'N/A')}")
            ```
        """
        try:
            validated_id = self._validate_resource_id(team_id, "team")

            logger.info(f"Retrieving team with ID: {validated_id}")
            response = self.get(f"/teams/{validated_id}")
            result = self._process_response_data(response, f"/teams/{validated_id}")

            logger.info(f"Successfully retrieved team: {validated_id}")
            return result

        except Exception as e:
            logger.error(f"Failed to retrieve team {team_id}: {str(e)}")
            raise

    def update_team(self, team_id: int, team_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing team with validation.

        Args:
            team_id: The ID of the team to update (must be a positive integer)
            team_data: A dictionary containing the fields to update.
                      Fields can include any valid team fields like:
                      - name, description, status, members, etc.

        Returns:
            A dictionary representing the updated team

        Raises:
            ValidationError: If team_id or team_data is invalid
            NotFoundError: If the team is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            updated_team = client.teams.update_team(123, {
                "name": "Updated Sales Team Alpha",
                "description": "Updated description",
                "status": "active"
            })
            ```
        """
        try:
            validated_id = self._validate_resource_id(team_id, "team")
            self._validate_team_data(team_data, "update")

            logger.info(
                f"Updating team with ID: {validated_id}",
                extra={"update_fields": list(team_data.keys())},
            )
            response = self.put(f"/teams/{validated_id}", json_data=team_data)
            result = self._process_response_data(response, f"/teams/{validated_id}")

            logger.info(f"Successfully updated team: {validated_id}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to update team {team_id}: {str(e)}",
                extra={
                    "team_data_keys": (
                        list(team_data.keys())
                        if isinstance(team_data, dict)
                        else "invalid"
                    )
                },
            )
            raise

    def delete_team(self, team_id: int) -> Dict[str, Any]:
        """Delete a team by its ID with validation.

        Args:
            team_id: The ID of the team to delete (must be a positive integer)

        Returns:
            A dictionary containing the API response (typically empty for successful deletions)

        Raises:
            ValidationError: If team_id is invalid
            NotFoundError: If the team is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            result = client.teams.delete_team(123)
            print("Team deleted successfully")
            ```
        """
        try:
            validated_id = self._validate_resource_id(team_id, "team")

            logger.info(f"Deleting team with ID: {validated_id}")
            result = self.delete(f"/teams/{validated_id}")

            logger.info(f"Successfully deleted team: {validated_id}")
            return result

        except Exception as e:
            logger.error(f"Failed to delete team {team_id}: {str(e)}")
            raise
