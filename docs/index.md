# Open To Close API Python Client

A comprehensive Python client library for the Open To Close API, providing easy-to-use interfaces for all API endpoints with full type safety and comprehensive documentation.

!!! tip "🚀 Quick Start"
    Get up and running in under 5 minutes with our streamlined installation and setup process.

## 🎯 Quick Navigation

<div class="grid cards" markdown>

-   :material-rocket:{ .lg .middle } **Getting Started**

    ---

    Complete setup and installation guide to get you up and running quickly

    [:octicons-arrow-right-24: Start Here](getting-started/installation.md)

-   :material-flash:{ .lg .middle } **Quick Start**

    ---

    5-minute tutorial with working examples for immediate productivity

    [:octicons-arrow-right-24: Quick Start](getting-started/quickstart.md)

-   :material-api:{ .lg .middle } **API Reference**

    ---

    Complete technical documentation for all endpoints and methods

    [:octicons-arrow-right-24: API Docs](reference/api-reference.md)

-   :material-code-tags:{ .lg .middle } **Examples**

    ---

    Comprehensive usage examples and real-world implementation patterns

    [:octicons-arrow-right-24: View Examples](guides/examples.md)

-   :material-wrench:{ .lg .middle } **Troubleshooting**

    ---

    Common issues, solutions, and debugging techniques

    [:octicons-arrow-right-24: Get Help](guides/troubleshooting.md)

-   :material-account-group:{ .lg .middle } **Contributing**

    ---

    Development setup, guidelines, and contribution process

    [:octicons-arrow-right-24: Contribute](development/contributing.md)

</div>

## ✨ Key Features

=== "Core Features"
    !!! success "✅ Complete API Coverage"
        All Open To Close API endpoints supported with full functionality

    !!! success "✅ Type Safety"
        Full type hints and validation for better development experience

    !!! success "✅ Comprehensive Documentation"
        Google-style docstrings with examples for every method

=== "Developer Experience"
    !!! success "✅ Error Handling"
        Detailed exception handling with specific error types

    !!! success "✅ Easy Authentication"
        Environment variable or direct API key support

    !!! success "✅ Smart Features"
        Built-in pagination support and rate limit handling

## 🏠 Supported Resources

<div class="grid cards" markdown>

-   :material-account:{ .lg .middle } **Agents**

    ---

    Manage real estate agents and their profiles

-   :material-contacts:{ .lg .middle } **Contacts**

    ---

    Handle customer contacts and relationships

-   :material-home:{ .lg .middle } **Properties**

    ---

    Complete property management functionality

-   :material-file-document:{ .lg .middle } **Property Relations**

    ---

    Documents, emails, notes, tasks, and contacts

-   :material-account-group:{ .lg .middle } **Teams**

    ---

    Team management and organization

-   :material-tag:{ .lg .middle } **Tags**

    ---

    Flexible tagging and categorization system

-   :material-account-circle:{ .lg .middle } **Users**

    ---

    User management and authentication

-   :material-plus:{ .lg .middle } **And More**

    ---

    Additional endpoints and functionality

</div>

## 📊 Quick Example

=== "Simple Usage"
    ```python
    from open_to_close import OpenToCloseAPI

    # Initialize client
    client = OpenToCloseAPI()

    # Get contacts
    contacts = client.contacts.list_contacts()
    print(f"Found {len(contacts)} contacts")
    ```

=== "With Error Handling"
    ```python
    from open_to_close import OpenToCloseAPI, NotFoundError

    client = OpenToCloseAPI()

    try:
        contact = client.contacts.retrieve_contact(123)
        print(f"Contact: {contact['first_name']} {contact['last_name']}")
    except NotFoundError:
        print("Contact not found")
    ```

=== "Advanced Usage"
    ```python
    from open_to_close import OpenToCloseAPI

    client = OpenToCloseAPI()

    # Create a new contact with full details
    new_contact = {
        "first_name": "John",
        "last_name": "Doe", 
        "email": "john.doe@example.com",
        "phone": "+1234567890"
    }

    contact = client.contacts.create_contact(new_contact)
    print(f"Created contact with ID: {contact['id']}")
    ```

!!! info "💡 Pro Tip"
    All methods include comprehensive type hints and detailed docstrings. Use your IDE's autocomplete and inline documentation for the best development experience.

## 📈 Status

!!! success "✅ Production Ready"
    **Current Version**: Latest stable release with comprehensive testing
    
    **API Coverage**: All Open To Close API endpoints implemented and tested
    
    **Documentation**: Complete with examples and troubleshooting guides

## 🏢 Project Information

**Organization**: The Perry Group  
**Author**: John Perry  
**Email**: john@theperry.group  
**License**: MIT License  

## 📋 What's Next?

Choose your path based on your needs:

- 🚀 **New to the API?** → [Installation Guide](getting-started/installation.md)
- ⚡ **Want to jump in?** → [Quick Start Guide](getting-started/quickstart.md)  
- 📚 **Need examples?** → [Usage Examples](guides/examples.md)
- 🔍 **Looking for specifics?** → [API Reference](reference/api-reference.md)
- 🐛 **Having issues?** → [Troubleshooting Guide](guides/troubleshooting.md)

## 🔄 Latest Updates

Stay informed about new features and improvements:

- 📅 [**Changelog**](development/changelog.md) - Version history and updates
- 🚀 [**Deployment Guide**](development/deployment.md) - Release process and CI/CD
- 🤝 [**Contributing**](development/contributing.md) - Join our development community 