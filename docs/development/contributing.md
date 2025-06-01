# Contributing Guide

Thank you for your interest in contributing to the Open To Close API Python client! This guide will help you get started with contributing to the project, whether you're fixing bugs, adding features, or improving documentation.

## 🤝 How to Contribute

We welcome contributions of all kinds:

- **Bug Reports**: Help us identify and fix issues
- **Feature Requests**: Suggest new functionality
- **Code Contributions**: Submit bug fixes and new features
- **Documentation**: Improve guides, examples, and API docs
- **Testing**: Add test cases and improve coverage
- **Performance**: Optimize code and identify bottlenecks

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** (we support Python 3.8, 3.9, 3.10, 3.11, 3.12)
- **Git** for version control
- **GitHub account** for submitting contributions

### Development Setup

1. **Fork the Repository**
   ```bash
   # Fork the repo on GitHub, then clone your fork
   git clone https://github.com/YOUR-USERNAME/open-to-close.git
   cd open-to-close
   ```

2. **Set Up Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate it
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Development Dependencies**
   ```bash
   # Install package in development mode with all dependencies
   pip install -e ".[dev,docs,test]"
   
   # Install pre-commit hooks
   pre-commit install
   ```

4. **Verify Setup**
   ```bash
   # Run tests to ensure everything works
   pytest
   
   # Run linting
   make lint
   
   # Build documentation
   mkdocs serve
   ```

### Development Dependencies

The project uses several development tools:

| Tool | Purpose | Configuration |
|------|---------|---------------|
| **pytest** | Testing framework | `pytest.ini` |
| **pytest-cov** | Coverage reporting | `pytest.ini` |
| **black** | Code formatting | `pyproject.toml` |
| **isort** | Import sorting | `pyproject.toml` |
| **flake8** | Linting | `.flake8` |
| **mypy** | Type checking | `mypy.ini` |
| **pre-commit** | Git hooks | `.pre-commit-config.yaml` |
| **mkdocs** | Documentation | `mkdocs.yml` |

---

## 📝 Code Style and Standards

### Python Code Style

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length**: 88 characters (Black default)
- **Quotes**: Double quotes for strings
- **Imports**: Sorted with isort
- **Type hints**: Required for all public APIs
- **Docstrings**: Google style for all public functions/classes

### Code Formatting

We use **Black** for automatic code formatting:

```bash
# Format all code
black open_to_close tests

# Check formatting without changes
black --check open_to_close tests
```

### Import Sorting

We use **isort** to organize imports:

```bash
# Sort imports
isort open_to_close tests

# Check import sorting
isort --check-only open_to_close tests
```

### Linting

We use **flake8** for linting:

```bash
# Run linting
flake8 open_to_close tests

# With specific rules
flake8 --select=E,W,F open_to_close
```

### Type Checking

We use **mypy** for static type checking:

```bash
# Run type checking
mypy open_to_close

# With strict mode
mypy --strict open_to_close
```

### Pre-commit Hooks

We use pre-commit hooks to ensure code quality:

```bash
# Install hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files

# Update hooks
pre-commit autoupdate
```

---

## 🧪 Testing Guidelines

### Testing Philosophy

- **Comprehensive Coverage**: Aim for >95% test coverage
- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test API interactions
- **Mock External Dependencies**: Use mocks for HTTP requests
- **Test Edge Cases**: Include error conditions and boundary cases

### Writing Tests

#### Test Structure

```python
"""Test module for properties API."""

import pytest
from unittest.mock import Mock, patch

from open_to_close import OpenToCloseAPI
from open_to_close.exceptions import NotFoundError, ValidationError


class TestPropertiesAPI:
    """Test cases for Properties API."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = OpenToCloseAPI(api_key="test-key")
    
    def test_list_properties_success(self, mock_response):
        """Test successful property listing."""
        # Arrange
        expected_data = [{"id": 1, "address": "123 Main St"}]
        mock_response.json.return_value = {"data": expected_data}
        
        # Act
        with patch('requests.get', return_value=mock_response):
            result = self.client.properties.list_properties()
        
        # Assert
        assert result == expected_data
    
    def test_create_property_validation_error(self):
        """Test property creation with invalid data."""
        # Arrange
        invalid_data = {"address": ""}  # Empty address
        
        # Act & Assert
        with pytest.raises(ValidationError):
            self.client.properties.create_property(invalid_data)
```

#### Test Fixtures

Use `conftest.py` for shared fixtures:

```python
"""Shared test fixtures."""

import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_response():
    """Mock HTTP response."""
    response = Mock()
    response.status_code = 200
    response.headers = {'Content-Type': 'application/json'}
    response.json.return_value = {"data": {}}
    return response


@pytest.fixture
def sample_property():
    """Sample property data."""
    return {
        "id": 123,
        "address": "123 Main Street",
        "city": "San Francisco",
        "state": "CA",
        "zip_code": "94102",
        "listing_price": 850000
    }
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=open_to_close --cov-report=html

# Run specific test file
pytest tests/test_properties.py

# Run specific test method
pytest tests/test_properties.py::TestPropertiesAPI::test_list_properties

# Run tests matching pattern
pytest -k "test_create"

# Run with verbose output
pytest -v

# Run with debugging
pytest -s --pdb
```

### Test Coverage

We maintain high test coverage:

```bash
# Generate coverage report
pytest --cov=open_to_close --cov-report=html

# View coverage in browser
open htmlcov/index.html

# Coverage requirements
# - Overall coverage: ≥95%
# - New code coverage: 100%
# - No untested code in critical paths
```

---

## 📚 Documentation Guidelines

### Documentation Types

1. **API Reference**: Auto-generated from docstrings
2. **User Guides**: Step-by-step tutorials and examples
3. **Reference Materials**: Data types, error codes, etc.
4. **Development Docs**: Contributing, testing, release process

### Writing Documentation

#### Docstring Format

We use Google-style docstrings:

```python
def create_property(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new property.

    Args:
        property_data: Dictionary containing property information including
            address, city, state, and other property details.

    Returns:
        Dictionary representing the newly created property with assigned ID
        and timestamps.

    Raises:
        ValidationError: If property data is invalid or missing required fields.
        AuthenticationError: If API key is invalid or expired.
        OpenToCloseAPIError: If the API request fails for other reasons.

    Example:
        ```python
        property_data = {
            "address": "123 Main Street",
            "city": "San Francisco",
            "state": "CA",
            "zip_code": "94102",
            "listing_price": 850000
        }
        
        property = client.properties.create_property(property_data)
        print(f"Created property {property['id']}")
        ```
    """
```

#### Markdown Documentation

- Use clear headings and structure
- Include code examples for all features
- Add cross-references between related topics
- Use admonitions for important notes

```markdown
!!! tip "Performance Tip"
    Use bulk operations when creating multiple properties to reduce API calls.

!!! warning "Rate Limits"
    Be aware of rate limits when making many requests in succession.

!!! example "Example Usage"
    ```python
    # Your example code here
    ```
```

### Building Documentation

```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Serve documentation locally
mkdocs serve

# Build static documentation
mkdocs build

# Deploy to GitHub Pages (maintainers only)
mkdocs gh-deploy
```

---

## 🐛 Bug Reports

### Before Reporting

1. **Search existing issues** to avoid duplicates
2. **Update to latest version** to see if bug is fixed
3. **Check documentation** for correct usage
4. **Create minimal reproduction** case

### Bug Report Template

```markdown
**Bug Description**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Initialize client with '...'
2. Call method '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Code Example**
```python
# Minimal code that reproduces the issue
from open_to_close import OpenToCloseAPI

client = OpenToCloseAPI()
# ... rest of code
```

**Environment**
- OS: [e.g. macOS 12.0]
- Python version: [e.g. 3.9.7]
- Package version: [e.g. 2.0.7]

**Additional Context**
Any other context about the problem.
```

---

## 💡 Feature Requests

### Before Requesting

1. **Check existing issues** for similar requests
2. **Review roadmap** to see if already planned
3. **Consider alternatives** using existing features
4. **Think about implementation** complexity

### Feature Request Template

```markdown
**Feature Description**
A clear description of the feature you'd like to see.

**Use Case**
Describe the problem this feature would solve.

**Proposed Solution**
How you think this feature should work.

**Alternative Solutions**
Other ways this could be implemented.

**API Design**
```python
# How you envision the API would look
client.new_feature.do_something(param="value")
```

**Additional Context**
Any other context or screenshots about the feature.
```

---

## 🔄 Pull Request Process

### Before Submitting

1. **Create an issue** to discuss the change
2. **Fork the repository** and create a feature branch
3. **Write tests** for your changes
4. **Update documentation** as needed
5. **Run all quality checks** locally

### Pull Request Checklist

- [ ] **Tests**: All tests pass and new tests added
- [ ] **Coverage**: Test coverage maintained or improved
- [ ] **Linting**: Code passes all linting checks
- [ ] **Type Checking**: No mypy errors
- [ ] **Documentation**: Updated relevant documentation
- [ ] **Changelog**: Added entry to CHANGELOG.md
- [ ] **Commit Messages**: Follow conventional commit format

### Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(properties): add bulk property creation endpoint

fix(auth): handle expired token refresh properly

docs(api): add examples for property search

test(contacts): add integration tests for contact creation
```

### Pull Request Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Tests added for new functionality
- [ ] Documentation updated
- [ ] Changelog updated

## Related Issues
Fixes #(issue number)
```

---

## 🏗️ API Design Principles

### Consistency

- **Method Naming**: Use consistent patterns across all APIs
- **Parameter Names**: Use the same names for similar concepts
- **Response Format**: Standardize response structure
- **Error Handling**: Consistent exception types and messages

### Usability

- **Intuitive APIs**: Methods should be self-explanatory
- **Good Defaults**: Sensible default values for optional parameters
- **Clear Documentation**: Every public method documented with examples
- **Type Hints**: Full type annotations for better IDE support

### Performance

- **Lazy Loading**: Don't initialize unnecessary resources
- **Efficient Requests**: Minimize API calls where possible
- **Caching**: Cache frequently accessed data appropriately
- **Bulk Operations**: Support batch operations for efficiency

### Reliability

- **Error Handling**: Comprehensive exception handling
- **Retry Logic**: Automatic retries for transient failures
- **Validation**: Input validation before API calls
- **Testing**: Thorough test coverage

---

## 🔒 Security Considerations

### API Key Handling

- Never log API keys
- Support environment variable configuration
- Clear documentation about key security
- Validate key format before use

### Input Validation

- Sanitize all user inputs
- Validate data types and ranges
- Escape special characters appropriately
- Use parameterized queries where applicable

### Dependencies

- Keep dependencies up to date
- Regular security audits
- Minimal dependency footprint
- Pin dependency versions

---

## 📋 Code Review Guidelines

### For Authors

- **Small PRs**: Keep changes focused and reviewable
- **Clear Description**: Explain what and why
- **Self Review**: Review your own code first
- **Tests**: Include comprehensive tests
- **Documentation**: Update relevant docs

### For Reviewers

- **Be Constructive**: Provide helpful feedback
- **Check Tests**: Ensure adequate test coverage
- **Consider Edge Cases**: Think about error conditions
- **Performance**: Consider performance implications
- **Security**: Look for security issues

### Review Checklist

- [ ] **Functionality**: Does the code do what it's supposed to?
- [ ] **Tests**: Are there adequate tests?
- [ ] **Performance**: Any performance concerns?
- [ ] **Security**: Any security implications?
- [ ] **Documentation**: Is documentation updated?
- [ ] **Style**: Does code follow project conventions?

---

## 🎯 Development Workflow

### Branch Strategy

- **main**: Production-ready code
- **develop**: Integration branch for features
- **feature/***: Feature development branches
- **fix/***: Bug fix branches
- **release/***: Release preparation branches

### Workflow Steps

1. **Create Issue**: Describe the work to be done
2. **Create Branch**: From develop branch
3. **Develop**: Write code, tests, and documentation
4. **Test**: Run all tests and quality checks
5. **Submit PR**: Create pull request to develop
6. **Review**: Code review and feedback
7. **Merge**: Merge to develop after approval
8. **Release**: Periodic releases to main

---

## 🏆 Recognition

We appreciate all contributions! Contributors are recognized in:

- **CONTRIBUTORS.md**: List of all contributors
- **Release Notes**: Major contributions highlighted
- **GitHub**: Contributor statistics and graphs
- **Documentation**: Author attribution where appropriate

---

## 📞 Getting Help

### Community Support

- **GitHub Discussions**: Ask questions and share ideas
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Comprehensive guides and examples

### Maintainer Contact

For sensitive issues or questions:

- **Email**: [maintainers@theperrygroup.com](mailto:maintainers@theperrygroup.com)
- **Security Issues**: [security@theperrygroup.com](mailto:security@theperrygroup.com)

---

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

*Thank you for contributing to the Open To Close API Python client! Your contributions help make real estate technology better for everyone.* 🏠✨