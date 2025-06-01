"""Tests for exceptions module."""

import pytest

from open_to_close.exceptions import (
    AuthenticationError,
    NetworkError,
    NotFoundError,
    OpenToCloseAPIError,
    RateLimitError,
    ServerError,
    ValidationError,
)


class TestOpenToCloseAPIError:
    """Test base OpenToCloseAPIError."""

    def test_basic_error(self) -> None:
        """Test basic error creation."""
        error = OpenToCloseAPIError("Test error")
        assert str(error) == "Test error"
        assert error.status_code is None
        assert error.response_data is None

    def test_error_with_status_code(self) -> None:
        """Test error with status code."""
        error = OpenToCloseAPIError("Test error", status_code=400)
        assert str(error) == "Test error"
        assert error.status_code == 400
        assert error.response_data is None

    def test_error_with_response_data(self) -> None:
        """Test error with response data."""
        response_data = {"error": "details", "field": "name"}
        error = OpenToCloseAPIError("Test error", response_data=response_data)
        assert str(error) == "Test error"
        assert error.status_code is None
        assert error.response_data == response_data

    def test_error_with_all_params(self) -> None:
        """Test error with all parameters."""
        response_data = {"error": "details"}
        error = OpenToCloseAPIError(
            "Test error", status_code=422, response_data=response_data
        )
        assert str(error) == "Test error"
        assert error.status_code == 422
        assert error.response_data == response_data

    def test_error_inheritance(self) -> None:
        """Test that OpenToCloseAPIError inherits from Exception."""
        error = OpenToCloseAPIError("Test error")
        assert isinstance(error, Exception)


class TestAuthenticationError:
    """Test AuthenticationError."""

    def test_authentication_error(self) -> None:
        """Test authentication error creation."""
        error = AuthenticationError("Invalid API key")
        assert str(error) == "Invalid API key"
        assert isinstance(error, OpenToCloseAPIError)

    def test_authentication_error_with_status_code(self) -> None:
        """Test authentication error with status code."""
        error = AuthenticationError("Invalid API key", status_code=401)
        assert str(error) == "Invalid API key"
        assert error.status_code == 401

    def test_authentication_error_inheritance(self) -> None:
        """Test AuthenticationError inheritance."""
        error = AuthenticationError("Test")
        assert isinstance(error, OpenToCloseAPIError)
        assert isinstance(error, Exception)


class TestValidationError:
    """Test ValidationError."""

    def test_validation_error(self) -> None:
        """Test validation error creation."""
        error = ValidationError("Invalid field format")
        assert str(error) == "Invalid field format"
        assert isinstance(error, OpenToCloseAPIError)

    def test_validation_error_with_data(self) -> None:
        """Test validation error with response data."""
        response_data = {"errors": {"name": ["This field is required"]}}
        error = ValidationError("Validation failed", response_data=response_data)
        assert str(error) == "Validation failed"
        assert error.response_data == response_data

    def test_validation_error_inheritance(self) -> None:
        """Test ValidationError inheritance."""
        error = ValidationError("Test")
        assert isinstance(error, OpenToCloseAPIError)
        assert isinstance(error, Exception)


class TestNotFoundError:
    """Test NotFoundError."""

    def test_not_found_error(self) -> None:
        """Test not found error creation."""
        error = NotFoundError("Resource not found")
        assert str(error) == "Resource not found"
        assert isinstance(error, OpenToCloseAPIError)

    def test_not_found_error_with_status_code(self) -> None:
        """Test not found error with status code."""
        error = NotFoundError("Resource not found", status_code=404)
        assert str(error) == "Resource not found"
        assert error.status_code == 404

    def test_not_found_error_inheritance(self) -> None:
        """Test NotFoundError inheritance."""
        error = NotFoundError("Test")
        assert isinstance(error, OpenToCloseAPIError)
        assert isinstance(error, Exception)


class TestRateLimitError:
    """Test RateLimitError."""

    def test_rate_limit_error(self) -> None:
        """Test rate limit error creation."""
        error = RateLimitError("Too many requests")
        assert str(error) == "Too many requests"
        assert isinstance(error, OpenToCloseAPIError)

    def test_rate_limit_error_with_status_code(self) -> None:
        """Test rate limit error with status code."""
        error = RateLimitError("Too many requests", status_code=429)
        assert str(error) == "Too many requests"
        assert error.status_code == 429

    def test_rate_limit_error_inheritance(self) -> None:
        """Test RateLimitError inheritance."""
        error = RateLimitError("Test")
        assert isinstance(error, OpenToCloseAPIError)
        assert isinstance(error, Exception)


class TestServerError:
    """Test ServerError."""

    def test_server_error(self) -> None:
        """Test server error creation."""
        error = ServerError("Internal server error")
        assert str(error) == "Internal server error"
        assert isinstance(error, OpenToCloseAPIError)

    def test_server_error_with_status_code(self) -> None:
        """Test server error with status code."""
        error = ServerError("Internal server error", status_code=500)
        assert str(error) == "Internal server error"
        assert error.status_code == 500

    def test_server_error_inheritance(self) -> None:
        """Test ServerError inheritance."""
        error = ServerError("Test")
        assert isinstance(error, OpenToCloseAPIError)
        assert isinstance(error, Exception)


class TestNetworkError:
    """Test NetworkError."""

    def test_network_error(self) -> None:
        """Test network error creation."""
        error = NetworkError("Connection failed")
        assert str(error) == "Connection failed"
        assert isinstance(error, OpenToCloseAPIError)

    def test_network_error_inheritance(self) -> None:
        """Test NetworkError inheritance."""
        error = NetworkError("Test")
        assert isinstance(error, OpenToCloseAPIError)
        assert isinstance(error, Exception)


class TestErrorRaising:
    """Test error raising scenarios."""

    def test_raise_authentication_error(self) -> None:
        """Test raising authentication error."""
        with pytest.raises(AuthenticationError, match="Invalid credentials"):
            raise AuthenticationError("Invalid credentials")

    def test_raise_validation_error(self) -> None:
        """Test raising validation error."""
        with pytest.raises(ValidationError, match="Invalid data"):
            raise ValidationError("Invalid data")

    def test_raise_not_found_error(self) -> None:
        """Test raising not found error."""
        with pytest.raises(NotFoundError, match="Resource not found"):
            raise NotFoundError("Resource not found")

    def test_raise_rate_limit_error(self) -> None:
        """Test raising rate limit error."""
        with pytest.raises(RateLimitError, match="Too many requests"):
            raise RateLimitError("Too many requests")

    def test_raise_server_error(self) -> None:
        """Test raising server error."""
        with pytest.raises(ServerError, match="Server error"):
            raise ServerError("Server error")

    def test_raise_network_error(self) -> None:
        """Test raising network error."""
        with pytest.raises(NetworkError, match="Network error"):
            raise NetworkError("Network error")

    def test_catch_as_base_exception(self) -> None:
        """Test catching specific errors as base OpenToCloseAPIError."""
        with pytest.raises(OpenToCloseAPIError):
            raise AuthenticationError("Test")

        with pytest.raises(OpenToCloseAPIError):
            raise ValidationError("Test")

        with pytest.raises(OpenToCloseAPIError):
            raise NotFoundError("Test")

        with pytest.raises(OpenToCloseAPIError):
            raise RateLimitError("Test")

        with pytest.raises(OpenToCloseAPIError):
            raise ServerError("Test")

        with pytest.raises(OpenToCloseAPIError):
            raise NetworkError("Test")
