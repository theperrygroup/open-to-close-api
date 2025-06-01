# Main Client

The `OpenToCloseAPI` class serves as the main entry point for interacting with the Open To Close API. It provides access to all API endpoints through service-specific clients using a composition pattern with lazy initialization.

!!! abstract "OpenToCloseAPI Client"
    The main client handles authentication, configuration, and provides access to all resource-specific API clients through properties.

---

## 🚀 Quick Start

```python
from open_to_close import OpenToCloseAPI

# Initialize with environment variable (recommended)
client = OpenToCloseAPI()

# Or provide API key directly
client = OpenToCloseAPI(api_key="your_api_key_here")

# Access different API endpoints
properties = client.properties.list_properties()
agents = client.agents.list_agents()
contacts = client.contacts.list_contacts()
```

---

## 📋 Class Reference

### **OpenToCloseAPI**

The main client class for accessing all Open To Close API endpoints.

```python
class OpenToCloseAPI:
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        base_url: Optional[str] = None
    ) -> None:
```

**Parameters:**

| Name | Type | Required | Description | Default |
|------|------|----------|-------------|---------|
| `api_key` | `str` | No | API key for authentication. If not provided, loads from `OPEN_TO_CLOSE_API_KEY` environment variable | `None` |
| `base_url` | `str` | No | Base URL for the Open To Close API | `https://api.opentoclose.com/v1` |

**Raises:**

| Exception | When |
|-----------|------|
| `AuthenticationError` | If API key is not provided and not found in environment variables |

---

## 🏗️ Available API Clients

The main client provides access to the following API endpoints through properties:

### **Core Resource Clients**

<div class="grid cards" markdown>

-   :material-account-tie:{ .lg .middle } **Agents**

    ---

    Manage agent profiles, contact information, and assignments

    [:octicons-arrow-right-24: Agents API](agents.md)

-   :material-account-group:{ .lg .middle } **Contacts**

    ---

    Customer and lead management with relationship tracking

    [:octicons-arrow-right-24: Contacts API](contacts.md)

-   :material-home-city:{ .lg .middle } **Properties**

    ---

    Complete property lifecycle from listing to closing

    [:octicons-arrow-right-24: Properties API](properties.md)

-   :material-account-supervisor:{ .lg .middle } **Teams**

    ---

    Team organization and user group management

    [:octicons-arrow-right-24: Teams API](teams.md)

-   :material-account:{ .lg .middle } **Users**

    ---

    User account management and system access

    [:octicons-arrow-right-24: Users API](users.md)

-   :material-tag:{ .lg .middle } **Tags**

    ---

    Classification and labeling system for organization

    [:octicons-arrow-right-24: Tags API](tags.md)

</div>

### **Property Sub-Resource Clients**

<div class="grid cards" markdown>

-   :material-file-document:{ .lg .middle } **Property Documents**

    ---

    File attachments and document management per property

    [:octicons-arrow-right-24: Documents API](property-documents.md)

-   :material-email:{ .lg .middle } **Property Emails**

    ---

    Email communication tracking and history

    [:octicons-arrow-right-24: Emails API](property-emails.md)

-   :material-note-text:{ .lg .middle } **Property Notes**

    ---

    Internal notes and annotations for properties

    [:octicons-arrow-right-24: Notes API](property-notes.md)

-   :material-calendar-check:{ .lg .middle } **Property Tasks**

    ---

    Task management and workflow automation

    [:octicons-arrow-right-24: Tasks API](property-tasks.md)

-   :material-home-account:{ .lg .middle } **Property Contacts**

    ---

    Property-specific contact relationships and roles

    [:octicons-arrow-right-24: Property Contacts API](property-contacts.md)

</div>

---

## 📖 Client Properties

### **Core Resource Properties**

| Property | Type | Description |
|----------|------|-------------|
| `client.agents` | `AgentsAPI` | Access to agents endpoints |
| `client.contacts` | `ContactsAPI` | Access to contacts endpoints |
| `client.properties` | `PropertiesAPI` | Access to properties endpoints |
| `client.teams` | `TeamsAPI` | Access to teams endpoints |
| `client.users` | `UsersAPI` | Access to users endpoints |
| `client.tags` | `TagsAPI` | Access to tags endpoints |

### **Property Sub-Resource Properties**

| Property | Type | Description |
|----------|------|-------------|
| `client.property_contacts` | `PropertyContactsAPI` | Property-specific contact relationships |
| `client.property_documents` | `PropertyDocumentsAPI` | Property document management |
| `client.property_emails` | `PropertyEmailsAPI` | Property email communication tracking |
| `client.property_notes` | `PropertyNotesAPI` | Property notes and annotations |
| `client.property_tasks` | `PropertyTasksAPI` | Property task management |

---

## 🔧 Configuration Examples

### **Environment Variable Configuration (Recommended)**

=== ":material-bash: Linux/macOS"

    ```bash
    export OPEN_TO_CLOSE_API_KEY="your_api_key_here"
    ```

=== ":material-microsoft-windows: Windows"

    ```cmd
    set OPEN_TO_CLOSE_API_KEY=your_api_key_here
    ```

=== ":material-application: Python Code"

    ```python
    import os
    from open_to_close import OpenToCloseAPI
    
    # Verify environment variable is set
    if not os.getenv("OPEN_TO_CLOSE_API_KEY"):
        raise EnvironmentError("API key not configured")
    
    # Initialize client (automatically uses environment variable)
    client = OpenToCloseAPI()
    ```

### **Direct Configuration**

```python
from open_to_close import OpenToCloseAPI

# Provide API key directly
client = OpenToCloseAPI(api_key="your_api_key_here")

# Custom base URL (for testing or different environments)
client = OpenToCloseAPI(
    api_key="your_api_key_here",
    base_url="https://staging-api.opentoclose.com/v1"
)
```

### **Configuration Class Pattern**

```python
import os
from dataclasses import dataclass
from typing import Optional
from open_to_close import OpenToCloseAPI

@dataclass
class APIConfig:
    """Configuration for Open To Close API client."""
    api_key: str
    base_url: str = "https://api.opentoclose.com/v1"
    
    @classmethod
    def from_environment(cls) -> "APIConfig":
        """Create configuration from environment variables."""
        api_key = os.getenv("OPEN_TO_CLOSE_API_KEY")
        if not api_key:
            raise ValueError("OPEN_TO_CLOSE_API_KEY environment variable required")
        
        return cls(
            api_key=api_key,
            base_url=os.getenv("OPEN_TO_CLOSE_BASE_URL", cls.base_url)
        )

# Usage
config = APIConfig.from_environment()
client = OpenToCloseAPI(api_key=config.api_key, base_url=config.base_url)
```

---

## 🎯 Common Usage Patterns

### **Basic Operations**

```python
from open_to_close import OpenToCloseAPI

# Initialize client
client = OpenToCloseAPI()

# Work with different resources
properties = client.properties.list_properties()
agents = client.agents.list_agents()
contacts = client.contacts.list_contacts()

print(f"Found {len(properties)} properties")
print(f"Found {len(agents)} agents")
print(f"Found {len(contacts)} contacts")
```

### **Resource Creation Workflow**

```python
# Create a new property
property_data = client.properties.create_property({
    "address": "123 Main Street",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
    "property_type": "Single Family Home"
})

# Create a contact
contact_data = client.contacts.create_contact({
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890"
})

# Link contact to property
client.property_contacts.create_property_contact(
    property_id=property_data["id"],
    contact_data={
        "contact_id": contact_data["id"],
        "role": "Buyer"
    }
)
```

### **Lazy Loading Demonstration**

```python
# Clients are initialized only when first accessed
client = OpenToCloseAPI()

# No API calls made yet - clients are lazy loaded
print("Client initialized")

# First access initializes the properties client
properties = client.properties.list_properties()  # API call made here

# Subsequent access uses the same instance
more_properties = client.properties.list_properties()  # Uses existing client
```

---

## 🛡️ Error Handling

All client methods can raise these exceptions:

```python
from open_to_close import OpenToCloseAPI
from open_to_close.exceptions import (
    AuthenticationError,
    ValidationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    NetworkError
)

def robust_api_usage():
    """Example of comprehensive error handling."""
    try:
        client = OpenToCloseAPI()
        
        # Make API calls
        properties = client.properties.list_properties()
        
    except AuthenticationError:
        print("Authentication failed - check your API key")
    except ValidationError as e:
        print(f"Invalid request parameters: {e}")
    except NotFoundError as e:
        print(f"Resource not found: {e}")
    except RateLimitError as e:
        print(f"Rate limit exceeded: {e}")
    except ServerError as e:
        print(f"Server error: {e}")
    except NetworkError as e:
        print(f"Network error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
```

---

## 📚 Related Documentation

!!! tip "Additional Resources"

    - **[Authentication Guide](../getting-started/authentication.md)** - Detailed authentication setup
    - **[Quick Start Tutorial](../getting-started/quickstart.md)** - Get started with the API
    - **[Error Handling Guide](../guides/error-handling.md)** - Comprehensive error handling patterns
    - **[Exception Reference](../reference/exceptions.md)** - Complete exception documentation

---

## 🚀 Next Steps

Ready to start using the API? Here's your path:

1. **[Set up authentication](../getting-started/authentication.md)** - Configure your API key
2. **[Try the quick start](../getting-started/quickstart.md)** - Make your first API calls
3. **[Explore Properties API](properties.md)** - Start with the core resource
4. **[Review error handling](../guides/error-handling.md)** - Build robust applications

---

*The main client provides a unified interface to all Open To Close API functionality with lazy loading and comprehensive error handling.* 