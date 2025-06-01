# Quick Start Guide

Get up and running with the Open To Close API in 5 minutes.

## 1. Installation

```bash
pip install open-to-close
```

## 2. Set Your API Key

```bash
export OPEN_TO_CLOSE_API_KEY="your_api_key_here"
```

Or create a `.env` file:
```env
OPEN_TO_CLOSE_API_KEY=your_actual_api_key_here
```

## 3. Initialize the Client

```python
from open_to_close import OpenToCloseAPI

# Initialize with environment variable
client = OpenToCloseAPI()

# Or provide API key directly
# client = OpenToCloseAPI(api_key="your_api_key")
```

## 4. Basic Usage Examples

### List Contacts

```python
try:
    contacts = client.contacts.list_contacts()
    print(f"Found {len(contacts)} contacts")
    
    for contact in contacts[:5]:  # Show first 5
        print(f"- {contact.get('first_name')} {contact.get('last_name')}")
        
except Exception as e:
    print(f"Error: {e}")
```

### Create a New Contact

```python
new_contact = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890"
}

try:
    contact = client.contacts.create_contact(new_contact)
    print(f"Created contact with ID: {contact['id']}")
except Exception as e:
    print(f"Error creating contact: {e}")
```

### Retrieve a Specific Contact

```python
try:
    contact = client.contacts.retrieve_contact(123)
    print(f"Contact: {contact['first_name']} {contact['last_name']}")
    print(f"Email: {contact['email']}")
except Exception as e:
    print(f"Error retrieving contact: {e}")
```

### List Properties

```python
try:
    properties = client.properties.list_properties()
    print(f"Found {len(properties)} properties")
    
    for prop in properties[:3]:  # Show first 3
        print(f"- {prop.get('address')}")
        
except Exception as e:
    print(f"Error: {e}")
```

### Work with Property Documents

```python
property_id = 123

try:
    # List documents for a property
    documents = client.property_documents.list_property_documents(property_id)
    print(f"Property has {len(documents)} documents")
    
    # Create a new document
    new_doc = {
        "title": "Purchase Agreement",
        "description": "Initial purchase agreement draft",
        "document_type": "contract"
    }
    
    doc = client.property_documents.create_property_document(property_id, new_doc)
    print(f"Created document with ID: {doc['id']}")
    
except Exception as e:
    print(f"Error with documents: {e}")
```

## 5. Error Handling

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

## 6. Available Resources

The client provides access to all Open To Close API resources:

```python
# Core resources
client.agents           # Agent management
client.contacts         # Contact management  
client.properties       # Property management
client.teams           # Team management
client.tags            # Tag management
client.users           # User management

# Property-related resources
client.property_contacts    # Property-contact relationships
client.property_documents   # Property documents
client.property_emails      # Property emails
client.property_notes       # Property notes
client.property_tasks       # Property tasks
```

## Next Steps

- [API Reference](api-reference.md) - Complete method documentation
- [Examples](examples.md) - More comprehensive examples
- [Troubleshooting](troubleshooting.md) - Common issues and solutions

## Need Help?

- Check the [troubleshooting guide](troubleshooting.md) for common issues
- Review the [complete examples](examples.md) for advanced usage patterns
- Refer to the [API reference](api-reference.md) for detailed method documentation 