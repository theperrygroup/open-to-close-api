# Best Practices Guide

Comprehensive guide to best practices for developing with the Open To Close API Python client. Follow these recommendations to build robust, maintainable, and efficient applications.

!!! abstract "Best Practices Philosophy"
    Good practices lead to reliable applications, easier maintenance, and better user experiences. This guide covers patterns learned from real-world usage.

---

## 🚀 Getting Started Right

### **Project Structure**

Organize your code for maintainability:

```
your_project/
├── config/
│   ├── __init__.py
│   └── settings.py          # Configuration management
├── services/
│   ├── __init__.py
│   ├── api_client.py        # API client wrapper
│   ├── property_service.py  # Property operations
│   └── contact_service.py   # Contact operations
├── models/
│   ├── __init__.py
│   ├── property.py          # Data models
│   └── contact.py
├── utils/
│   ├── __init__.py
│   ├── error_handler.py     # Error handling utilities
│   └── validators.py       # Data validation
└── main.py
```

### **Configuration Management**

```python
# config/settings.py
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class APIConfig:
    api_key: str
    base_url: str = "https://api.opentoclose.com/v1"
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    
    @classmethod
    def from_environment(cls) -> 'APIConfig':
        """Load configuration from environment variables."""
        api_key = os.getenv("OPEN_TO_CLOSE_API_KEY")
        if not api_key:
            raise ValueError("OPEN_TO_CLOSE_API_KEY environment variable required")
            
        return cls(
            api_key=api_key,
            base_url=os.getenv("OPEN_TO_CLOSE_BASE_URL", cls.base_url),
            timeout=int(os.getenv("OPEN_TO_CLOSE_TIMEOUT", cls.timeout)),
            max_retries=int(os.getenv("OPEN_TO_CLOSE_MAX_RETRIES", cls.max_retries)),
            retry_delay=float(os.getenv("OPEN_TO_CLOSE_RETRY_DELAY", cls.retry_delay))
        )
    
    def validate(self) -> None:
        """Validate configuration values."""
        if not self.api_key:
            raise ValueError("API key cannot be empty")
        if self.timeout <= 0:
            raise ValueError("Timeout must be positive")
        if self.max_retries < 0:
            raise ValueError("Max retries cannot be negative")
```

---

## 🛡️ Error Handling Best Practices

### **Hierarchical Error Handling**

```python
# services/api_client.py
import logging
from typing import Dict, Any, Optional, Callable
from open_to_close import OpenToCloseAPI
from open_to_close.exceptions import *
from config.settings import APIConfig

logger = logging.getLogger(__name__)

class APIClient:
    """Production-ready API client wrapper."""
    
    def __init__(self, config: APIConfig):
        self.config = config
        self._client = None
        
    @property
    def client(self) -> OpenToCloseAPI:
        """Lazy-loaded client instance."""
        if self._client is None:
            self._client = OpenToCloseAPI(
                api_key=self.config.api_key,
                base_url=self.config.base_url
            )
        return self._client
    
    def execute_with_retry(self, 
                          operation: Callable,
                          operation_name: str,
                          *args, 
                          **kwargs) -> Dict[str, Any]:
        """Execute API operation with comprehensive error handling."""
        
        for attempt in range(self.config.max_retries + 1):
            try:
                result = operation(*args, **kwargs)
                return {
                    "success": True,
                    "data": result,
                    "attempts": attempt + 1
                }
                
            except AuthenticationError as e:
                logger.error(f"Authentication failed for {operation_name}: {e}")
                return self._create_error_response("authentication_failed", str(e), False)
                
            except ValidationError as e:
                logger.error(f"Validation failed for {operation_name}: {e}")
                return self._create_error_response("validation_failed", str(e), False)
                
            except NotFoundError as e:
                logger.warning(f"Resource not found for {operation_name}: {e}")
                return self._create_error_response("not_found", str(e), False)
                
            except RateLimitError as e:
                if attempt < self.config.max_retries:
                    delay = getattr(e, 'retry_after', self.config.retry_delay * (2 ** attempt))
                    logger.warning(f"Rate limited, retrying in {delay}s...")
                    time.sleep(delay)
                    continue
                else:
                    return self._create_error_response("rate_limited", str(e), True)
                    
            except (ServerError, NetworkError) as e:
                if attempt < self.config.max_retries:
                    delay = self.config.retry_delay * (2 ** attempt)
                    logger.warning(f"Temporary error, retrying in {delay}s...")
                    time.sleep(delay)
                    continue
                else:
                    return self._create_error_response("server_error", str(e), True)
                    
        return self._create_error_response("max_retries_exceeded", "Operation failed", False)
    
    def _create_error_response(self, error_type: str, message: str, retry_recommended: bool) -> Dict[str, Any]:
        """Create standardized error response."""
        return {
            "success": False,
            "error": error_type,
            "message": message,
            "retry_recommended": retry_recommended
        }
```

### **Service Layer Pattern**

```python
# services/property_service.py
from typing import List, Dict, Any, Optional
from .api_client import APIClient
from models.property import Property

class PropertyService:
    """Service layer for property operations."""
    
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        
    def get_property(self, property_id: int) -> Optional[Property]:
        """Get a single property with error handling."""
        response = self.api_client.execute_with_retry(
            self.api_client.client.properties.retrieve_property,
            "get_property",
            property_id
        )
        
        if response["success"]:
            return Property.from_dict(response["data"])
        else:
            self._handle_error(response, f"Failed to get property {property_id}")
            return None
    
    def create_property(self, property_data: Dict[str, Any]) -> Optional[Property]:
        """Create property with validation."""
        # Validate data before API call
        validation_errors = self._validate_property_data(property_data)
        if validation_errors:
            logger.error(f"Property validation failed: {validation_errors}")
            return None
            
        response = self.api_client.execute_with_retry(
            self.api_client.client.properties.create_property,
            "create_property", 
            property_data
        )
        
        if response["success"]:
            return Property.from_dict(response["data"])
        else:
            self._handle_error(response, "Failed to create property")
            return None
    
    def get_properties_batch(self, property_ids: List[int]) -> List[Property]:
        """Get multiple properties efficiently."""
        properties = []
        
        # Process in batches to avoid overwhelming the API
        batch_size = 10
        for i in range(0, len(property_ids), batch_size):
            batch = property_ids[i:i + batch_size]
            
            for prop_id in batch:
                prop = self.get_property(prop_id)
                if prop:
                    properties.append(prop)
                    
            # Rate limiting between batches
            if i + batch_size < len(property_ids):
                time.sleep(0.5)
                
        return properties
    
    def _validate_property_data(self, data: Dict[str, Any]) -> List[str]:
        """Validate property data before API submission."""
        errors = []
        
        required_fields = ["address", "city", "state"]
        for field in required_fields:
            if not data.get(field):
                errors.append(f"Missing required field: {field}")
                
        if "price" in data:
            try:
                price = float(data["price"])
                if price < 0:
                    errors.append("Price cannot be negative")
            except (ValueError, TypeError):
                errors.append("Price must be a valid number")
                
        return errors
    
    def _handle_error(self, response: Dict[str, Any], context: str):
        """Handle and log service errors."""
        logger.error(f"{context}: {response.get('error', 'Unknown error')}")
        
        # Could also publish to error tracking service
        # error_tracker.record_error(response, context)
```

---

## 📊 Data Management Best Practices

### **Data Models**

```python
# models/property.py
from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime

@dataclass
class Property:
    """Property data model with validation."""
    id: Optional[int] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    price: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    square_feet: Optional[int] = None
    property_type: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Property':
        """Create Property from API response data."""
        # Handle datetime parsing
        created_at = None
        if data.get('created_at'):
            created_at = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
            
        updated_at = None
        if data.get('updated_at'):
            updated_at = datetime.fromisoformat(data['updated_at'].replace('Z', '+00:00'))
        
        return cls(
            id=data.get('id'),
            address=data.get('address'),
            city=data.get('city'),
            state=data.get('state'),
            zip_code=data.get('zip_code'),
            price=data.get('price'),
            bedrooms=data.get('bedrooms'),
            bathrooms=data.get('bathrooms'),
            square_feet=data.get('square_feet'),
            property_type=data.get('property_type'),
            status=data.get('status'),
            created_at=created_at,
            updated_at=updated_at
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Property to dictionary for API submission."""
        data = {}
        
        for field, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, datetime):
                    data[field] = value.isoformat()
                else:
                    data[field] = value
                    
        return data
    
    def validate(self) -> List[str]:
        """Validate property data."""
        errors = []
        
        if not self.address:
            errors.append("Address is required")
        if not self.city:
            errors.append("City is required")
        if not self.state:
            errors.append("State is required")
            
        if self.price is not None and self.price < 0:
            errors.append("Price cannot be negative")
            
        if self.bedrooms is not None and self.bedrooms < 0:
            errors.append("Bedrooms cannot be negative")
            
        return errors
```

### **Caching Strategy**

```python
# utils/cache.py
import time
from typing import Dict, Any, Optional, Callable
from functools import wraps

class SimpleCache:
    """Simple in-memory cache with TTL."""
    
    def __init__(self, default_ttl: int = 300):  # 5 minutes
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        if key in self.cache:
            entry = self.cache[key]
            if time.time() < entry['expires_at']:
                return entry['value']
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache with TTL."""
        ttl = ttl or self.default_ttl
        self.cache[key] = {
            'value': value,
            'expires_at': time.time() + ttl
        }
    
    def invalidate(self, key: str) -> None:
        """Remove key from cache."""
        self.cache.pop(key, None)
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()

# Cache decorator
def cached(ttl: int = 300, key_func: Optional[Callable] = None):
    """Decorator to cache function results."""
    def decorator(func):
        cache = SimpleCache(ttl)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = f"{func.__name__}:{str(args)}:{str(sorted(kwargs.items()))}"
            
            # Check cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result)
            return result
            
        wrapper.cache = cache  # Expose cache for manual management
        return wrapper
    return decorator

# Usage in service
class PropertyService:
    @cached(ttl=600)  # Cache for 10 minutes
    def get_property(self, property_id: int) -> Optional[Property]:
        # Implementation...
        pass
```

---

## ⚡ Performance Best Practices

### **Batch Operations**

```python
# utils/batch_processor.py
import time
import asyncio
from typing import List, Callable, Any, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

class BatchProcessor:
    """Efficient batch processing with rate limiting."""
    
    def __init__(self, 
                 batch_size: int = 10,
                 delay_between_batches: float = 0.5,
                 max_workers: int = 5):
        self.batch_size = batch_size
        self.delay_between_batches = delay_between_batches
        self.max_workers = max_workers
    
    def process_sequential(self, 
                          items: List[Any], 
                          processor: Callable[[Any], Any]) -> List[Any]:
        """Process items sequentially with rate limiting."""
        results = []
        
        for i in range(0, len(items), self.batch_size):
            batch = items[i:i + self.batch_size]
            
            batch_results = []
            for item in batch:
                try:
                    result = processor(item)
                    batch_results.append(result)
                except Exception as e:
                    logger.error(f"Error processing item {item}: {e}")
                    batch_results.append(None)
            
            results.extend(batch_results)
            
            # Rate limiting between batches
            if i + self.batch_size < len(items):
                time.sleep(self.delay_between_batches)
        
        return results
    
    def process_parallel(self, 
                        items: List[Any], 
                        processor: Callable[[Any], Any]) -> List[Any]:
        """Process items in parallel with controlled concurrency."""
        results = [None] * len(items)
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_index = {
                executor.submit(processor, item): i 
                for i, item in enumerate(items)
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    results[index] = future.result()
                except Exception as e:
                    logger.error(f"Error processing item at index {index}: {e}")
                    results[index] = None
        
        return results

# Usage example
def bulk_update_properties(property_updates: List[Dict[str, Any]]):
    """Efficiently update multiple properties."""
    processor = BatchProcessor(batch_size=5, delay_between_batches=1.0)
    
    def update_property(update_data):
        property_id = update_data['id']
        data = update_data['data']
        return property_service.update_property(property_id, data)
    
    return processor.process_sequential(property_updates, update_property)
```

### **Resource Management**

```python
# utils/resource_manager.py
import contextlib
from typing import Generator
from services.api_client import APIClient
from config.settings import APIConfig

@contextlib.contextmanager
def api_client_context(config: APIConfig) -> Generator[APIClient, None, None]:
    """Context manager for API client resource management."""
    client = APIClient(config)
    try:
        yield client
    except Exception as e:
        logger.error(f"API client error: {e}")
        raise
    finally:
        # Cleanup if needed (close connections, etc.)
        pass

# Usage
def process_properties():
    config = APIConfig.from_environment()
    
    with api_client_context(config) as client:
        property_service = PropertyService(client)
        
        # Use the service
        properties = property_service.get_properties_batch([1, 2, 3, 4, 5])
        return properties
```

---

## 🔒 Security Best Practices

### **API Key Management**

```python
# utils/security.py
import os
import keyring
from typing import Optional

class SecureConfig:
    """Secure configuration management."""
    
    def __init__(self, service_name: str = "open_to_close_api"):
        self.service_name = service_name
    
    def get_api_key(self) -> str:
        """Get API key from secure storage."""
        # Try environment variable first
        api_key = os.getenv("OPEN_TO_CLOSE_API_KEY")
        if api_key:
            return api_key
        
        # Try system keyring
        try:
            api_key = keyring.get_password(self.service_name, "api_key")
            if api_key:
                return api_key
        except Exception as e:
            logger.warning(f"Failed to get API key from keyring: {e}")
        
        raise ValueError("API key not found in environment or keyring")
    
    def set_api_key(self, api_key: str) -> None:
        """Store API key in secure storage."""
        try:
            keyring.set_password(self.service_name, "api_key", api_key)
        except Exception as e:
            logger.error(f"Failed to store API key in keyring: {e}")
            raise
    
    def validate_api_key_format(self, api_key: str) -> bool:
        """Validate API key format."""
        if not api_key:
            return False
        if len(api_key) < 50:  # Basic length check
            return False
        # Add more validation as needed
        return True

# Usage
secure_config = SecureConfig()
api_key = secure_config.get_api_key()
```

### **Input Validation**

```python
# utils/validators.py
import re
from typing import Dict, Any, List

class PropertyValidator:
    """Comprehensive property data validation."""
    
    @staticmethod
    def validate_address(address: str) -> List[str]:
        """Validate address format."""
        errors = []
        
        if not address or not address.strip():
            errors.append("Address cannot be empty")
        elif len(address.strip()) < 5:
            errors.append("Address too short")
        elif len(address) > 200:
            errors.append("Address too long")
            
        return errors
    
    @staticmethod
    def validate_price(price: Any) -> List[str]:
        """Validate price value."""
        errors = []
        
        if price is None:
            return errors  # Price is optional
            
        try:
            price_float = float(price)
            if price_float < 0:
                errors.append("Price cannot be negative")
            elif price_float > 1_000_000_000:  # 1 billion
                errors.append("Price unreasonably high")
        except (ValueError, TypeError):
            errors.append("Price must be a valid number")
            
        return errors
    
    @staticmethod
    def validate_email(email: str) -> List[str]:
        """Validate email format."""
        errors = []
        
        if not email:
            return errors  # Email is optional
            
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            errors.append("Invalid email format")
            
        return errors
    
    @classmethod
    def validate_property_data(cls, data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate complete property data."""
        all_errors = {}
        
        # Validate individual fields
        if 'address' in data:
            errors = cls.validate_address(data['address'])
            if errors:
                all_errors['address'] = errors
        
        if 'price' in data:
            errors = cls.validate_price(data['price'])
            if errors:
                all_errors['price'] = errors
                
        # Add more field validations as needed
        
        return all_errors
```

---

## 🧪 Testing Best Practices

### **Unit Testing**

```python
# tests/test_property_service.py
import unittest
from unittest.mock import Mock, patch
from services.property_service import PropertyService
from services.api_client import APIClient
from models.property import Property

class TestPropertyService(unittest.TestCase):
    """Test cases for PropertyService."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_api_client = Mock(spec=APIClient)
        self.property_service = PropertyService(self.mock_api_client)
    
    def test_get_property_success(self):
        """Test successful property retrieval."""
        # Arrange
        property_data = {
            'id': 123,
            'address': '123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'price': 500000
        }
        
        self.mock_api_client.execute_with_retry.return_value = {
            'success': True,
            'data': property_data
        }
        
        # Act
        result = self.property_service.get_property(123)
        
        # Assert
        self.assertIsInstance(result, Property)
        self.assertEqual(result.id, 123)
        self.assertEqual(result.address, '123 Main St')
        self.mock_api_client.execute_with_retry.assert_called_once()
    
    def test_get_property_not_found(self):
        """Test property not found scenario."""
        # Arrange
        self.mock_api_client.execute_with_retry.return_value = {
            'success': False,
            'error': 'not_found',
            'message': 'Property not found'
        }
        
        # Act
        result = self.property_service.get_property(999)
        
        # Assert
        self.assertIsNone(result)
    
    def test_create_property_validation_error(self):
        """Test property creation with validation errors."""
        # Arrange
        invalid_data = {
            'address': '',  # Invalid empty address
            'price': -1000  # Invalid negative price
        }
        
        # Act
        result = self.property_service.create_property(invalid_data)
        
        # Assert
        self.assertIsNone(result)
        # Should not call API due to validation failure
        self.mock_api_client.execute_with_retry.assert_not_called()

class TestPropertyModel(unittest.TestCase):
    """Test cases for Property model."""
    
    def test_from_dict(self):
        """Test Property creation from dictionary."""
        data = {
            'id': 123,
            'address': '123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'price': 500000,
            'created_at': '2024-01-15T10:30:00Z'
        }
        
        property_obj = Property.from_dict(data)
        
        self.assertEqual(property_obj.id, 123)
        self.assertEqual(property_obj.address, '123 Main St')
        self.assertIsNotNone(property_obj.created_at)
    
    def test_validation(self):
        """Test property validation."""
        property_obj = Property(
            address='',  # Invalid
            city='Test City',
            state='CA',
            price=-1000  # Invalid
        )
        
        errors = property_obj.validate()
        
        self.assertIn('Address is required', errors)
        self.assertIn('Price cannot be negative', errors)
```

### **Integration Testing**

```python
# tests/test_integration.py
import unittest
import os
from services.api_client import APIClient
from services.property_service import PropertyService
from config.settings import APIConfig

class TestAPIIntegration(unittest.TestCase):
    """Integration tests with real API (use test environment)."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        # Only run if test API key is available
        test_api_key = os.getenv("OPEN_TO_CLOSE_TEST_API_KEY")
        if not test_api_key:
            raise unittest.SkipTest("Test API key not available")
        
        config = APIConfig(
            api_key=test_api_key,
            base_url="https://test-api.opentoclose.com/v1"
        )
        
        cls.api_client = APIClient(config)
        cls.property_service = PropertyService(cls.api_client)
    
    def test_full_property_lifecycle(self):
        """Test complete property CRUD operations."""
        # Create property
        property_data = {
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'CA',
            'price': 500000
        }
        
        created_property = self.property_service.create_property(property_data)
        self.assertIsNotNone(created_property)
        self.assertIsNotNone(created_property.id)
        
        # Retrieve property
        retrieved_property = self.property_service.get_property(created_property.id)
        self.assertIsNotNone(retrieved_property)
        self.assertEqual(retrieved_property.address, property_data['address'])
        
        # Update property
        updated_data = {'price': 550000}
        updated_property = self.property_service.update_property(
            created_property.id, 
            updated_data
        )
        self.assertIsNotNone(updated_property)
        self.assertEqual(updated_property.price, 550000)
        
        # Delete property (cleanup)
        success = self.property_service.delete_property(created_property.id)
        self.assertTrue(success)
```

---

## 📚 Documentation Best Practices

### **Code Documentation**

```python
def create_property_with_contacts(
    property_data: Dict[str, Any],
    contacts: List[Dict[str, Any]],
    validate_data: bool = True
) -> Optional[Property]:
    """
    Create a property and associate contacts in a single transaction.
    
    This method creates a property and then associates the provided contacts
    with appropriate roles. If any step fails, it attempts to rollback changes.
    
    Args:
        property_data: Dictionary containing property information. Must include
            'address', 'city', and 'state' fields.
        contacts: List of contact dictionaries. Each contact should have
            'contact_id' and 'role' fields.
        validate_data: Whether to perform client-side validation before
            API calls. Defaults to True.
    
    Returns:
        Property object if successful, None if failed.
    
    Raises:
        ValueError: If required fields are missing from property_data.
        ValidationError: If data validation fails and validate_data is True.
    
    Example:
        >>> property_data = {
        ...     'address': '123 Main St',
        ...     'city': 'Anytown',
        ...     'state': 'CA',
        ...     'price': 500000
        ... }
        >>> contacts = [
        ...     {'contact_id': 101, 'role': 'Buyer'},
        ...     {'contact_id': 201, 'role': 'Seller'}
        ... ]
        >>> property_obj = create_property_with_contacts(property_data, contacts)
        >>> print(f"Created property {property_obj.id}")
    """
    # Implementation...
    pass
```

---

## 🚀 Summary of Best Practices

### **Code Organization**
- Use clear project structure with separation of concerns
- Implement service layer pattern for business logic
- Create reusable data models with validation
- Use dependency injection for better testability

### **Error Handling**
- Implement comprehensive exception handling
- Use retry logic for transient errors
- Provide meaningful error messages
- Log errors with sufficient context

### **Performance**
- Use caching for frequently accessed data
- Implement batch processing for bulk operations
- Add rate limiting to avoid API overwhelm
- Monitor and optimize slow operations

### **Security**
- Secure API key storage and access
- Validate all input data
- Use HTTPS for all communications
- Implement proper authentication handling

### **Testing**
- Write comprehensive unit tests
- Include integration tests for critical paths
- Mock external dependencies in unit tests
- Test error scenarios thoroughly

### **Monitoring**
- Log all API operations
- Track error rates and patterns
- Monitor performance metrics
- Set up alerting for critical issues

---

## 📚 Related Resources

- **[Error Handling Guide](error-handling.md)** - Comprehensive error handling patterns
- **[Examples](examples.md)** - Real-world code examples
- **[API Reference](../api/index.md)** - Complete API documentation

---

*Following these best practices will help you build robust, maintainable applications with the Open To Close API.* 