# Error Handling Guide

Comprehensive guide to handling errors in the Open To Close API Python client. Learn patterns and best practices for building robust, resilient applications.

!!! abstract "Error Handling Philosophy"
    Effective error handling improves user experience, aids debugging, and ensures application reliability. The Open To Close API provides structured exceptions to help you handle different scenarios appropriately.

---

## 🚀 Quick Start

```python
from open_to_close import OpenToCloseAPI
from open_to_close.exceptions import (
    AuthenticationError,
    ValidationError, 
    NotFoundError,
    RateLimitError
)

client = OpenToCloseAPI()

try:
    property_data = client.properties.retrieve_property(123)
except NotFoundError:
    print("Property not found")
except AuthenticationError:
    print("Authentication failed - check your API key")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## 🎯 Exception-Specific Handling

### **Authentication Errors**

Authentication errors typically require immediate attention and shouldn't be retried without fixing the underlying issue.

```python
from open_to_close.exceptions import AuthenticationError

def handle_auth_error():
    try:
        client = OpenToCloseAPI(api_key="invalid_key")
        properties = client.properties.list_properties()
    except AuthenticationError as e:
        print(f"Authentication failed: {e}")
        
        # Log the error for debugging
        logger.error(f"API authentication failed: {e}")
        
        # Notify user with actionable message
        return {
            "error": "authentication_failed",
            "message": "Please check your API key configuration",
            "action_required": "Verify API key in environment variables"
        }
```

### **Validation Errors**

Validation errors indicate invalid data. These should be caught and the user should be provided with specific feedback.

```python
from open_to_close.exceptions import ValidationError

def create_property_with_validation(property_data):
    """Create property with comprehensive validation error handling."""
    try:
        return client.properties.create_property(property_data)
        
    except ValidationError as e:
        # Extract validation details if available
        error_details = {}
        if hasattr(e, 'response_data') and e.response_data:
            error_details = e.response_data.get('error', {})
        
        # Create user-friendly error response
        return {
            "success": False,
            "error": "validation_failed",
            "message": str(e),
            "details": error_details.get('details', {}),
            "fields": extract_field_errors(error_details)
        }

def extract_field_errors(error_details):
    """Extract field-specific validation errors."""
    field_errors = {}
    
    if 'details' in error_details:
        details = error_details['details']
        if isinstance(details, dict):
            for field, error_msg in details.items():
                field_errors[field] = error_msg
    
    return field_errors
```

### **Not Found Errors**

Handle missing resources gracefully, especially in user-facing applications.

```python
from open_to_close.exceptions import NotFoundError

def safe_get_property(property_id):
    """Safely retrieve a property with user-friendly error handling."""
    try:
        return {
            "success": True,
            "data": client.properties.retrieve_property(property_id)
        }
        
    except NotFoundError:
        logger.warning(f"Property {property_id} not found")
        return {
            "success": False,
            "error": "not_found",
            "message": f"Property with ID {property_id} was not found",
            "suggestion": "Please verify the property ID and try again"
        }
        
    except Exception as e:
        logger.error(f"Unexpected error retrieving property {property_id}: {e}")
        return {
            "success": False,
            "error": "unexpected_error",
            "message": "An unexpected error occurred",
            "details": str(e)
        }
```

### **Rate Limit Errors**

Implement automatic retry logic with exponential backoff for rate limit errors.

```python
import time
from open_to_close.exceptions import RateLimitError

def rate_limited_request(operation_func, *args, max_retries=3, **kwargs):
    """Execute operation with automatic rate limit handling."""
    
    for attempt in range(max_retries):
        try:
            return operation_func(*args, **kwargs)
            
        except RateLimitError as e:
            if attempt < max_retries - 1:
                # Calculate delay (exponential backoff)
                delay = getattr(e, 'retry_after', 2 ** attempt)
                
                logger.warning(
                    f"Rate limited on attempt {attempt + 1}. "
                    f"Waiting {delay} seconds before retry..."
                )
                
                time.sleep(delay)
                continue
            else:
                logger.error(f"Rate limit exceeded after {max_retries} attempts")
                raise
                
        except Exception as e:
            # Don't retry on other errors
            logger.error(f"Non-rate-limit error: {e}")
            raise

# Usage
def get_properties_with_rate_limiting():
    return rate_limited_request(
        client.properties.list_properties,
        params={"limit": 100}
    )
```

---

## 🔄 Retry Patterns

### **Exponential Backoff**

```python
import time
import random
from open_to_close.exceptions import ServerError, NetworkError

def exponential_backoff_retry(
    operation_func, 
    *args, 
    max_retries=3, 
    base_delay=1,
    max_delay=60,
    jitter=True,
    **kwargs
):
    """
    Execute operation with exponential backoff retry logic.
    
    Args:
        operation_func: Function to execute
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        jitter: Add random jitter to prevent thundering herd
    """
    
    for attempt in range(max_retries + 1):
        try:
            return operation_func(*args, **kwargs)
            
        except (ServerError, NetworkError) as e:
            if attempt < max_retries:
                # Calculate delay with exponential backoff
                delay = min(base_delay * (2 ** attempt), max_delay)
                
                # Add jitter to prevent thundering herd problem
                if jitter:
                    delay += random.uniform(0, delay * 0.1)
                
                logger.warning(
                    f"Attempt {attempt + 1} failed: {e}. "
                    f"Retrying in {delay:.2f} seconds..."
                )
                
                time.sleep(delay)
                continue
            else:
                logger.error(f"Operation failed after {max_retries} retries: {e}")
                raise
                
        except Exception as e:
            # Don't retry on non-retryable errors
            logger.error(f"Non-retryable error: {e}")
            raise
```

### **Circuit Breaker Pattern**

```python
import time
from enum import Enum
from dataclasses import dataclass

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open" 
    HALF_OPEN = "half_open"

@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    recovery_timeout: int = 60
    expected_exceptions: tuple = (ServerError, NetworkError)

class CircuitBreaker:
    def __init__(self, config: CircuitBreakerConfig):
        self.config = config
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        
    def call(self, operation_func, *args, **kwargs):
        """Execute operation through circuit breaker."""
        
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = operation_func(*args, **kwargs)
            self._on_success()
            return result
            
        except self.config.expected_exceptions as e:
            self._on_failure()
            raise
            
    def _should_attempt_reset(self):
        """Check if enough time has passed to attempt reset."""
        if self.last_failure_time is None:
            return True
            
        return (time.time() - self.last_failure_time) >= self.config.recovery_timeout
    
    def _on_success(self):
        """Handle successful operation."""
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        
    def _on_failure(self):
        """Handle failed operation."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.config.failure_threshold:
            self.state = CircuitState.OPEN

# Usage
circuit_breaker = CircuitBreaker(CircuitBreakerConfig())

def protected_api_call():
    return circuit_breaker.call(
        client.properties.list_properties,
        params={"limit": 10}
    )
```

---

## 📊 Error Monitoring and Logging

### **Structured Logging**

```python
import logging
import json
from datetime import datetime

class APIErrorLogger:
    def __init__(self):
        self.logger = logging.getLogger('open_to_close_api')
        self.setup_logger()
        
    def setup_logger(self):
        """Configure structured logging."""
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        
    def log_api_error(self, operation, error, context=None):
        """Log API error with structured data."""
        error_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context or {}
        }
        
        # Add additional error details if available
        if hasattr(error, 'status_code'):
            error_data["status_code"] = error.status_code
            
        if hasattr(error, 'response_data'):
            error_data["response_data"] = error.response_data
            
        self.logger.error(json.dumps(error_data))
        
    def log_retry_attempt(self, operation, attempt, max_retries, error):
        """Log retry attempts."""
        retry_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation,
            "attempt": attempt,
            "max_retries": max_retries,
            "error_type": type(error).__name__,
            "error_message": str(error)
        }
        
        self.logger.warning(f"Retry attempt: {json.dumps(retry_data)}")

# Usage
error_logger = APIErrorLogger()

def logged_operation(operation_name, operation_func, *args, **kwargs):
    """Execute operation with comprehensive error logging."""
    try:
        return operation_func(*args, **kwargs)
        
    except Exception as e:
        error_logger.log_api_error(
            operation=operation_name,
            error=e,
            context={
                "args": args,
                "kwargs": kwargs
            }
        )
        raise
```

### **Error Metrics Collection**

```python
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ErrorMetrics:
    total_errors: int = 0
    error_types: Dict[str, int] = None
    operations: Dict[str, int] = None
    
    def __post_init__(self):
        if self.error_types is None:
            self.error_types = defaultdict(int)
        if self.operations is None:
            self.operations = defaultdict(int)

class ErrorTracker:
    def __init__(self):
        self.metrics = ErrorMetrics()
        
    def record_error(self, error, operation=None):
        """Record error for metrics tracking."""
        self.metrics.total_errors += 1
        self.metrics.error_types[type(error).__name__] += 1
        
        if operation:
            self.metrics.operations[operation] += 1
            
    def get_metrics(self):
        """Get current error metrics."""
        return {
            "total_errors": self.metrics.total_errors,
            "error_types": dict(self.metrics.error_types),
            "operations": dict(self.metrics.operations),
            "error_rate": self._calculate_error_rate()
        }
        
    def _calculate_error_rate(self):
        """Calculate error rate (placeholder - implement based on your needs)."""
        # This would typically compare errors to total requests
        return 0.0

# Global error tracker
error_tracker = ErrorTracker()

def tracked_operation(operation_name, operation_func, *args, **kwargs):
    """Execute operation with error tracking."""
    try:
        return operation_func(*args, **kwargs)
        
    except Exception as e:
        error_tracker.record_error(e, operation_name)
        raise
```

---

## 🛡️ Production-Ready Error Handler

### **Complete Error Handling Wrapper**

```python
import asyncio
from functools import wraps
from typing import Callable, Any, Optional

class APIErrorHandler:
    """Production-ready error handler for Open To Close API operations."""
    
    def __init__(self, 
                 logger: Optional[logging.Logger] = None,
                 error_tracker: Optional[ErrorTracker] = None,
                 circuit_breaker: Optional[CircuitBreaker] = None):
        self.logger = logger or logging.getLogger(__name__)
        self.error_tracker = error_tracker
        self.circuit_breaker = circuit_breaker
        
    def handle_operation(self, 
                        operation_name: str,
                        operation_func: Callable,
                        *args,
                        retry_on_rate_limit: bool = True,
                        max_retries: int = 3,
                        **kwargs) -> Dict[str, Any]:
        """
        Execute API operation with comprehensive error handling.
        
        Args:
            operation_name: Human-readable operation name
            operation_func: The API operation to execute
            retry_on_rate_limit: Whether to retry on rate limit errors
            max_retries: Maximum number of retries for rate limits
            
        Returns:
            Dictionary with success status and data or error information
        """
        
        try:
            # Use circuit breaker if available
            if self.circuit_breaker:
                result = self.circuit_breaker.call(operation_func, *args, **kwargs)
            else:
                result = operation_func(*args, **kwargs)
                
            return {
                "success": True,
                "data": result,
                "operation": operation_name
            }
            
        except AuthenticationError as e:
            return self._handle_auth_error(operation_name, e)
            
        except ValidationError as e:
            return self._handle_validation_error(operation_name, e)
            
        except NotFoundError as e:
            return self._handle_not_found_error(operation_name, e)
            
        except RateLimitError as e:
            if retry_on_rate_limit:
                return self._handle_rate_limit_with_retry(
                    operation_name, operation_func, e, max_retries, *args, **kwargs
                )
            else:
                return self._handle_rate_limit_error(operation_name, e)
                
        except (ServerError, NetworkError) as e:
            return self._handle_server_error(operation_name, e)
            
        except Exception as e:
            return self._handle_unexpected_error(operation_name, e)
    
    def _handle_auth_error(self, operation_name: str, error: AuthenticationError):
        """Handle authentication errors."""
        self._log_and_track_error(operation_name, error)
        
        return {
            "success": False,
            "error": "authentication_failed",
            "message": "Authentication failed. Please check your API key.",
            "operation": operation_name,
            "retry_recommended": False
        }
    
    def _handle_validation_error(self, operation_name: str, error: ValidationError):
        """Handle validation errors."""
        self._log_and_track_error(operation_name, error)
        
        # Extract field-specific errors if available
        field_errors = {}
        if hasattr(error, 'response_data') and error.response_data:
            details = error.response_data.get('error', {}).get('details', {})
            if isinstance(details, dict):
                field_errors = details
        
        return {
            "success": False,
            "error": "validation_failed",
            "message": str(error),
            "field_errors": field_errors,
            "operation": operation_name,
            "retry_recommended": False
        }
    
    def _handle_not_found_error(self, operation_name: str, error: NotFoundError):
        """Handle not found errors."""
        self._log_and_track_error(operation_name, error, level="warning")
        
        return {
            "success": False,
            "error": "not_found",
            "message": "The requested resource was not found.",
            "operation": operation_name,
            "retry_recommended": False
        }
    
    def _handle_rate_limit_error(self, operation_name: str, error: RateLimitError):
        """Handle rate limit errors without retry."""
        self._log_and_track_error(operation_name, error)
        
        retry_after = getattr(error, 'retry_after', 60)
        
        return {
            "success": False,
            "error": "rate_limited",
            "message": f"Rate limit exceeded. Please retry after {retry_after} seconds.",
            "retry_after": retry_after,
            "operation": operation_name,
            "retry_recommended": True
        }
    
    def _handle_rate_limit_with_retry(self, 
                                    operation_name: str,
                                    operation_func: Callable,
                                    error: RateLimitError,
                                    max_retries: int,
                                    *args, **kwargs):
        """Handle rate limit errors with automatic retry."""
        return rate_limited_request(
            operation_func, *args, max_retries=max_retries, **kwargs
        )
    
    def _handle_server_error(self, operation_name: str, error):
        """Handle server errors."""
        self._log_and_track_error(operation_name, error)
        
        return {
            "success": False,
            "error": "server_error",
            "message": "A server error occurred. Please try again later.",
            "operation": operation_name,
            "retry_recommended": True
        }
    
    def _handle_unexpected_error(self, operation_name: str, error: Exception):
        """Handle unexpected errors."""
        self._log_and_track_error(operation_name, error)
        
        return {
            "success": False,
            "error": "unexpected_error",
            "message": "An unexpected error occurred.",
            "details": str(error),
            "operation": operation_name,
            "retry_recommended": False
        }
    
    def _log_and_track_error(self, operation_name: str, error: Exception, level: str = "error"):
        """Log and track error for monitoring."""
        if self.logger:
            log_func = getattr(self.logger, level)
            log_func(f"Operation '{operation_name}' failed: {error}")
            
        if self.error_tracker:
            self.error_tracker.record_error(error, operation_name)

# Usage
error_handler = APIErrorHandler(
    logger=logging.getLogger(__name__),
    error_tracker=error_tracker,
    circuit_breaker=circuit_breaker
)

# Decorator for easy use
def with_error_handling(operation_name: str, **handler_kwargs):
    """Decorator to wrap API operations with error handling."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return error_handler.handle_operation(
                operation_name, func, *args, **handler_kwargs, **kwargs
            )
        return wrapper
    return decorator

# Example usage
@with_error_handling("get_property", retry_on_rate_limit=True)
def get_property(property_id):
    return client.properties.retrieve_property(property_id)

@with_error_handling("create_property", retry_on_rate_limit=False) 
def create_property(property_data):
    return client.properties.create_property(property_data)
```

---

## 🚀 Best Practices Summary

1. **Catch specific exceptions** rather than generic `Exception` when possible
2. **Implement retry logic** for transient errors (rate limits, server errors)
3. **Use exponential backoff** to avoid overwhelming servers
4. **Log errors appropriately** with sufficient context for debugging
5. **Provide user-friendly error messages** with actionable guidance
6. **Monitor error patterns** to identify systemic issues
7. **Don't retry authentication or validation errors** - they require intervention
8. **Use circuit breakers** for external service reliability
9. **Track error metrics** for performance monitoring
10. **Test error handling paths** as thoroughly as success paths

---

## 📚 Related Resources

- **[Exception Reference](../reference/exceptions.md)** - Complete exception documentation
- **[Best Practices](best-practices.md)** - General development guidelines
- **[API Reference](../api/index.md)** - API method documentation

---

*Robust error handling is essential for production applications. Use these patterns to build resilient, user-friendly experiences.* 