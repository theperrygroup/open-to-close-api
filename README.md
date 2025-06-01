# Open To Close API Python Client

A comprehensive Python client library for the Open To Close API, providing easy-to-use interfaces for all API endpoints with full type safety and documentation.

## Organization

- **Organization**: The Perry Group
- **Author**: John Perry
- **Email**: john@theperry.group

## Features

✅ **Complete API Coverage** - All Open To Close API endpoints supported  
✅ **Type Safety** - Full type hints and validation  
✅ **Comprehensive Documentation** - Google-style docstrings with examples  
✅ **Error Handling** - Detailed exception handling with specific error types  
✅ **Easy Authentication** - Environment variable or direct API key support  
✅ **Real Estate Workflows** - Purpose-built for real estate operations  

## Quick Start

### Installation

```bash
pip install open-to-close
```

### Basic Usage

```python
from open_to_close import OpenToCloseAPI

# Initialize the client (loads API key from .env or environment variable by default)
client = OpenToCloseAPI()

# Or, provide the API key directly
# client = OpenToCloseAPI(api_key="YOUR_API_KEY")

# Example: List contacts
try:
    contacts = client.contacts.list_contacts()
    for contact in contacts[:5]:  # Show first 5
        print(f"{contact.get('first_name')} {contact.get('last_name')}")
except Exception as e:
    print(f"An error occurred: {e}")
```

### Complete Example

```python
# Create a new contact
new_contact = {
    "first_name": "John",
    "last_name": "Doe", 
    "email": "john.doe@example.com",
    "phone": "+1234567890"
}

try:
    contact = client.contacts.create_contact(new_contact)
    print(f"Created contact with ID: {contact['id']}")
    
    # Retrieve the contact
    retrieved = client.contacts.retrieve_contact(contact['id'])
    print(f"Retrieved: {retrieved['first_name']} {retrieved['last_name']}")
    
except Exception as e:
    print(f"Error: {e}")
```

## Available API Resources

The client provides access to all Open To Close API resources:

### Core Resources
*   `client.agents` - Real estate agent management
*   `client.contacts` - Customer contact management  
*   `client.properties` - Property management
*   `client.teams` - Team management
*   `client.tags` - Tagging system
*   `client.users` - User management

### Property-Related Resources
*   `client.property_contacts` - Property-contact relationships
*   `client.property_documents` - Document management
*   `client.property_emails` - Email tracking
*   `client.property_notes` - Note management
*   `client.property_tasks` - Task management

Each resource provides methods for `list`, `create`, `retrieve`, `update`, and `delete` operations where applicable.

## Documentation

📚 **Comprehensive Documentation Available:**

- **[📖 Complete Documentation](docs/index.md)** - Start here for full documentation
- **[⚡ Quick Start Guide](docs/quickstart.md)** - Get up and running in 5 minutes
- **[📋 Installation Guide](docs/installation.md)** - Detailed setup instructions
- **[🔧 API Reference](docs/api-reference.md)** - Complete API documentation
- **[💡 Examples](docs/examples.md)** - Real-world usage examples
- **[🚨 Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions
- **[🤝 Contributing](docs/contributing.md)** - Development and contribution guide
- **[🚀 Deployment](docs/deployment.md)** - Production deployment guide

## Environment Setup

Create a `.env` file in your project root:

```env
OPEN_TO_CLOSE_API_KEY=your_actual_api_key_here
```

The client will automatically load this when you initialize it:

```python
from open_to_close import OpenToCloseAPI

# Automatically loads from environment or .env file
client = OpenToCloseAPI()
```

## Error Handling

The client provides specific exception types for different error conditions:

```python
from open_to_close import (
    OpenToCloseAPI,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    RateLimitError
)

client = OpenToCloseAPI()

try:
    contact = client.contacts.retrieve_contact(999999)
except NotFoundError:
    print("Contact not found")
except AuthenticationError:
    print("Check your API key")
except ValidationError as e:
    print(f"Invalid data: {e}")
except RateLimitError:
    print("Rate limit exceeded, please wait")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Real Estate Workflows

The client is designed specifically for real estate operations:

```python
# Complete property listing workflow
property_data = {
    "address": "123 Main St",
    "city": "Anytown", 
    "state": "CA",
    "zip_code": "12345",
    "property_type": "single_family",
    "listing_price": 750000
}

# Create property
property = client.properties.create_property(property_data)

# Add listing documentation
client.property_documents.create_property_document(property['id'], {
    "title": "Listing Agreement",
    "description": "Signed listing agreement",
    "document_type": "contract"
})

# Create tasks for the listing
client.property_tasks.create_property_task(property['id'], {
    "title": "Schedule Photography",
    "description": "Arrange professional listing photos",
    "due_date": "2024-12-31",
    "priority": "high"
})
```

## Development

To set up for development:

1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment: `source .venv/bin/activate` (or `\.venv\Scripts\activate` on Windows)
4. Install dependencies: `pip install -r requirements-dev.txt`
5. Install in editable mode: `pip install -e .`
6. Create a `.env` file with your API key

### Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=open_to_close

# Run integration tests (requires API key)
pytest tests/integration/
```

A basic test script `test_api.py` is included to verify connectivity:

```bash
python test_api.py
```

## Documentation Standards

This project follows the **ReZEN Documentation Process** with:

- 📝 **Google-style docstrings** for all public methods
- 🔧 **Comprehensive type hints** throughout
- 💡 **Real-world examples** in all documentation
- 🚨 **Detailed error handling** documentation
- 🔄 **Automatic documentation updates** with code changes

See our [Contributing Guide](docs/contributing.md) for detailed documentation standards.

## Version History

See [CHANGELOG.md](docs/changelog.md) for detailed version history and migration guides.

## Support

- 📖 Check the [troubleshooting guide](docs/troubleshooting.md) for common issues
- 💡 Review [comprehensive examples](docs/examples.md) for usage patterns
- 📧 Contact: john@theperry.group

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Built by The Perry Group for the real estate industry** 🏠 