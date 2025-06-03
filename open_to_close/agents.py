"""Agents client for Open To Close API."""

import logging
from typing import Any, Dict, List, Optional

from .base_client import BaseClient
from .exceptions import ValidationError

logger = logging.getLogger(__name__)


class AgentsAPI(BaseClient):
    """Client for agents API endpoints.

    This client provides methods to manage agents in the Open To Close platform.
    All methods include comprehensive input validation and error handling.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the agents client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API

        Raises:
            AuthenticationError: If API key is missing or invalid
            ConfigurationError: If configuration is invalid
        """
        super().__init__(api_key=api_key, base_url=base_url)
        logger.debug("Initialized AgentsAPI client")

    def _validate_agent_data(self, agent_data: Dict[str, Any], operation: str) -> None:
        """Validate agent data before sending to API.

        Args:
            agent_data: Agent data to validate
            operation: Operation type for error context (create/update)

        Raises:
            ValidationError: If agent data is invalid
        """
        if not isinstance(agent_data, dict):
            raise ValidationError(
                f"Agent data for {operation} must be a dictionary, got {type(agent_data).__name__}"
            )

        if not agent_data:
            raise ValidationError(f"Agent data for {operation} cannot be empty")

        # Validate required fields for create operations
        if operation == "create":
            # Check for at least one identifier field
            identifier_fields = ["email", "phone", "name", "first_name", "last_name"]
            if not any(field in agent_data for field in identifier_fields):
                raise ValidationError(
                    f"Agent data for {operation} must include at least one of: {', '.join(identifier_fields)}"
                )

        # Validate email format if provided
        if "email" in agent_data:
            email = agent_data["email"]
            if not isinstance(email, str) or "@" not in email:
                raise ValidationError(f"Invalid email format: {email}")

        # Validate phone format if provided
        if "phone" in agent_data:
            phone = agent_data["phone"]
            if not isinstance(phone, str) or len(phone.strip()) == 0:
                raise ValidationError(f"Phone must be a non-empty string, got: {phone}")

        # Validate name fields if provided
        for name_field in ["name", "first_name", "last_name"]:
            if name_field in agent_data:
                name_value = agent_data[name_field]
                if not isinstance(name_value, str) or len(name_value.strip()) == 0:
                    raise ValidationError(
                        f"{name_field} must be a non-empty string, got: {name_value}"
                    )

        # Validate license number if provided
        if "license_number" in agent_data:
            license_num = agent_data["license_number"]
            if not isinstance(license_num, str) or len(license_num.strip()) == 0:
                raise ValidationError(
                    f"license_number must be a non-empty string, got: {license_num}"
                )

        logger.debug(f"Agent data validated for {operation} operation")

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

    def list_agents(
        self, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of agents with validation and error handling.

        Args:
            params: Optional dictionary of query parameters for filtering.
                   Supported parameters may include:
                   - limit: Maximum number of agents to return
                   - offset: Number of agents to skip
                   - search: Search term for filtering agents

        Returns:
            A list of dictionaries, where each dictionary represents an agent

        Raises:
            ValidationError: If parameters are invalid
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            # Get all agents
            agents = client.agents.list_agents()

            # Get agents with custom parameters
            agents = client.agents.list_agents(params={"limit": 50, "offset": 100})
            ```
        """
        try:
            validated_params = self._validate_list_params(params)

            logger.info("Listing agents", extra={"params": validated_params})
            response = self.get("/agents", params=validated_params)
            result = self._process_list_response(response, "/agents")

            logger.info(f"Successfully retrieved {len(result)} agents")
            return result

        except Exception as e:
            logger.error(f"Failed to list agents: {str(e)}", extra={"params": params})
            raise

    def create_agent(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new agent with comprehensive validation.

        Args:
            agent_data: A dictionary containing the agent's information.
                       Must include at least one of: email, phone, name, first_name, last_name.
                       Common fields include:
                       - email: Agent email address
                       - phone: Agent phone number
                       - name: Full name (or use first_name/last_name)
                       - first_name: First name
                       - last_name: Last name
                       - license_number: Agent license number
                       - brokerage: Brokerage name

        Returns:
            A dictionary representing the newly created agent

        Raises:
            ValidationError: If agent data is invalid or missing required fields
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            agent = client.agents.create_agent({
                "name": "John Doe",
                "email": "john@realty.com",
                "phone": "+1234567890",
                "license_number": "12345678"
            })
            ```
        """
        try:
            self._validate_agent_data(agent_data, "create")

            logger.info(
                "Creating new agent", extra={"has_email": "email" in agent_data}
            )
            response = self.post("/agents", json_data=agent_data)
            result = self._process_response_data(response, "/agents")

            agent_id = result.get("id")
            logger.info(f"Successfully created agent with ID: {agent_id}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to create agent: {str(e)}",
                extra={
                    "agent_data_keys": (
                        list(agent_data.keys())
                        if isinstance(agent_data, dict)
                        else "invalid"
                    )
                },
            )
            raise

    def retrieve_agent(self, agent_id: int) -> Dict[str, Any]:
        """Retrieve a specific agent by their ID with validation.

        Args:
            agent_id: The ID of the agent to retrieve (must be a positive integer)

        Returns:
            A dictionary representing the agent

        Raises:
            ValidationError: If agent_id is invalid
            NotFoundError: If the agent is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            agent = client.agents.retrieve_agent(123)
            print(f"Agent name: {agent.get('name', 'N/A')}")
            ```
        """
        try:
            validated_id = self._validate_resource_id(agent_id, "agent")

            logger.info(f"Retrieving agent with ID: {validated_id}")
            response = self.get(f"/agents/{validated_id}")
            result = self._process_response_data(response, f"/agents/{validated_id}")

            logger.info(f"Successfully retrieved agent: {validated_id}")
            return result

        except Exception as e:
            logger.error(f"Failed to retrieve agent {agent_id}: {str(e)}")
            raise

    def update_agent(self, agent_id: int, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing agent with validation.

        Args:
            agent_id: The ID of the agent to update (must be a positive integer)
            agent_data: A dictionary containing the fields to update.
                       Fields can include any valid agent fields like:
                       - email, phone, name, first_name, last_name, license_number, etc.

        Returns:
            A dictionary representing the updated agent

        Raises:
            ValidationError: If agent_id or agent_data is invalid
            NotFoundError: If the agent is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            updated_agent = client.agents.update_agent(123, {
                "name": "Jane Doe",
                "email": "jane@realty.com",
                "license_number": "87654321"
            })
            ```
        """
        try:
            validated_id = self._validate_resource_id(agent_id, "agent")
            self._validate_agent_data(agent_data, "update")

            logger.info(
                f"Updating agent with ID: {validated_id}",
                extra={"update_fields": list(agent_data.keys())},
            )
            response = self.put(f"/agents/{validated_id}", json_data=agent_data)
            result = self._process_response_data(response, f"/agents/{validated_id}")

            logger.info(f"Successfully updated agent: {validated_id}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to update agent {agent_id}: {str(e)}",
                extra={
                    "agent_data_keys": (
                        list(agent_data.keys())
                        if isinstance(agent_data, dict)
                        else "invalid"
                    )
                },
            )
            raise

    def delete_agent(self, agent_id: int) -> Dict[str, Any]:
        """Delete an agent by their ID with validation.

        Args:
            agent_id: The ID of the agent to delete (must be a positive integer)

        Returns:
            A dictionary containing the API response (typically empty for successful deletions)

        Raises:
            ValidationError: If agent_id is invalid
            NotFoundError: If the agent is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            result = client.agents.delete_agent(123)
            print("Agent deleted successfully")
            ```
        """
        try:
            validated_id = self._validate_resource_id(agent_id, "agent")

            logger.info(f"Deleting agent with ID: {validated_id}")
            result = self.delete(f"/agents/{validated_id}")

            logger.info(f"Successfully deleted agent: {validated_id}")
            return result

        except Exception as e:
            logger.error(f"Failed to delete agent {agent_id}: {str(e)}")
            raise
