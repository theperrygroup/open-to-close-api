"""Custom exceptions for Open To Close API wrapper."""

from typing import Any, Dict, Optional


class OpenToCloseAPIError(Exception):
    """Base exception for all Open To Close API errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            status_code: HTTP status code
            response_data: Raw response data
        """
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class AuthenticationError(OpenToCloseAPIError):
    """Raised when authentication fails."""


class ValidationError(OpenToCloseAPIError):
    """Raised when request validation fails."""


class NotFoundError(OpenToCloseAPIError):
    """Raised when a resource is not found."""


class RateLimitError(OpenToCloseAPIError):
    """Raised when rate limit is exceeded."""


class ServerError(OpenToCloseAPIError):
    """Raised when server returns 5xx error."""


class NetworkError(OpenToCloseAPIError):
    """Raised when network connection fails."""
