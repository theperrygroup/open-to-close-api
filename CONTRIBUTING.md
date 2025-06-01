# Contributing to Open To Close API Python Client

Thank you for your interest in contributing to the Open To Close API Python Client! This document provides guidelines and information for contributors.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, virtualenv, or conda)

### Setting up the Development Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/theperrygroup/open-to-close.git
   cd open-to-close
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Set up pre-commit hooks:**
   ```bash
   pre-commit install
   ```

5. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API key
   ```

## Development Workflow

### Code Style and Quality

This project uses several tools to maintain code quality:

- **Black**: Code formatting (88 character line length)
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **bandit**: Security scanning
- **pylint**: Additional code analysis

Run all checks before committing:
```bash
# Format code
black open_to_close tests

# Sort imports
isort open_to_close tests

# Lint code
flake8 open_to_close

# Type checking
mypy open_to_close

# Security scanning
bandit -r open_to_close

# Run all pre-commit hooks
pre-commit run --all-files
```

### Testing

We maintain high test coverage (>98%). All tests must pass before merging.

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=open_to_close --cov-report=term-missing

# Run specific test file
pytest tests/test_agents.py

# Run tests in watch mode
pytest --watch
```

### Adding New Features

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Write tests first (TDD approach):**
   - Add tests in the appropriate `tests/test_*.py` file
   - Ensure tests fail initially

3. **Implement the feature:**
   - Follow the existing code patterns
   - Add comprehensive docstrings (Google style)
   - Include type hints
   - Update documentation if needed

4. **Ensure all checks pass:**
   ```bash
   pytest
   pre-commit run --all-files
   ```

5. **Update documentation:**
   - Update API reference if needed
   - Add examples for new features
   - Update changelog

## API Client Guidelines

### File Organization

- One API resource class per file (e.g., `contacts.py`, `properties.py`)
- Resource classes inherit from `BaseClient`
- Follow RESTful method naming: `list_*`, `create_*`, `retrieve_*`, `update_*`, `delete_*`

### Method Structure

```python
def create_contact(
    self,
    contact_data: Dict[str, Union[str, int, float]],
    validate: bool = True
) -> Dict[str, Any]:
    """Create a new contact.
    
    Args:
        contact_data: Contact information to create
        validate: Whether to validate input data
        
    Returns:
        Created contact data
        
    Raises:
        AuthenticationError: If API key is invalid
        ValidationError: If contact data is invalid
        
    Example:
        >>> client = OpenToCloseAPI()
        >>> contact = client.contacts.create_contact({
        ...     "first_name": "John",
        ...     "last_name": "Doe",
        ...     "email": "john@example.com"
        ... })
    """
    return self._process_response_data(
        self.post("contacts", json_data=contact_data)
    )
```

### Error Handling

- Use specific exception types from `exceptions.py`
- Provide helpful error messages
- Log exceptions with context
- Handle rate limiting gracefully

### Documentation

- Use Google-style docstrings for all public methods
- Include type hints for all parameters and return values
- Provide usage examples in docstrings
- Keep README.md updated with new features

## Submitting Changes

### Pull Request Process

1. **Update your branch:**
   ```bash
   git checkout main
   git pull origin main
   git checkout your-feature-branch
   git rebase main
   ```

2. **Ensure all checks pass:**
   ```bash
   pytest
   pre-commit run --all-files
   ```

3. **Create a pull request:**
   - Use a descriptive title
   - Provide a detailed description of changes
   - Reference any related issues
   - Include screenshots for UI changes

4. **Address review feedback:**
   - Make requested changes
   - Push updates to your branch
   - Respond to reviewer comments

### Commit Message Guidelines

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Examples:
```
Add rate limiting support to base client

- Implement exponential backoff for 429 responses
- Add configurable retry attempts
- Update documentation with rate limiting examples

Fixes #123
```

## Release Process

1. **Update version numbers:**
   - `open_to_close/__init__.py`
   - `pyproject.toml`

2. **Update changelog:**
   - Add new version section
   - List all changes and breaking changes

3. **Create release PR:**
   - Title: "Release v{version}"
   - Include changelog updates

4. **After merge:**
   - Tag the release
   - GitHub Actions will handle PyPI publishing

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/theperrygroup/open-to-close/issues)
- **Discussions**: [GitHub Discussions](https://github.com/theperrygroup/open-to-close/discussions)
- **Email**: john@theperry.group

## Code of Conduct

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/) Code of Conduct. Please read and follow these guidelines when participating in our community.

Thank you for contributing! 🎉 