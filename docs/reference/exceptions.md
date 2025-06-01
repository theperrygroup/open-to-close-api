# Exception Reference

Complete reference for all exception types in the Open To Close API Python client. Understanding these exceptions is essential for building robust applications with proper error handling.

!!! abstract "Exception Hierarchy"
    All Open To Close API exceptions inherit from `OpenToCloseAPIError`, providing a consistent interface for error handling.

---

## 🚀 Exception Hierarchy

```python
OpenToCloseAPIError (Base Exception)
├── AuthenticationError
├── ValidationError  
├── NotFoundError
├── RateLimitError
├── ServerError
└── NetworkError
```

---

## 📋 Base Exception

### **OpenToCloseAPIError**

The base exception class for all Open To Close API errors. All specific exceptions inherit from this class.

```python
class OpenToCloseAPIError(Exception):
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ) -> None:
```

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `message` | `str` | Human-readable error message |
| `status_code` | `Optional[int]` | HTTP status code (if applicable) |
| `response_data` | `Optional[Dict[str, Any]]` | Raw response data from API |

**Usage:**
```python
try:
    client.properties.retrieve_property(123)
except OpenToCloseAPIError as e:
    print(f"API Error: {e}")
    print(f"Status Code: {e.status_code}")
    print(f"Response Data: {e.response_data}")
```

---

## 🔐 Authentication Exceptions

### **AuthenticationError**

Raised when authentication fails due to invalid, missing, or expired API credentials.

**Common Causes:**
- Invalid API key
- Missing API key in environment variables
- Expired or revoked API key
- Incorrect API key format

**HTTP Status Codes:** `401 Unauthorized`, `403 Forbidden`

=== ":material-shield-alert: Common Scenarios"

    ```python
    from open_to_close.exceptions import AuthenticationError
    
    try:
        client = OpenToCloseAPI(api_key="invalid_key")
        properties = client.properties.list_properties()
    except AuthenticationError as e:
        print(f"Authentication failed: {e}")
        # Handle authentication error
        # - Check API key configuration
        # - Regenerate API key if needed
        # - Verify environment variables
    ```

=== ":material-key-variant: Resolution Steps"

    **1. Verify API Key:**
    ```python
    import os
    
    # Check if API key is set
    api_key = os.getenv("OPEN_TO_CLOSE_API_KEY")
    if not api_key:
        raise EnvironmentError("API key not found in environment")
    
    # Check API key format (basic validation)
    if len(api_key) < 50:
        print("Warning: API key seems too short")
    ```

    **2. Test Authentication:**
    ```python
    def test_authentication():
        try:
            client = OpenToCloseAPI()
            # Simple test call
            client.agents.list_agents(params={"limit": 1})
            print("✅ Authentication successful")
            return True
        except AuthenticationError:
            print("❌ Authentication failed")
            return False
    ```

---

## ✅ Validation Exceptions

### **ValidationError**

Raised when request parameters or data fail validation on the client or server side.

**Common Causes:**
- Invalid data types in request payload
- Missing required fields
- Field values outside acceptable ranges
- Malformed request parameters

**HTTP Status Codes:** `400 Bad Request`, `422 Unprocessable Entity`

=== ":material-alert-circle: Common Scenarios"

    ```python
    from open_to_close.exceptions import ValidationError
    
    try:
        # Invalid data that fails validation
        client.properties.create_property({
            "invalid_field": "value",
            "price": "not_a_number"  # Should be numeric
        })
    except ValidationError as e:
        print(f"Validation failed: {e}")
        # Handle validation error
        # - Check required fields
        # - Validate data types
        # - Review API documentation
    ```

=== ":material-check-circle: Prevention"

    **Data Validation Helper:**
    ```python
    def validate_property_data(property_data):
        """Validate property data before API call."""
        required_fields = ["address", "city", "state"]
        errors = []
        
        # Check required fields
        for field in required_fields:
            if field not in property_data:
                errors.append(f"Missing required field: {field}")
        
        # Validate data types
        if "price" in property_data:
            try:
                float(property_data["price"])
            except (ValueError, TypeError):
                errors.append("Price must be a number")
        
        if errors:
            raise ValidationError(f"Validation errors: {', '.join(errors)}")
        
        return True
    
    # Usage
    property_data = {"address": "123 Main St", "city": "NYC", "state": "NY"}
    validate_property_data(property_data)
    client.properties.create_property(property_data)
    ```

---

## 🔍 Resource Exceptions

### **NotFoundError**

Raised when attempting to access a resource that doesn't exist or has been deleted.

**Common Causes:**
- Resource ID doesn't exist
- Resource was deleted
- Insufficient permissions to access resource
- Typo in resource ID

**HTTP Status Codes:** `404 Not Found`

=== ":material-magnify: Common Scenarios"

    ```python
    from open_to_close.exceptions import NotFoundError
    
    try:
        # Attempting to access non-existent resource
        property_data = client.properties.retrieve_property(999999)
    except NotFoundError as e:
        print(f"Property not found: {e}")
        # Handle not found error
        # - Verify resource ID
        # - Check if resource was deleted
        # - Provide user feedback
    ```

=== ":material-shield-check: Safe Operations"

    **Safe Resource Access:**
    ```python
    def safe_get_property(client, property_id):
        """Safely retrieve a property with error handling."""
        try:
            return client.properties.retrieve_property(property_id)
        except NotFoundError:
            print(f"Property {property_id} not found")
            return None
        except Exception as e:
            print(f"Error retrieving property {property_id}: {e}")
            return None
    
    # Batch safe operations
    def get_multiple_properties(client, property_ids):
        """Get multiple properties, skipping those that don't exist."""
        properties = []
        for prop_id in property_ids:
            prop = safe_get_property(client, prop_id)
            if prop:
                properties.append(prop)
        return properties
    ```

---

## 🚦 Rate Limiting Exceptions

### **RateLimitError**

Raised when API rate limits are exceeded. This protects the API from being overwhelmed.

**Common Causes:**
- Too many requests in short time period
- Concurrent requests exceeding limits
- Bulk operations without rate limiting

**HTTP Status Codes:** `429 Too Many Requests`

=== ":material-timer: Rate Limit Handling"

    ```python
    import time
    from open_to_close.exceptions import RateLimitError
    
    def rate_limited_operation(operation_func, max_retries=3):
        """Execute operation with automatic retry on rate limit."""
        for attempt in range(max_retries):
            try:
                return operation_func()
            except RateLimitError as e:
                if attempt < max_retries - 1:
                    # Extract retry delay from headers if available
                    delay = getattr(e, 'retry_after', 60)  # Default 60 seconds
                    print(f"Rate limited. Waiting {delay} seconds before retry...")
                    time.sleep(delay)
                else:
                    print("Max retries exceeded for rate limit")
                    raise
    
    # Usage
    def get_properties():
        return client.properties.list_properties()
    
    properties = rate_limited_operation(get_properties)
    ```

=== ":material-clock-fast: Batch Operations"

    **Rate-Limited Batch Processing:**
    ```python
    import time
    
    def process_properties_batch(client, property_ids, delay=1.0):
        """Process properties in batches with rate limiting."""
        results = []
        
        for i, prop_id in enumerate(property_ids):
            try:
                # Add delay between requests
                if i > 0:
                    time.sleep(delay)
                
                property_data = client.properties.retrieve_property(prop_id)
                results.append(property_data)
                
            except RateLimitError:
                print(f"Rate limited at property {prop_id}. Increasing delay.")
                delay *= 2  # Exponential backoff
                time.sleep(delay)
                # Retry current item
                property_data = client.properties.retrieve_property(prop_id)
                results.append(property_data)
                
        return results
    ```

---

## 🖥️ Server Exceptions

### **ServerError**

Raised when the server encounters an internal error. These are typically temporary issues.

**Common Causes:**
- Internal server errors
- Database connectivity issues
- Service unavailability
- Server maintenance

**HTTP Status Codes:** `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable`

=== ":material-server: Server Error Handling"

    ```python
    import time
    from open_to_close.exceptions import ServerError
    
    def retry_on_server_error(operation_func, max_retries=3, base_delay=5):
        """Retry operation on server errors with exponential backoff."""
        for attempt in range(max_retries):
            try:
                return operation_func()
            except ServerError as e:
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)  # Exponential backoff
                    print(f"Server error on attempt {attempt + 1}. Retrying in {delay}s...")
                    time.sleep(delay)
                else:
                    print("Max retries exceeded for server error")
                    raise
    ```

---

## 🌐 Network Exceptions

### **NetworkError**

Raised when network connectivity issues prevent API communication.

**Common Causes:**
- Internet connectivity issues
- DNS resolution failures
- Network timeouts
- Firewall blocking requests

**HTTP Status Codes:** No HTTP status (connection never established)

=== ":material-wifi-off: Network Error Handling"

    ```python
    import time
    from open_to_close.exceptions import NetworkError
    
    def handle_network_issues(operation_func, max_retries=3):
        """Handle network connectivity issues."""
        for attempt in range(max_retries):
            try:
                return operation_func()
            except NetworkError as e:
                if attempt < max_retries - 1:
                    delay = 10 * (attempt + 1)  # Linear backoff for network issues
                    print(f"Network error: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
                else:
                    print("Network connectivity could not be established")
                    raise
    ```

---

## 🛡️ Comprehensive Error Handling

### **Complete Error Handling Pattern**

```python
from open_to_close import OpenToCloseAPI
from open_to_close.exceptions import (
    OpenToCloseAPIError,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    NetworkError
)
import time
import logging

logger = logging.getLogger(__name__)

def robust_api_operation(operation_func, *args, **kwargs):
    """
    Execute API operation with comprehensive error handling.
    
    Args:
        operation_func: The API operation function to execute
        *args, **kwargs: Arguments to pass to the operation function
    
    Returns:
        Result of the operation or None if failed
    """
    max_retries = 3
    base_delay = 1
    
    for attempt in range(max_retries):
        try:
            return operation_func(*args, **kwargs)
            
        except AuthenticationError as e:
            logger.error(f"Authentication failed: {e}")
            # Don't retry authentication errors
            break
            
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            # Don't retry validation errors
            break
            
        except NotFoundError as e:
            logger.warning(f"Resource not found: {e}")
            # Don't retry not found errors
            break
            
        except RateLimitError as e:
            if attempt < max_retries - 1:
                delay = getattr(e, 'retry_after', 60)
                logger.warning(f"Rate limited. Waiting {delay}s...")
                time.sleep(delay)
                continue
            else:
                logger.error("Rate limit exceeded after retries")
                break
                
        except (ServerError, NetworkError) as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                logger.warning(f"Temporary error: {e}. Retrying in {delay}s...")
                time.sleep(delay)
                continue
            else:
                logger.error(f"Operation failed after {max_retries} attempts: {e}")
                break
                
        except OpenToCloseAPIError as e:
            logger.error(f"Unexpected API error: {e}")
            break
            
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            break
    
    return None

# Usage examples
def get_property_safely(client, property_id):
    """Safely get a property with full error handling."""
    return robust_api_operation(
        client.properties.retrieve_property,
        property_id
    )

def create_property_safely(client, property_data):
    """Safely create a property with full error handling."""
    return robust_api_operation(
        client.properties.create_property,
        property_data
    )
```

---

## 📊 Error Response Format

When exceptions occur, they may include structured error information:

```python
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid field value",
        "details": {
            "field": "price",
            "value": "invalid",
            "expected": "numeric value"
        },
        "timestamp": "2024-01-15T10:30:00Z"
    }
}
```

**Accessing Error Details:**
```python
try:
    client.properties.create_property(invalid_data)
except ValidationError as e:
    if e.response_data and 'error' in e.response_data:
        error_details = e.response_data['error']
        print(f"Error Code: {error_details.get('code')}")
        print(f"Details: {error_details.get('details', {})}")
```

---

## 🚀 Best Practices

1. **Always catch specific exceptions** rather than the base exception when possible
2. **Implement retry logic** for transient errors (rate limits, server errors, network issues)
3. **Log errors appropriately** with different levels based on severity
4. **Don't retry authentication or validation errors** - these require user intervention
5. **Use exponential backoff** for retries to avoid overwhelming the server
6. **Provide meaningful user feedback** based on the exception type
7. **Monitor exception patterns** to identify systemic issues

---

*Proper exception handling is crucial for building reliable applications. Use these patterns to create robust, user-friendly experiences.* 