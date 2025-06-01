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

# Initialize the client (loads API key from .env or environment variable)
client = OpenToCloseAPI()

# Example: List contacts
contacts = client.contacts.list_contacts()
for contact in contacts[:5]:  # Show first 5
    print(f"{contact.get('first_name')} {contact.get('last_name')}")
```

### API Key Setup

Create a `.env` file or set environment variable:

```env
OPEN_TO_CLOSE_API_KEY=your_actual_api_key_here
```

## 📚 Complete Documentation

For comprehensive documentation, examples, and guides, see the **[docs/](docs/)** directory:

| Document | Description |
|----------|-------------|
| **[📖 Complete Documentation](docs/index.md)** | Main documentation hub |
| **[⚡ Quick Start Guide](docs/quickstart.md)** | 5-minute tutorial with examples |
| **[📋 Installation Guide](docs/installation.md)** | Detailed setup instructions |
| **[🔧 API Reference](docs/api-reference.md)** | Complete API method documentation |
| **[💡 Examples](docs/examples.md)** | Real-world usage examples and workflows |
| **[🚨 Troubleshooting](docs/troubleshooting.md)** | Common issues and solutions |
| **[🤝 Contributing](docs/contributing.md)** | Development setup and guidelines |
| **[🚀 Deployment](docs/deployment.md)** | Production deployment guide |
| **[📝 Changelog](docs/changelog.md)** | Version history and migration guides |

## Available API Resources

The client provides access to all Open To Close API resources:

**Core Resources:** `agents`, `contacts`, `properties`, `teams`, `tags`, `users`  
**Property Relations:** `property_contacts`, `property_documents`, `property_emails`, `property_notes`, `property_tasks`

Each resource provides methods for `list`, `create`, `retrieve`, `update`, and `delete` operations where applicable.

> 📖 **See [API Reference](docs/api-reference.md) for complete method documentation and examples**

## Error Handling

The client provides specific exception types for robust error handling:

```python
from open_to_close import OpenToCloseAPI, AuthenticationError, NotFoundError

try:
    client = OpenToCloseAPI()
    contact = client.contacts.retrieve_contact(123)
except AuthenticationError:
    print("Check your API key")
except NotFoundError:
    print("Contact not found")
```

> 📖 **See [Error Handling Guide](docs/troubleshooting.md#error-handling) for comprehensive error handling patterns**

## Development

For development setup, testing, and contribution guidelines:

> 📖 **See [Contributing Guide](docs/contributing.md) for complete development documentation**

## Support

- 📖 **[Troubleshooting Guide](docs/troubleshooting.md)** - Common issues and solutions
- 💡 **[Examples](docs/examples.md)** - Comprehensive usage patterns
- 📧 **Email**: john@theperry.group

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Built by The Perry Group for the real estate industry** 🏠 