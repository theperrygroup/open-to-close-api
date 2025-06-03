"""Custom exceptions for Open To Close API wrapper."""

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class OpenToCloseAPIError(Exception):
    """Base exception for all Open To Close API errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        endpoint: Optional[str] = None,
        method: Optional[str] = None,
        request_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            status_code: HTTP status code
            response_data: Raw response data from API
            endpoint: API endpoint that failed
            method: HTTP method used
            request_data: Request data that caused the error
        """
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data
        self.endpoint = endpoint
        self.method = method
        self.request_data = request_data

        # Log the error for debugging
        self._log_error()

    def _log_error(self) -> None:
        """Log error details for debugging."""
        logger.error(
            "API Error: %s",
            str(self),
            extra={
                "status_code": self.status_code,
                "endpoint": self.endpoint,
                "method": self.method,
                "response_data": self.response_data,
                "request_data": self.request_data,
            },
        )

    def get_error_details(self) -> Dict[str, Any]:
        """Get comprehensive error details for debugging.

        Returns:
            Dictionary containing all available error information
        """
        return {
            "error_type": self.__class__.__name__,
            "message": str(self),
            "status_code": self.status_code,
            "endpoint": self.endpoint,
            "method": self.method,
            "response_data": self.response_data,
            "request_data": self.request_data,
        }


class AuthenticationError(OpenToCloseAPIError):
    """Raised when authentication fails.

    This typically occurs when:
    - API key is missing or invalid
    - API key format is incorrect
    - API key has expired or been revoked
    """

    def __init__(self, message: Optional[str] = None, **kwargs: Any) -> None:
        if not message:
            message = (
                "Authentication failed. Please check your API key. "
                "Ensure OPEN_TO_CLOSE_API_KEY environment variable is set "
                "or pass api_key parameter to the client."
            )
        super().__init__(message, **kwargs)


class ValidationError(OpenToCloseAPIError):
    """Raised when request validation fails.

    This typically occurs when:
    - Required fields are missing
    - Field values are in wrong format
    - Field values exceed limits
    - Invalid parameter combinations
    """

    def __init__(
        self,
        message: Optional[str] = None,
        field_errors: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        if not message and field_errors:
            message = f"Validation failed: {field_errors}"
        elif not message:
            message = "Request validation failed. Please check your input data."

        super().__init__(message, **kwargs)
        self.field_errors = field_errors

    def get_field_errors(self) -> Dict[str, Any]:
        """Get specific field validation errors.

        Returns:
            Dictionary of field-specific error messages
        """
        if self.field_errors:
            return self.field_errors

        # Try to extract field errors from response data
        if self.response_data and isinstance(self.response_data, dict):
            errors = self.response_data.get("errors", {})
            return errors if isinstance(errors, dict) else {}

        return {}


class NotFoundError(OpenToCloseAPIError):
    """Raised when a resource is not found.

    This typically occurs when:
    - Resource ID doesn't exist
    - Resource has been deleted
    - User doesn't have access to the resource
    """

    def __init__(
        self,
        message: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Any = None,
        **kwargs: Any,
    ) -> None:
        if not message:
            if resource_type and resource_id:
                message = f"{resource_type} with ID {resource_id} not found"
            else:
                message = "Requested resource not found"

        super().__init__(message, **kwargs)
        self.resource_type = resource_type
        self.resource_id = resource_id


class RateLimitError(OpenToCloseAPIError):
    """Raised when rate limit is exceeded.

    This typically occurs when:
    - Too many requests in a short time period
    - API quota has been exceeded
    """

    def __init__(
        self,
        message: Optional[str] = None,
        retry_after: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        if not message:
            if retry_after:
                message = f"Rate limit exceeded. Retry after {retry_after} seconds."
            else:
                message = (
                    "Rate limit exceeded. Please wait before making more requests."
                )

        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class ServerError(OpenToCloseAPIError):
    """Raised when server returns 5xx error.

    This typically occurs when:
    - Internal server error
    - Service temporarily unavailable
    - Database connection issues
    """

    def __init__(self, message: Optional[str] = None, **kwargs: Any) -> None:
        if not message:
            message = (
                "Server error occurred. This is typically a temporary issue. "
                "Please try again later or contact support if the problem persists."
            )
        super().__init__(message, **kwargs)


class NetworkError(OpenToCloseAPIError):
    """Raised when network connection fails.

    This typically occurs when:
    - Network connectivity issues
    - DNS resolution failures
    - Connection timeouts
    - SSL/TLS errors
    """

    def __init__(
        self,
        message: Optional[str] = None,
        original_error: Optional[Exception] = None,
        **kwargs: Any,
    ) -> None:
        if not message:
            message = (
                "Network connection failed. Please check your internet connection "
                "and try again."
            )

        super().__init__(message, **kwargs)
        self.original_error = original_error


class TimeoutError(OpenToCloseAPIError):
    """Raised when request times out.

    This typically occurs when:
    - Request takes too long to complete
    - Server is overloaded
    - Network latency issues
    """

    def __init__(
        self,
        message: Optional[str] = None,
        timeout_duration: Optional[float] = None,
        **kwargs: Any,
    ) -> None:
        if not message:
            if timeout_duration:
                message = f"Request timed out after {timeout_duration} seconds"
            else:
                message = "Request timed out. Please try again."

        super().__init__(message, **kwargs)
        self.timeout_duration = timeout_duration


class ConfigurationError(OpenToCloseAPIError):
    """Raised when client configuration is invalid.

    This typically occurs when:
    - Missing required configuration
    - Invalid configuration values
    - Conflicting configuration options
    """

    def __init__(self, message: Optional[str] = None, **kwargs: Any) -> None:
        if not message:
            message = "Invalid client configuration. Please check your settings."
        super().__init__(message, **kwargs)


class DataFormatError(OpenToCloseAPIError):
    """Raised when response data format is unexpected.

    This typically occurs when:
    - API returns malformed JSON
    - Response structure differs from expected
    - Data type mismatches
    """

    def __init__(
        self,
        message: Optional[str] = None,
        expected_format: Optional[str] = None,
        actual_format: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        if not message:
            if expected_format and actual_format:
                message = f"Expected {expected_format} but got {actual_format}"
            else:
                message = "Response data format is invalid or unexpected"

        super().__init__(message, **kwargs)
        self.expected_format = expected_format
        self.actual_format = actual_format
