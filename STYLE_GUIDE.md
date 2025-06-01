# Open To Close API Client Style Guide

This document outlines the coding standards and practices for the Open To Close API Python client library. Following these guidelines ensures consistent, maintainable, and high-quality code.

## General Principles

- **Readability**: Code should be easily readable by others
- **Consistency**: Follow established patterns in the codebase
- **Simplicity**: Prefer simpler solutions over complex ones
- **Documentation**: Document code thoroughly with Google-style docstrings
- **Type Safety**: Use comprehensive type hints for all function parameters and return values
- **API-First Design**: Structure code around API endpoints and resources

## Code Organization

### File Structure

- One API resource class per file (e.g., `contacts.py`, `properties.py`)
- Group related functionality in modules
- Follow resource-based organization matching API structure
- Keep base functionality in `base_client.py`
- Centralize exceptions in `exceptions.py`

### Import Order

1. Python standard library imports
2. Third-party imports (requests, etc.)
3. Local application imports
4. Import specific classes/functions rather than modules where practical

Example:
```python
import logging
from typing import Dict, List, Optional, Union
from datetime import datetime

import requests
from requests.exceptions import RequestException

from .base_client import BaseClient
from .exceptions import AuthenticationError, ValidationError
```

## API Client Design Patterns

### Resource Classes

- Each API resource should have its own class
- Inherit from `BaseClient` for common functionality
- Follow RESTful method naming: `list_*`, `create_*`, `retrieve_*`, `update_*`, `delete_*`

```python
class ContactsAPI(BaseClient):
    """API client for contact management endpoints."""
    
    def list_contacts(self, **params) -> List[Dict]:
        """List all contacts with optional filtering."""
        return self._get("/v1/contacts", params=params)
    
    def create_contact(self, contact_data: Dict) -> Dict:
        """Create a new contact."""
        return self._post("/v1/contacts", json=contact_data)
```

### Method Organization

- CRUD methods first (list, create, retrieve, update, delete)
- Utility methods after CRUD operations
- Private methods last
- Group related methods together

### Naming Conventions

- **Classes**: `PascalCase` ending with `API` (e.g., `ContactsAPI`)
- **Methods**: `snake_case` with descriptive verbs (`list_contacts`, `create_property`)
- **Variables**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods/attributes**: Prefix with underscore `_private_method`

## Type Hints

Use comprehensive type hints for all function/method signatures:

```python
def create_contact(
    self,
    contact_data: Dict[str, Union[str, int, float]],
    validate: bool = True
) -> Dict[str, Any]:
    """Create a new contact with validation."""
    # Implementation
```

## Docstrings

Use Google-style docstrings for all public methods, functions, and classes:

```python
def list_properties(
    self,
    status: Optional[str] = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """List properties with optional filtering.
    
    Args:
        status: Filter by property status (e.g., 'active', 'closed')
        limit: Maximum number of properties to return
        
    Returns:
        List of property dictionaries containing property data
        
    Raises:
        AuthenticationError: If API key is invalid
        ValidationError: If parameters are invalid
        
    Example:
        >>> client = OpenToCloseAPI()
        >>> properties = client.properties.list_properties(status='active', limit=50)
        >>> print(f"Found {len(properties)} active properties")
    """
    # Implementation
```

## Error Handling

- Use specific exception types for different error conditions
- Always log exceptions with context
- Provide helpful error messages
- Handle API rate limiting gracefully

```python
try:
    response = self._request("GET", endpoint)
    return response.json()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        raise AuthenticationError("Invalid API key")
    elif e.response.status_code == 422:
        raise ValidationError(f"Invalid request data: {e.response.text}")
    else:
        raise APIError(f"Request failed: {e}")
```

## API Response Handling

- Always validate API responses
- Handle both list and paginated responses consistently
- Normalize response formats when needed

```python
def _handle_response(self, response: requests.Response) -> Dict:
    """Handle API response and extract data."""
    try:
        data = response.json()
        # Handle paginated responses
        if isinstance(data, dict) and 'data' in data:
            return data['data']
        return data
    except ValueError:
        raise APIError("Invalid JSON response from API")
```

## Testing

- Write tests for all public methods
- Use mock responses for external API calls
- Test error conditions and edge cases
- Separate unit tests from integration tests

```python
def test_list_contacts_success(self, mock_get):
    """Test successful contact listing."""
    mock_get.return_value.json.return_value = [{"id": 1, "name": "John"}]
    
    client = ContactsAPI()
    contacts = client.list_contacts()
    
    assert len(contacts) == 1
    assert contacts[0]["name"] == "John"
```

## Configuration and Environment

- Use environment variables for API keys and configuration
- Provide sensible defaults
- Support both `.env` files and direct environment variables

```python
class OpenToCloseAPI:
    """Main API client."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.opentoclose.com"
    ):
        self.api_key = api_key or os.getenv("OPEN_TO_CLOSE_API_KEY")
        if not self.api_key:
            raise AuthenticationError("API key is required")
```

## Tools and Enforcement

This project uses the following tools to enforce style:

1. **Black**: For code formatting (line length 88)
2. **isort**: For import sorting (profile: black)
3. **mypy**: For type checking (strict mode)
4. **flake8**: For linting
5. **pylint**: For deeper code analysis
6. **pytest**: For testing with 100% coverage requirement

## Documentation Standards

- All public APIs must have comprehensive docstrings
- Include usage examples in docstrings
- Keep README.md updated with latest API changes
- Use MkDocs for comprehensive documentation
- Update changelog for all breaking changes

## Version Management

- Follow semantic versioning (MAJOR.MINOR.PATCH)
- Update version in `__init__.py`, `pyproject.toml`, and `setup.py`
- Tag releases in git
- Maintain backward compatibility in minor versions

## Git Commits

- Write descriptive commit messages
- Use present tense ("Add feature" not "Added feature")
- Reference issue numbers in commit messages
- Keep commits focused and atomic 