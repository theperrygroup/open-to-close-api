# Contributing Guide

We welcome contributions to the Open To Close API Python Client! This guide will help you get started with development, testing, and contributing to the project.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Code Standards](#code-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Standards](#documentation-standards)
- [Submission Process](#submission-process)
- [Release Process](#release-process)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A GitHub account
- Open To Close API key for testing

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork locally:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/open-to-close-api.git
   cd open-to-close-api
   ```

3. **Add upstream remote:**
   ```bash
   git remote add upstream https://github.com/theperry-group/open-to-close-api.git
   ```

## Development Environment

### 1. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install package in editable mode
pip install -e .
```

### 3. Environment Configuration

Create a `.env` file for testing:

```env
OPEN_TO_CLOSE_API_KEY=your_test_api_key_here
```

**⚠️ Never commit your API key to version control**

### 4. Verify Installation

```bash
# Run basic tests
python -c "import open_to_close_api; print('Import successful')"

# Run test suite
pytest tests/
```

## Code Standards

We follow The Perry Group Python Style Guide outlined in `STYLE_GUIDE.md`.

### Key Requirements

1. **Code Formatting:**
   ```bash
   # Format code with Black
   black .
   
   # Sort imports with isort
   isort .
   ```

2. **Type Hints:**
   ```python
   def create_contact(
       self, 
       contact_data: Dict[str, Any]
   ) -> Dict[str, Any]:
       """Create a new contact."""
       # Implementation
   ```

3. **Docstrings:**
   ```python
   def list_contacts(
       self, 
       params: Optional[Dict[str, Any]] = None
   ) -> List[Dict[str, Any]]:
       """Retrieve a list of contacts.

       Args:
           params: Optional dictionary of query parameters for filtering

       Returns:
           A list of dictionaries, where each dictionary represents a contact

       Raises:
           OpenToCloseAPIError: If the API request fails
           ValidationError: If parameters are invalid
           AuthenticationError: If authentication fails

       Example:
           ```python
           # Get all contacts
           contacts = client.contacts.list_contacts()

           # Get contacts with filtering
           contacts = client.contacts.list_contacts(params={"limit": 50})
           ```
       """
   ```

### Pre-commit Hooks

Set up pre-commit hooks to automatically format code:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

## Testing Guidelines

### Test Structure

```
tests/
├── test_base_client.py      # Base client unit tests
├── test_agents.py           # Agents API tests
├── test_contacts.py         # Contacts API tests
├── test_properties.py       # Properties API tests
├── test_additional_apis.py  # Property-related sub-resources
├── test_core_apis.py        # Core API functionality
├── test_exceptions.py       # Exception handling tests
├── test_api_integration.py  # Integration tests with real API
├── test_smoke.py            # Basic smoke tests
└── fixtures/                # Test data and fixtures
    ├── sample_responses.json
    └── ...
```

### Writing Tests

#### Unit Tests
```python
import pytest
from unittest.mock import Mock, patch
from open_to_close_api.contacts import ContactsAPI
from open_to_close_api.exceptions import ValidationError

class TestContactsAPI:
    """Test suite for ContactsAPI."""
    
    def test_list_contacts_success(self, mock_client):
        """Test successful contact listing."""
        # Arrange
        mock_response = [{"id": 1, "first_name": "John", "last_name": "Doe"}]
        mock_client.get.return_value = mock_response
        
        contacts_api = ContactsAPI()
        contacts_api.get = mock_client.get
        
        # Act
        result = contacts_api.list_contacts()
        
        # Assert
        assert result == mock_response
        mock_client.get.assert_called_once_with("/contacts", params=None)
    
    def test_create_contact_validation_error(self, mock_client):
        """Test contact creation with invalid data."""
        # Arrange
        mock_client.post.side_effect = ValidationError("Invalid email format")
        
        contacts_api = ContactsAPI()
        contacts_api.post = mock_client.post
        
        # Act & Assert
        with pytest.raises(ValidationError, match="Invalid email format"):
            contacts_api.create_contact({"email": "invalid-email"})
```

#### Integration Tests
```python
import pytest
from open_to_close_api import OpenToCloseAPI

@pytest.mark.integration
class TestContactsIntegration:
    """Integration tests for contacts API."""
    
    def test_contact_lifecycle(self, api_client):
        """Test complete contact CRUD lifecycle."""
        # Create
        contact_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com"
        }
        
        created_contact = api_client.contacts.create_contact(contact_data)
        assert created_contact["first_name"] == "Test"
        
        # Read
        retrieved_contact = api_client.contacts.retrieve_contact(created_contact["id"])
        assert retrieved_contact["email"] == "test@example.com"
        
        # Update
        updated_contact = api_client.contacts.update_contact(
            created_contact["id"], 
            {"phone": "+1234567890"}
        )
        assert updated_contact["phone"] == "+1234567890"
        
        # Delete
        api_client.contacts.delete_contact(created_contact["id"])
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=open_to_close_api

# Run only unit tests (by marker)
pytest -m "not integration"

# Run only integration tests (by marker)
pytest -m integration

# Run specific test file
pytest tests/unit/test_contacts.py

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "test_contact"
```

### Test Configuration

`pytest.ini`:
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --strict-markers --disable-warnings
markers =
    integration: marks tests as integration tests
    slow: marks tests as slow
```

## Documentation Standards

### Documentation Updates Required

When making code changes, update the corresponding documentation:

#### 1. Code Changes → Docstring Updates
- Update Google-format docstrings with new parameters, return types, or behavior
- Update examples in docstrings
- Add usage examples for new features

#### 2. New Features → Documentation Updates
- Add usage examples to `docs/examples.md`
- Update `docs/api-reference.md` with new endpoint documentation
- Update main `README.md` if it's a major feature
- Add troubleshooting information if applicable

#### 3. Breaking Changes → Migration Documentation
- Update `docs/changelog.md` with migration notes
- Add deprecation warnings and migration guides
- Update version number in `open_to_close_api/__init__.py`

### Documentation Checklist

Before submitting a PR:

- [ ] Updated relevant docstrings
- [ ] Updated examples in affected documentation files
- [ ] Updated API reference if needed
- [ ] Updated changelog if user-facing change
- [ ] Verified all examples still work
- [ ] Updated type hints if signatures changed
- [ ] Added test documentation for new features

## Submission Process

### 1. Create Feature Branch

```bash
# Ensure you're on main
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Changes

1. Write your code following the style guidelines
2. Add comprehensive tests
3. Update documentation
4. Run the test suite

### 3. Commit Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add: New contact filtering capabilities

- Add advanced filtering options for contacts API
- Include support for date range filtering
- Add comprehensive tests for new functionality
- Update documentation with examples"
```

### 4. Quality Checks

Before pushing, run:

```bash
# Code formatting
black .
isort .

# Type checking
mypy open_to_close_api/

# Linting
flake8 open_to_close_api/

# Tests
pytest

# Test coverage
pytest --cov=open_to_close_api --cov-report=html
```

### 5. Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create pull request on GitHub
```

### Pull Request Guidelines

#### PR Title Format
```
Type: Brief description

Examples:
- Add: Contact filtering by date range
- Fix: Handle empty response in property list
- Update: Improve error messages for validation
- Remove: Deprecated authentication method
```

#### PR Description Template
```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that causes existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests pass locally
- [ ] Test coverage maintained/improved

## Documentation
- [ ] Docstrings updated
- [ ] API reference updated
- [ ] Examples updated
- [ ] Changelog updated

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Breaking changes documented
- [ ] Ready for review
```

## Release Process

### Version Management

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Steps

1. **Update Version Numbers:**
   ```python
   # open_to_close_api/__init__.py
   __version__ = "1.2.0"
   ```

2. **Update Changelog:**
   ```markdown
   ## [1.2.0] - 2024-02-01
   
   ### Added
   - Advanced contact filtering capabilities
   - Bulk import utilities
   
   ### Changed
   - Improved error handling for rate limits
   ```

3. **Create Release PR:**
   - Update version numbers
   - Update changelog
   - Update documentation

4. **Tag Release:**
   ```bash
   git tag -a v1.2.0 -m "Release version 1.2.0"
   git push origin v1.2.0
   ```

5. **Publish to PyPI:**
   ```bash
   # Build package
   python -m build
   
   # Upload to PyPI
   twine upload dist/*
   ```

## Getting Help

### Development Questions
- Check existing [issues](https://github.com/theperry-group/open-to-close-api/issues)
- Join our developer discussions
- Contact the maintainers

### Reporting Issues
When reporting bugs, include:
- Python version
- Library version
- Minimal reproduction case
- Error messages and traceback
- Expected vs actual behavior

### Feature Requests
When requesting features:
- Describe the use case
- Provide examples of how it would be used
- Consider backward compatibility
- Suggest implementation approach

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read and follow our Code of Conduct.

## Recognition

Contributors will be recognized in:
- Release notes
- Contributors section of README
- GitHub contributors list

Thank you for contributing to the Open To Close API Python Client! 