# Open To Close API Python Client

[![PyPI version](https://img.shields.io/pypi/v/open-to-close?color=blue&label=version)](https://pypi.org/project/open-to-close/)
[![Python versions](https://img.shields.io/pypi/pyversions/open-to-close)](https://pypi.org/project/open-to-close/)
[![License](https://img.shields.io/github/license/theperrygroup/open-to-close)](https://github.com/theperrygroup/open-to-close/blob/main/LICENSE)
[![Build Status](https://img.shields.io/github/actions/workflow/status/theperrygroup/open-to-close/ci.yml?branch=main)](https://github.com/theperrygroup/open-to-close/actions)
[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue)](https://theperrygroup.github.io/open-to-close/)
[![Coverage](https://img.shields.io/codecov/c/github/theperrygroup/open-to-close)](https://codecov.io/gh/theperrygroup/open-to-close)

A modern, type-safe Python wrapper for the Open To Close API. Manage properties, agents, contacts, and more with a clean, intuitive interface designed for real estate professionals and developers.

## ✨ Features

- **🏠 Complete Property Management** - Full CRUD operations for properties, listings, and transactions
- **👥 Contact & Team Management** - Manage agents, contacts, teams, and user relationships
- **📄 Document Tracking** - Handle property documents, emails, notes, and tasks
- **🔒 Type Safety** - Full type hints and IDE support for better development experience
- **🛡️ Robust Error Handling** - Comprehensive exception handling with detailed error messages
- **⚡ Production Ready** - Built-in rate limiting, retry logic, and authentication management
- **🧪 Well Tested** - Comprehensive test suite with 100% coverage
- **📚 Excellent Documentation** - Complete guides, examples, and API reference

## 🚀 Quick Start

### Installation

```bash
pip install open-to-close
```

### Authentication

Set your API key as an environment variable:

```bash
export OPEN_TO_CLOSE_API_KEY="your_api_key_here"
```

### Basic Usage

```python
from open_to_close import OpenToCloseAPI

# Initialize the client
client = OpenToCloseAPI()

# Create a new property
property_data = client.properties.create_property({
    "address": "123 Main Street",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
    "property_type": "Single Family Home",
    "listing_price": 450000
})

# Get all properties
properties = client.properties.list_properties()

# Add a note to the property
note = client.property_notes.create_property_note(
    property_data["id"],
    {"content": "Initial property intake completed"}
)

print(f"Created property {property_data['id']} with note {note['id']}")
```

## 📋 Core Resources

| Resource | Description | Example Usage |
|----------|-------------|---------------|
| **Properties** | Manage real estate listings and transactions | `client.properties.list_properties()` |
| **Agents** | Handle agent profiles and assignments | `client.agents.list_agents()` |
| **Contacts** | Customer and lead management | `client.contacts.create_contact(data)` |
| **Teams** | Team organization and structure | `client.teams.list_teams()` |
| **Users** | User account management | `client.users.retrieve_user(123)` |
| **Tags** | Classification and labeling | `client.tags.list_tags()` |

## 🏗️ Property Sub-Resources

Extend property functionality with related data:

| Sub-Resource | Description | Example Usage |
|-------------|-------------|---------------|
| **Documents** | File attachments per property | `client.property_documents.list_property_documents(prop_id)` |
| **Emails** | Communication tracking | `client.property_emails.create_property_email(prop_id, data)` |
| **Notes** | Internal annotations | `client.property_notes.list_property_notes(prop_id)` |
| **Tasks** | Workflow management | `client.property_tasks.create_property_task(prop_id, data)` |
| **Contacts** | Property-specific relationships | `client.property_contacts.list_property_contacts(prop_id)` |

## 🎯 Real-World Example

Here's a complete workflow for onboarding a new property listing:

```python
from open_to_close import OpenToCloseAPI
from datetime import datetime, timedelta

def onboard_new_listing():
    client = OpenToCloseAPI()
    
    # Create the property
    property_data = client.properties.create_property({
        "address": "456 Oak Avenue",
        "city": "Los Angeles",
        "state": "CA",
        "zip_code": "90210",
        "property_type": "Condo",
        "bedrooms": 2,
        "bathrooms": 2,
        "listing_price": 750000,
        "status": "Coming Soon"
    })
    
    # Create seller contact
    seller = client.contacts.create_contact({
        "first_name": "Sarah",
        "last_name": "Johnson",
        "email": "sarah.johnson@email.com",
        "contact_type": "Seller"
    })
    
    # Link seller to property
    client.property_contacts.create_property_contact(
        property_data["id"],
        {
            "contact_id": seller["id"],
            "role": "Seller",
            "primary": True
        }
    )
    
    # Add initial tasks
    client.property_tasks.create_property_task(
        property_data["id"],
        {
            "title": "Professional photography",
            "due_date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
            "priority": "High"
        }
    )
    
    # Log initial note
    client.property_notes.create_property_note(
        property_data["id"],
        {
            "content": "Property onboarding completed. Ready for marketing.",
            "note_type": "Listing"
        }
    )
    
    return property_data

# Run the workflow
new_property = onboard_new_listing()
print(f"Successfully onboarded property: {new_property['address']}")
```

## 🔧 Advanced Configuration

### Environment-Specific Setup

```python
from open_to_close import OpenToCloseAPI

# Production
prod_client = OpenToCloseAPI(
    api_key="prod_key_here",
    base_url="https://api.opentoclose.com/v1"
)

# Development
dev_client = OpenToCloseAPI(
    api_key="dev_key_here",
    base_url="https://dev-api.opentoclose.com/v1"
)
```

### Error Handling

```python
from open_to_close import OpenToCloseAPI
from open_to_close.exceptions import (
    NotFoundError,
    ValidationError,
    AuthenticationError,
    RateLimitError
)

client = OpenToCloseAPI()

try:
    property_data = client.properties.retrieve_property(123)
except NotFoundError:
    print("Property not found")
except ValidationError as e:
    print(f"Invalid request: {e}")
except AuthenticationError:
    print("Check your API key")
except RateLimitError:
    print("Rate limit exceeded, retrying...")
```

## 📚 Documentation

- **[Complete Documentation](https://theperrygroup.github.io/open-to-close/)** - Full guides and API reference
- **[Getting Started](https://theperrygroup.github.io/open-to-close/getting-started/)** - Installation and setup
- **[API Reference](https://theperrygroup.github.io/open-to-close/api/)** - Detailed method documentation
- **[Examples](https://theperrygroup.github.io/open-to-close/guides/examples/)** - Real-world usage patterns
- **[Best Practices](https://theperrygroup.github.io/open-to-close/guides/best-practices/)** - Production guidelines

## 🧪 Testing

Run the test suite:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests with coverage
pytest --cov=open_to_close --cov-report=term-missing

# Run with specific Python version
python -m pytest tests/
```

## 🛠️ Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/theperrygroup/open-to-close.git
cd open-to-close

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Code Quality

This project maintains high code quality standards:

- **Formatting**: [Black](https://black.readthedocs.io/)
- **Import Sorting**: [isort](https://pycqa.github.io/isort/)
- **Linting**: [flake8](https://flake8.pycqa.org/)
- **Type Checking**: [mypy](https://mypy.readthedocs.io/)
- **Testing**: [pytest](https://docs.pytest.org/) with 100% coverage

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](https://theperrygroup.github.io/open-to-close/development/contributing/) for details.

### Quick Contribution Steps

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes with tests
4. **Ensure** all tests pass (`pytest`)
5. **Commit** your changes (`git commit -am 'Add amazing feature'`)
6. **Push** to the branch (`git push origin feature/amazing-feature`)
7. **Open** a Pull Request

## 📋 Requirements

- **Python**: 3.8 or higher
- **Dependencies**: `requests>=2.25.0`, `python-dotenv>=0.19.0`
- **API Access**: Valid Open To Close API key

## 🔗 Links

- **[PyPI Package](https://pypi.org/project/open-to-close/)**
- **[GitHub Repository](https://github.com/theperrygroup/open-to-close)**
- **[Documentation](https://theperrygroup.github.io/open-to-close/)**
- **[Issue Tracker](https://github.com/theperrygroup/open-to-close/issues)**
- **[Changelog](https://theperrygroup.github.io/open-to-close/reference/changelog/)**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏢 About The Perry Group

The Open To Close API Python client is developed and maintained by [The Perry Group](https://theperry.group), a leading real estate technology company.

---

**Built with ❤️ for the real estate community** 