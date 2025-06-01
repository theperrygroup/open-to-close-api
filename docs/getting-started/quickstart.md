# Quick Start Guide

Get up and running with the Open To Close API in 5 minutes with this hands-on tutorial.

!!! tip "🚀 Before You Start"
    This guide assumes you have Python 3.8+ installed and the Open To Close API client ready to go. 
    
    **New to the client?** → [Installation Guide](installation.md)

## 🎯 What You'll Learn

By the end of this guide, you'll be able to:

- ✅ Initialize the API client
- ✅ Authenticate with your API key  
- ✅ Perform basic CRUD operations
- ✅ Handle errors gracefully
- ✅ Use advanced features

## 📋 Step 1: Installation & Setup

=== "Quick Install"
    ```bash
    pip install open-to-close
    ```

    !!! success "✅ Ready to go!"
        If you already have the client installed, skip to [Step 2](#step-2-set-your-api-key).

=== "Verify Installation"
    ```python
    import open_to_close
    print(f"Version: {open_to_close.__version__}")
    ```

## 🔑 Step 2: Set Your API Key

!!! warning "🔐 API Key Required"
    You'll need a valid Open To Close API key. Contact your administrator if you don't have one.

=== "Environment Variable"
    **Linux/macOS:**
    ```bash
    export OPEN_TO_CLOSE_API_KEY="your_api_key_here"
    ```

    **Windows:**
    ```cmd
    set OPEN_TO_CLOSE_API_KEY=your_api_key_here
    ```

=== ".env File"
    Create a `.env` file in your project directory:
    ```env
    OPEN_TO_CLOSE_API_KEY=your_actual_api_key_here
    ```

    !!! tip "💡 Recommended"
        The `.env` file approach is perfect for development and keeps your API key secure.

## 🔌 Step 3: Initialize the Client

=== "Basic Initialization"
    ```python
    from open_to_close import OpenToCloseAPI

    # Initialize with environment variable
    client = OpenToCloseAPI()
    ```

=== "With Direct API Key"
    ```python
    from open_to_close import OpenToCloseAPI

    # Initialize with API key directly (not recommended for production)
    client = OpenToCloseAPI(api_key="your_api_key")
    ```

=== "With Error Handling"
    ```python
    from open_to_close import OpenToCloseAPI, AuthenticationError

    try:
        client = OpenToCloseAPI()
        print("✅ Client initialized successfully!")
    except AuthenticationError:
        print("❌ Invalid API key")
    except Exception as e:
        print(f"⚠️ Initialization failed: {e}")
    ```

## 📝 Step 4: Your First API Calls

### Working with Contacts

!!! example "👥 Contact Management"

=== "List Contacts"
    ```python
    try:
        contacts = client.contacts.list_contacts()
        print(f"Found {len(contacts)} contacts")
        
        # Show first 5 contacts
        for contact in contacts[:5]:
            name = f"{contact.get('first_name', '')} {contact.get('last_name', '')}"
            print(f"- {name.strip()}")
            
    except Exception as e:
        print(f"Error listing contacts: {e}")
    ```

    **Expected Output:**
    ```
    Found 23 contacts
    - John Doe
    - Jane Smith
    - Mike Johnson
    - Sarah Wilson
    - Tom Brown
    ```

=== "Create Contact"
    ```python
    # Define new contact data
    new_contact = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890"
    }

    try:
        contact = client.contacts.create_contact(new_contact)
        print(f"✅ Created contact with ID: {contact['id']}")
    except Exception as e:
        print(f"❌ Error creating contact: {e}")
    ```

=== "Retrieve Contact"
    ```python
    contact_id = 123  # Replace with actual contact ID

    try:
        contact = client.contacts.retrieve_contact(contact_id)
        print(f"Contact Details:")
        print(f"  Name: {contact['first_name']} {contact['last_name']}")
        print(f"  Email: {contact['email']}")
    except NotFoundError:
        print(f"❌ Contact {contact_id} not found")
    except Exception as e:
        print(f"⚠️ Error retrieving contact: {e}")
    ```

### Working with Properties

!!! example "🏠 Property Management"

=== "List Properties"
    ```python
    try:
        properties = client.properties.list_properties()
        print(f"Found {len(properties)} properties")
        
        # Show first 3 properties with details
        for prop in properties[:3]:
            print(f"📍 {prop.get('address', 'Address not available')}")
            print(f"   Price: ${prop.get('price', 'N/A')}")
            print(f"   Status: {prop.get('status', 'Unknown')}")
            print()
            
    except Exception as e:
        print(f"Error listing properties: {e}")
    ```

=== "Create Property"
    ```python
    new_property = {
        "address": "123 Main St, Anytown, ST 12345",
        "price": 350000,
        "bedrooms": 3,
        "bathrooms": 2,
        "square_feet": 1800,
        "status": "active"
    }

    try:
        property_obj = client.properties.create_property(new_property)
        print(f"✅ Created property with ID: {property_obj['id']}")
        print(f"   Address: {property_obj['address']}")
    except Exception as e:
        print(f"❌ Error creating property: {e}")
    ```

### Working with Property Documents

!!! example "📄 Document Management"

=== "List Documents"
    ```python
    property_id = 123  # Replace with actual property ID

    try:
        documents = client.property_documents.list_property_documents(property_id)
        print(f"Property has {len(documents)} documents")
        
        for doc in documents:
            print(f"📄 {doc.get('title', 'Untitled')}")
            print(f"   Type: {doc.get('document_type', 'Unknown')}")
            print(f"   Description: {doc.get('description', 'No description')}")
            print()
            
    except Exception as e:
        print(f"Error listing documents: {e}")
    ```

=== "Add Document"
    ```python
    property_id = 123  # Replace with actual property ID
    
    new_document = {
        "title": "Purchase Agreement",
        "description": "Initial purchase agreement draft",
        "document_type": "contract"
    }

    try:
        document = client.property_documents.create_property_document(
            property_id, new_document
        )
        print(f"✅ Created document with ID: {document['id']}")
        print(f"   Title: {document['title']}")
    except Exception as e:
        print(f"❌ Error creating document: {e}")
    ```

## 🛡️ Step 5: Error Handling

!!! warning "⚠️ Production-Ready Error Handling"
    Always implement proper error handling for production applications.

=== "Comprehensive Example"
    ```python
    from open_to_close import (
        OpenToCloseAPI,
        AuthenticationError,
        ValidationError,
        NotFoundError,
        RateLimitError
    )

    client = OpenToCloseAPI()

    def safe_get_contact(contact_id):
        try:
            contact = client.contacts.retrieve_contact(contact_id)
            return contact
        except NotFoundError:
            print(f"❌ Contact {contact_id} not found")
        except AuthenticationError:
            print("🔐 Check your API key")
        except ValidationError as e:
            print(f"📝 Invalid data: {e}")
        except RateLimitError:
            print("⏱️ Rate limit exceeded, please wait")
        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")
        return None

    # Usage
    contact = safe_get_contact(999999)
    if contact:
        print(f"Found contact: {contact['first_name']} {contact['last_name']}")
    ```

=== "Error Types"
    | Exception | When It Occurs | Typical Response |
    |-----------|----------------|------------------|
    | `AuthenticationError` | Invalid API key | Check credentials |
    | `NotFoundError` | Resource doesn't exist | Verify ID or create new |
    | `ValidationError` | Invalid request data | Fix data format |
    | `RateLimitError` | Too many requests | Wait and retry |
    | `ConnectionError` | Network issues | Check internet connection |

## 🚀 Step 6: Available Resources

!!! info "📚 Complete Resource Overview"
    The client provides access to all Open To Close API resources with consistent interfaces.

<div class="grid cards" markdown>

-   :material-account:{ .lg .middle } **Agents**

    ---

    `client.agents` - Agent management and profiles

-   :material-contacts:{ .lg .middle } **Contacts**

    ---

    `client.contacts` - Customer contact management

-   :material-home:{ .lg .middle } **Properties**

    ---

    `client.properties` - Property listings and data

-   :material-account-group:{ .lg .middle } **Teams**

    ---

    `client.teams` - Team organization

-   :material-tag:{ .lg .middle } **Tags**

    ---

    `client.tags` - Flexible tagging system

-   :material-account-circle:{ .lg .middle } **Users**

    ---

    `client.users` - User account management

-   :material-file-document:{ .lg .middle } **Property Documents**

    ---

    `client.property_documents` - Document management

-   :material-email:{ .lg .middle } **Property Emails**

    ---

    `client.property_emails` - Email communications

-   :material-note-text:{ .lg .middle } **Property Notes**

    ---

    `client.property_notes` - Notes and comments

-   :material-checkbox-marked-circle:{ .lg .middle } **Property Tasks**

    ---

    `client.property_tasks` - Task management

-   :material-account-multiple:{ .lg .middle } **Property Contacts**

    ---

    `client.property_contacts` - Contact relationships

-   :material-plus:{ .lg .middle } **More Resources**

    ---

    Additional endpoints and functionality

</div>

## 🎉 Step 7: Complete Example

Put it all together with a real-world scenario:

!!! example "🏆 Real-World Example"

```python
from open_to_close import OpenToCloseAPI, NotFoundError

def property_management_demo():
    """Complete example: Create contact, property, and add documentation."""
    
    client = OpenToCloseAPI()
    
    try:
        # 1. Create a new contact
        new_contact = {
            "first_name": "Sarah",
            "last_name": "Johnson",
            "email": "sarah.johnson@example.com",
            "phone": "+1555123456"
        }
        
        contact = client.contacts.create_contact(new_contact)
        print(f"✅ Created contact: {contact['first_name']} {contact['last_name']}")
        
        # 2. Create a property
        new_property = {
            "address": "456 Oak Street, Springfield, IL 62701",
            "price": 275000,
            "bedrooms": 3,
            "bathrooms": 2,
            "square_feet": 1650,
            "status": "active"
        }
        
        property_obj = client.properties.create_property(new_property)
        print(f"✅ Created property: {property_obj['address']}")
        
        # 3. Add property documentation
        document = {
            "title": "Property Inspection Report",
            "description": "Initial property inspection findings",
            "document_type": "inspection"
        }
        
        doc = client.property_documents.create_property_document(
            property_obj['id'], document
        )
        print(f"✅ Added document: {doc['title']}")
        
        # 4. Create property task
        task = {
            "title": "Schedule showing",
            "description": "Coordinate with Sarah Johnson for property viewing",
            "due_date": "2024-01-15",
            "priority": "high"
        }
        
        new_task = client.property_tasks.create_property_task(
            property_obj['id'], task
        )
        print(f"✅ Created task: {new_task['title']}")
        
        print("\n🎉 Complete workflow executed successfully!")
        
    except Exception as e:
        print(f"❌ Error in workflow: {e}")

if __name__ == "__main__":
    property_management_demo()
```

## 📋 What's Next?

Choose your learning path:

<div class="grid cards" markdown>

-   :material-code-tags:{ .lg .middle } **Examples**

    ---

    Comprehensive real-world usage examples and patterns

    [:octicons-arrow-right-24: View Examples](../guides/examples.md)

-   :material-api:{ .lg .middle } **API Reference**

    ---

    Complete technical documentation for all methods

    [:octicons-arrow-right-24: API Documentation](../reference/api-reference.md)

-   :material-wrench:{ .lg .middle } **Troubleshooting**

    ---

    Common issues, solutions, and debugging tips

    [:octicons-arrow-right-24: Get Help](../guides/troubleshooting.md)

-   :material-github:{ .lg .middle } **Contributing**

    ---

    Join our development community

    [:octicons-arrow-right-24: Contribute](../development/contributing.md)

</div>

!!! success "🎯 Congratulations!"
    You've successfully completed the quick start guide! You now know how to:
    
    - ✅ Initialize the API client
    - ✅ Perform CRUD operations  
    - ✅ Handle errors properly
    - ✅ Work with multiple resources
    - ✅ Build complete workflows

    **Ready for more?** Check out our comprehensive examples and API reference for advanced usage patterns. 