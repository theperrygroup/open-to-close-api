# The Perry Group Python Style Guide

This document outlines the coding standards and practices for the Perry Group Django projects. Following these guidelines ensures consistent, maintainable, and high-quality code.

## General Principles

- **Readability**: Code should be easily readable by others
- **Consistency**: Follow established patterns in the codebase
- **Simplicity**: Prefer simpler solutions over complex ones
- **Documentation**: Document code thoroughly with docstrings
- **Type Safety**: Use type hints for all function parameters and return values

## Code Organization

### File Structure

- One class per file when possible (with exceptions for closely related small classes)
- Group related functionality in modules
- Follow Django's app-based organization

### Import Order

1. Python standard library imports
2. Django and third-party imports
3. Local application imports
4. Import specific classes/functions rather than modules where practical

Example:
```python
import re
import logging
from datetime import datetime
from typing import Dict, Optional

from django.db import models
from django.conf import settings
from bs4 import BeautifulSoup

from apps.core.helpers import clean_phone, clean_email
from apps.opendoor_leads.models import OpendoorLead
```

## Code Style

### Class Structure

- Use object-oriented design principles
- Break large classes into smaller, focused ones
- Follow single responsibility principle

```python
class LeadExtractor:
    """Extract lead data from external sources."""
    
    @staticmethod
    def extract_data(source_data: Dict) -> Dict:
        """Extract normalized lead data from source."""
        # Implementation
```

### Method Organization

- Public methods first, followed by private methods
- Group related methods together
- Use descriptive method names

### Naming Conventions

- **Classes**: `PascalCase`
- **Functions/Methods**: `snake_case`
- **Variables**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods/attributes**: Prefix with underscore `_private_method`

## Type Hints

Use comprehensive type hints for all function/method signatures:

```python
def process_lead(
    lead_data: Dict[str, str], 
    reference_id: str,
    create_date: Optional[datetime] = None
) -> Optional[Lead]:
    """Process lead data and create a Lead object if valid."""
    # Implementation
```

## Docstrings

Use Google-style docstrings for all public methods, functions, and classes:

```python
def clean_phone(phone: str) -> str:
    """Clean and standardize phone number format.
    
    Args:
        phone: Raw phone number string
        
    Returns:
        Cleaned phone number in format (XXX) XXX-XXXX
        
    Raises:
        ValueError: If the phone number is invalid
    """
    # Implementation
```

## Error Handling

- Use specific exception types
- Always log exceptions with context
- Handle errors at appropriate levels

```python
try:
    result = process_data(data)
except ValueError as e:
    logger.error(f"Invalid data format: {e}")
    return None
except ConnectionError as e:
    logger.error(f"Failed to connect: {e}")
    raise ServiceUnavailableError(f"Service unavailable: {e}")
```

## Testing

- Write tests for all new functionality
- Use descriptive test method names that explain what they test
- Separate unit tests from integration tests

## Tools and Enforcement

This project uses the following tools to enforce style:

1. **Black**: For code formatting
2. **isort**: For import sorting
3. **mypy**: For type checking
4. **flake8**: For linting
5. **pylint**: For deeper code analysis

Configuration files for these tools are in the project root.

## Models and Database

- Always define `__str__` method for models
- Include docstrings for model classes and complex fields
- Use appropriate field types and validators
- Add Meta classes with proper ordering and constraints

## Django-Specific Guidelines

### Views
- Use class-based views when appropriate
- Keep view logic minimal, move business logic to services

### Templates
- Use consistent naming for templates
- Keep templates DRY with proper inheritance

### Forms
- Add validation in form classes, not in views
- Use model forms when appropriate

## Git Commits

- Write descriptive commit messages
- Use present tense ("Add feature" not "Added feature")
- Reference issue numbers in commit messages 