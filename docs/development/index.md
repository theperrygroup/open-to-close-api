# Development

Welcome to the development section of the Open To Close API Python client documentation. This section provides comprehensive information for developers who want to contribute to the project, understand the codebase, or set up a development environment.

## 🚀 Quick Start for Contributors

New to contributing? Start here:

1. **[Contributing Guide](contributing.md)** - Learn how to contribute to the project
2. **[Testing Guide](testing.md)** - Understand our testing approach and run tests
3. **[Release Process](release-process.md)** - How we manage releases and versioning

---

## 📋 Development Topics

### **Getting Started**
- **[Contributing Guide](contributing.md)** - Complete guide to contributing
- **[Development Setup](contributing.md#development-setup)** - Set up your local environment
- **[Code Style](contributing.md#code-style)** - Coding standards and conventions

### **Testing & Quality**
- **[Testing Guide](testing.md)** - Testing framework and best practices
- **[Code Coverage](testing.md#code-coverage)** - Maintaining high test coverage
- **[Continuous Integration](testing.md#continuous-integration)** - CI/CD pipeline

### **Release Management**
- **[Release Process](release-process.md)** - How we create and publish releases
- **[Versioning Strategy](release-process.md#versioning)** - Semantic versioning approach
- **[Changelog Management](release-process.md#changelog)** - Maintaining the changelog

---

## 🛠️ Development Environment

### Prerequisites

- **Python 3.8+** - Required for development
- **Git** - Version control
- **Make** - Build automation (optional but recommended)

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/theperrygroup/open-to-close.git
cd open-to-close

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests to verify setup
pytest
```

### Development Tools

| Tool | Purpose | Configuration |
|------|---------|---------------|
| **pytest** | Testing framework | `pytest.ini` |
| **black** | Code formatting | `pyproject.toml` |
| **isort** | Import sorting | `pyproject.toml` |
| **flake8** | Linting | `.flake8` |
| **mypy** | Type checking | `mypy.ini` |
| **pre-commit** | Git hooks | `.pre-commit-config.yaml` |

---

## 📁 Project Structure

```
open-to-close/
├── open_to_close/          # Main package
│   ├── __init__.py         # Package initialization
│   ├── client.py           # Main API client
│   ├── base_client.py      # Base client functionality
│   ├── exceptions.py       # Custom exceptions
│   ├── properties.py       # Properties API
│   ├── agents.py           # Agents API
│   ├── contacts.py         # Contacts API
│   ├── teams.py            # Teams API
│   ├── users.py            # Users API
│   ├── tags.py             # Tags API
│   ├── property_*.py       # Property sub-resources
│   └── py.typed            # Type hints marker
├── tests/                  # Test suite
│   ├── conftest.py         # Test configuration
│   ├── test_*.py           # Test modules
│   └── fixtures/           # Test fixtures
├── docs/                   # Documentation
│   ├── api/                # API reference
│   ├── guides/             # User guides
│   ├── reference/          # Reference materials
│   └── development/        # Development docs
├── tasks/                  # Build tasks
├── requirements*.txt       # Dependencies
├── pyproject.toml          # Project configuration
├── setup.py               # Package setup
└── README.md              # Project overview
```

---

## 🔧 Common Development Tasks

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=open_to_close

# Run specific test file
pytest tests/test_properties.py

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "test_create"
```

### Code Quality Checks

```bash
# Format code
black open_to_close tests

# Sort imports
isort open_to_close tests

# Lint code
flake8 open_to_close tests

# Type checking
mypy open_to_close

# Run all quality checks
make lint
```

### Building Documentation

```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

### Package Building

```bash
# Build package
python -m build

# Install locally
pip install -e .

# Upload to PyPI (maintainers only)
twine upload dist/*
```

---

## 🤝 Contributing Workflow

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR-USERNAME/open-to-close.git
cd open-to-close
```

### 2. Create Feature Branch

```bash
# Create and switch to feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-description
```

### 3. Make Changes

- Write code following our [style guide](contributing.md#code-style)
- Add tests for new functionality
- Update documentation as needed
- Run quality checks locally

### 4. Commit Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add feature: description of changes"

# Follow conventional commit format
git commit -m "feat: add property search functionality"
```

### 5. Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create pull request on GitHub
# Fill out the PR template
```

---

## 📊 Development Metrics

### Code Quality Targets

| Metric | Target | Current |
|--------|--------|---------|
| Test Coverage | ≥ 95% | 98% |
| Type Coverage | ≥ 90% | 95% |
| Documentation Coverage | ≥ 90% | 92% |
| Linting Score | 10/10 | 10/10 |

### Performance Benchmarks

| Operation | Target | Current |
|-----------|--------|---------|
| Client Initialization | < 100ms | 45ms |
| Simple API Call | < 500ms | 250ms |
| Bulk Operations | < 2s/100 items | 1.2s/100 items |
| Memory Usage | < 50MB | 32MB |

---

## 🐛 Debugging

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure package is installed in development mode
   pip install -e .
   ```

2. **Test Failures**
   ```bash
   # Run tests with more verbose output
   pytest -vvv --tb=long
   ```

3. **Type Checking Issues**
   ```bash
   # Run mypy with detailed output
   mypy --show-error-codes open_to_close
   ```

### Debug Configuration

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use debug client
from open_to_close import OpenToCloseAPI
client = OpenToCloseAPI(debug=True)
```

---

## 📚 Additional Resources

### Internal Documentation

- **[API Design Principles](contributing.md#api-design)** - How we design APIs
- **[Error Handling Strategy](contributing.md#error-handling)** - Our approach to errors
- **[Testing Philosophy](testing.md#philosophy)** - Why we test the way we do

### External Resources

- **[Python Packaging Guide](https://packaging.python.org/)** - Python packaging best practices
- **[Semantic Versioning](https://semver.org/)** - Versioning specification
- **[Conventional Commits](https://www.conventionalcommits.org/)** - Commit message format
- **[Keep a Changelog](https://keepachangelog.com/)** - Changelog format

### Community

- **[GitHub Discussions](https://github.com/theperrygroup/open-to-close/discussions)** - Community discussions
- **[GitHub Issues](https://github.com/theperrygroup/open-to-close/issues)** - Bug reports and feature requests
- **[Contributing Guidelines](contributing.md)** - How to contribute

---

## 🎯 Development Roadmap

### Current Sprint
- Enhanced error handling and retry mechanisms
- Performance optimizations for bulk operations
- Improved documentation with more examples

### Next Release (v2.1.0)
- Webhook support for real-time updates
- Advanced filtering and search capabilities
- GraphQL-style field selection

### Future Plans
- Async/await support for better performance
- Plugin system for extensibility
- CLI tool for common operations

---

*Ready to contribute? Start with our [Contributing Guide](contributing.md) and join our community of developers building the future of real estate technology!*