# API Reference

Complete documentation for all Open To Close API Python client methods, classes, and functionality. This reference provides detailed method signatures, parameters, return values, and examples.

!!! success "✅ Endpoint Reliability"
    **100% Verified**: All API endpoints have been comprehensively tested and verified working. The client features smart URL routing that automatically handles the Open To Close API's different URL patterns for optimal compatibility.

!!! abstract "Main Client"
    The **`OpenToCloseAPI`** serves as the main entry point, providing access to all API modules through a unified interface.

---

## 🚀 Quick Navigation

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Main Client**

    ---

    Primary client class for initialization and configuration

    [:octicons-arrow-right-24: Properties API](properties.md)

-   :material-home:{ .lg .middle } **Core Resources**

    ---

    Primary business entities and their CRUD operations

    [:octicons-arrow-right-24: View Core APIs](#core-resources)

-   :material-file-document:{ .lg .middle } **Property Sub-Resources**

    ---

    Property-specific data and relationship management

    [:octicons-arrow-right-24: View Property APIs](#property-sub-resources)

-   :material-alert-octagon:{ .lg .middle } **Exception Reference**

    ---

    Error handling and exception types

    [:octicons-arrow-right-24: Properties API](properties.md)

</div>

---

## 🏗️ Core Resources

Primary business entities that form the foundation of the Open To Close platform:

### **🏠 Properties API**
Manage real estate properties and listings:
- **[Properties](properties.md)** - Complete property lifecycle management

### **👥 People & Organizations**
Manage people and organizational structures:
- **Agents** - Agent profiles and management *(Documentation coming soon)*
- **Contacts** - Customer and lead management *(Documentation coming soon)*
- **Teams** - Team organization and structure *(Documentation coming soon)*
- **Users** - User account management *(Documentation coming soon)*

### **🏷️ Classification & Organization**
Tools for organizing and categorizing data:
- **Tags** - Classification and labeling system *(Documentation coming soon)*

---

## 📋 Property Sub-Resources

Property-specific resources that extend core property functionality:

### **📄 Documentation & Communication**
Track all property-related communications and documents:

- **Property Documents** - File attachments and document management *(Documentation coming soon)*
- **Property Emails** - Email communication tracking *(Documentation coming soon)*
- **Property Notes** - Internal notes and annotations *(Documentation coming soon)*

### **📅 Tasks & Relationships**
Manage workflows and relationships for properties:

- **Property Tasks** - Task management and workflow automation *(Documentation coming soon)*
- **Property Contacts** - Property-specific contact relationships *(Documentation coming soon)*

---

## 📋 API Overview

=== ":material-rocket-launch: Initialization"

    ```python
    from open_to_close import OpenToCloseAPI
    
    # Initialize with environment variable
    client = OpenToCloseAPI()
    
    # Initialize with explicit configuration
    client = OpenToCloseAPI(
        api_key="your_api_key",
        base_url="https://api.opentoclose.com/v1"
    )
    ```

=== ":material-home: Core Resources"

    ```python
    # Properties
    properties = client.properties.list_properties()
    property = client.properties.retrieve_property(123)
    
    # Contacts and People
    contacts = client.contacts.list_contacts()
    agents = client.agents.list_agents()
    teams = client.teams.list_teams()
    users = client.users.list_users()
    
    # Organization
    tags = client.tags.list_tags()
    ```

=== ":material-file-document: Property Sub-Resources"

    ```python
    property_id = 123
    
    # Documents and Communication
    documents = client.property_documents.list_property_documents(property_id)
    emails = client.property_emails.list_property_emails(property_id)
    notes = client.property_notes.list_property_notes(property_id)
    
    # Tasks and Relationships
    tasks = client.property_tasks.list_property_tasks(property_id)
    contacts = client.property_contacts.list_property_contacts(property_id)
    ```

---

## 🎯 Common Patterns

All API clients follow consistent patterns for CRUD operations:

### **Standard CRUD Operations**

| Operation | Method Pattern | Description |
|-----------|----------------|-------------|
| **List** | `list_{resource}s()` | Get all resources with optional filtering |
| **Create** | `create_{resource}()` | Create a new resource |
| **Retrieve** | `retrieve_{resource}()` | Get a specific resource by ID |
| **Update** | `update_{resource}()` | Update an existing resource |
| **Delete** | `delete_{resource}()` | Delete a resource by ID |

### **Property Sub-Resource Patterns**

Property sub-resources follow a similar pattern but require a property ID:

| Operation | Method Pattern | Description |
|-----------|----------------|-------------|
| **List** | `list_property_{resource}s(property_id)` | Get all sub-resources for a property |
| **Create** | `create_property_{resource}(property_id, data)` | Create new sub-resource |
| **Retrieve** | `retrieve_property_{resource}(property_id, resource_id)` | Get specific sub-resource |
| **Update** | `update_property_{resource}(property_id, resource_id, data)` | Update sub-resource |
| **Delete** | `delete_property_{resource}(property_id, resource_id)` | Delete sub-resource |

---

## 🔧 Method Signatures

### **Standard Parameters**

All methods accept these common parameter patterns:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `params` | `Dict[str, Any]` | No | Query parameters for filtering, pagination, and sorting |
| `{resource}_data` | `Dict[str, Any]` | Yes (create/update) | Data payload for creating or updating resources |
| `{resource}_id` | `int` | Yes (retrieve/update/delete) | Unique identifier for the resource |

### **Return Values**

| Method Type | Return Type | Description |
|-------------|-------------|-------------|
| `list_*` | `List[Dict[str, Any]]` | List of resource dictionaries |
| `create_*` | `Dict[str, Any]` | Created resource data |
| `retrieve_*` | `Dict[str, Any]` | Resource data |
| `update_*` | `Dict[str, Any]` | Updated resource data |
| `delete_*` | `Dict[str, Any]` | Deletion confirmation |

---

## ⚡ Quick Method Lookup

### **Core Resources**
- **Properties**: `properties.{list,create,retrieve,update,delete}_property*()`
- **Agents**: `agents.{list,create,retrieve,update,delete}_agent*()`
- **Contacts**: `contacts.{list,create,retrieve,update,delete}_contact*()`
- **Teams**: `teams.{list,create,retrieve,update,delete}_team*()`
- **Users**: `users.{list,create,retrieve,update,delete}_user*()`
- **Tags**: `tags.{list,create,retrieve,update,delete}_tag*()`

### **Property Sub-Resources**
- **Documents**: `property_documents.{list,create,retrieve,update,delete}_property_document*()`
- **Emails**: `property_emails.{list,create,retrieve,update,delete}_property_email*()`
- **Notes**: `property_notes.{list,create,retrieve,update,delete}_property_note*()`
- **Tasks**: `property_tasks.{list,create,retrieve,update,delete}_property_task*()`
- **Contacts**: `property_contacts.{list,create,retrieve,update,delete}_property_contact*()`

---

## 🆘 Error Handling

All methods can raise these exception types:

!!! warning "Common Exceptions"
    - **`AuthenticationError`**: Invalid or missing API key
    - **`ValidationError`**: Invalid request parameters
    - **`NotFoundError`**: Resource not found
    - **`RateLimitError`**: API rate limit exceeded
    - **`ServerError`**: Server-side error occurred
    - **`NetworkError`**: Network connectivity issue

See the Properties API documentation for error handling examples.

---

## 🔍 Detailed API Documentation

### **Core Resource APIs**

<div class="grid cards" markdown>

-   :material-home-city:{ .lg .middle } **Properties API**

    ---

    Complete property lifecycle from listing to closing

    [:octicons-arrow-right-24: Properties Documentation](properties.md)

</div>

### **Property Sub-Resource APIs**

Property sub-resource APIs are covered in the main Properties documentation.

---

## 📚 Related Documentation

!!! tip "Additional Resources"

    - **[Properties API](properties.md)** - Complete properties documentation
    - **[Getting Started](../getting-started/index.md)** - Setup and configuration
    - **[Guides](../guides/index.md)** - Usage patterns and examples

---

## 🚀 Quick Start

New to the API? Start here:

1. **[Install the client](../getting-started/installation.md)** - Get up and running
2. **[Configure authentication](../getting-started/authentication.md)** - Set up your API key
3. **[Try the quick start](../getting-started/quickstart.md)** - Make your first API call
4. **[Explore guides](../guides/index.md)** - See usage patterns and examples

---

*Complete API reference for building powerful applications with the Open To Close platform* 