"""Base client for Open To Close API."""

import os
from typing import Any, Dict, List, Optional, Union

import requests
from dotenv import load_dotenv

from .exceptions import (
    AuthenticationError,
    NetworkError,
    NotFoundError,
    OpenToCloseAPIError,
    RateLimitError,
    ServerError,
    ValidationError,
)

load_dotenv()

# Constants
DEFAULT_BASE_URL = "https://api.opentoclose.com/v1"


class BaseClient:
    """Base client with common functionality."""

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the base client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API
        """
        self.api_key = api_key or os.getenv("OPEN_TO_CLOSE_API_KEY")
        if not self.api_key:
            raise AuthenticationError(
                "API key is required. Set OPEN_TO_CLOSE_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.base_url = base_url or DEFAULT_BASE_URL
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle HTTP response and raise appropriate exceptions."""
        try:
            response_data = response.json() if response.content else {}
        except ValueError:
            response_data = {"message": response.text}

        if response.status_code in (200, 201):
            return response_data
        if response.status_code == 204:
            return {}
        if response.status_code == 400:
            raise ValidationError(
                f"Bad request: {response_data.get('message', 'Invalid request')}",
                status_code=400,
                response_data=response_data,
            )
        if response.status_code == 401:
            message = response_data.get("message", "Invalid credentials")
            raise AuthenticationError(
                f"Authentication failed: {message}",
                status_code=401,
                response_data=response_data,
            )
        if response.status_code == 404:
            raise NotFoundError(
                f"Resource not found: {response_data.get('message', 'Not found')}",
                status_code=404,
                response_data=response_data,
            )
        if response.status_code == 429:
            message = response_data.get("message", "Too many requests")
            raise RateLimitError(
                f"Rate limit exceeded: {message}",
                status_code=429,
                response_data=response_data,
            )
        if 500 <= response.status_code < 600:
            message = response_data.get("message", "Internal server error")
            raise ServerError(
                f"Server error: {message}",
                status_code=response.status_code,
                response_data=response_data,
            )

        raise OpenToCloseAPIError(
            f"Unexpected error: {response_data.get('message', 'Unknown error')}",
            status_code=response.status_code,
            response_data=response_data,
        )

    def _process_response_data(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Process API response data with consistent format handling.

        Args:
            response: Raw response from API

        Returns:
            Processed response data
        """
        if isinstance(response, dict) and response.get("id"):
            return response
        if isinstance(response, dict):
            data = response.get("data", {})
            return data if isinstance(data, dict) else {}
        return {}

    def _process_list_response(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process API response for list endpoints with consistent format handling.

        Args:
            response: Raw response from API

        Returns:
            List of processed response data
        """
        if isinstance(response, list):
            return response
        if isinstance(response, dict):
            data = response.get("data", [])
            return data if isinstance(data, list) else []
        return []

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        files: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request to API."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        # Add api_token to params for all requests
        if params is None:
            params = {}
        params["api_token"] = self.api_key

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=json_data,
                data=data,
                files=files,
                params=params,
            )
            return self._handle_response(response)

        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error: {str(e)}") from e

    def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make GET request."""
        return self._request("GET", endpoint, params=params)

    def post(
        self,
        endpoint: str,
        json_data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make POST request."""
        return self._request(
            "POST", endpoint, json_data=json_data, data=data, files=files
        )

    def put(
        self,
        endpoint: str,
        json_data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make PUT request."""
        return self._request(
            "PUT", endpoint, json_data=json_data, data=data, files=files
        )

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request."""
        return self._request("DELETE", endpoint)

    def patch(
        self,
        endpoint: str,
        json_data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make PATCH request."""
        return self._request(
            "PATCH", endpoint, json_data=json_data, data=data, files=files
        )
