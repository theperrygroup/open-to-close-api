# API Reference

Complete reference for all Open To Close API client methods.

---

## :material-api: Client Initialization

### OpenToCloseAPI

Initialize the main API client to access all endpoints.

=== "Basic Usage"

    ```python
    from open_to_close import OpenToCloseAPI

    # Load API key from environment variable
    client = OpenToCloseAPI()
    ```

=== "With API Key"

    ```python
    from open_to_close import OpenToCloseAPI

    # Explicit API key
    client = OpenToCloseAPI(api_key="your_api_key_here")
    ```

=== "Custom Base URL"

    ```python
    from open_to_close import OpenToCloseAPI

    # Custom API endpoint
    client = OpenToCloseAPI(
        api_key="your_api_key_here",
        base_url="https://staging-api.opentoclose.com/v1"
    )
    ```

!!! info "Parameters"
    - **`api_key`** `str, optional` - API key for authentication. If not provided, loads from `OPEN_TO_CLOSE_API_KEY` environment variable
    - **`base_url`** `str, optional` - Base URL for the API. Defaults to production URL

---

## :material-account-group: Agents API

Manage real estate agents in the system.

### :material-format-list-bulleted: `client.agents.list_agents(params=None)`

Retrieve a list of agents with optional filtering.

=== "Basic Example"

    ```python
    # Get all agents
    agents = client.agents.list_agents()
    print(f"Found {len(agents)} agents")
    ```

=== "With Filtering"

    ```python
    # Filter active agents with pagination
    agents = client.agents.list_agents(params={
        "limit": 50,
        "active": True,
        "office_id": 123
    })
    ```

=== "Response Example"

    ```json
    [
      {
        "id": 1,
        "name": "John Doe",
        "email": "john@realty.com",
        "phone": "+1234567890",
        "license_number": "ABC123",
        "active": true,
        "office_id": 123
      }
    ]
    ```

!!! success "Returns"
    **`List[Dict[str, Any]]`** - List of agent objects

!!! tip "Query Parameters"
    - `limit` - Number of results to return
    - `offset` - Number of results to skip
    - `active` - Filter by active status
    - `office_id` - Filter by office

### :material-plus-circle: `client.agents.create_agent(agent_data)`

Create a new agent in the system.

=== "Example"

    ```python
    new_agent = client.agents.create_agent({
        "name": "Jane Smith",
        "email": "jane@realty.com",
        "phone": "+1987654321",
        "license_number": "XYZ789",
        "office_id": 123
    })
    print(f"Created agent with ID: {new_agent['id']}")
    ```

=== "Required Fields"

    | Field | Type | Description |
    |-------|------|-------------|
    | `name` | `str` | Full name of the agent |
    | `email` | `str` | Email address |
    | `license_number` | `str` | Real estate license number |

=== "Optional Fields"

    | Field | Type | Description |
    |-------|------|-------------|
    | `phone` | `str` | Phone number |
    | `office_id` | `int` | Associated office ID |
    | `bio` | `str` | Agent biography |
    | `specialties` | `List[str]` | Areas of specialization |

!!! success "Returns"
    **`Dict[str, Any]`** - Created agent object with assigned ID

### :material-file-find: `client.agents.retrieve_agent(agent_id)`

Retrieve a specific agent by ID.

=== "Example"

    ```python
    agent = client.agents.retrieve_agent(123)
    print(f"Agent: {agent['name']} - {agent['email']}")
    ```

=== "Error Handling"

    ```python
    from open_to_close import NotFoundError

    try:
        agent = client.agents.retrieve_agent(999999)
    except NotFoundError:
        print("Agent not found!")
    ```

!!! info "Parameters"
    - **`agent_id`** `int` - Unique agent identifier

!!! success "Returns"
    **`Dict[str, Any]`** - Agent object

!!! warning "Exceptions"
    - `NotFoundError` - Agent with specified ID doesn't exist
    - `AuthenticationError` - Invalid API key

### :material-pencil: `client.agents.update_agent(agent_id, agent_data)`

Update an existing agent's information.

=== "Example"

    ```python
    updated_agent = client.agents.update_agent(123, {
        "phone": "+1555123456",
        "bio": "Specialist in luxury homes",
        "specialties": ["luxury", "waterfront"]
    })
    ```

=== "Partial Updates"

    ```python
    # Update only specific fields
    agent = client.agents.update_agent(123, {
        "active": False  # Deactivate agent
    })
    ```

!!! info "Parameters"
    - **`agent_id`** `int` - Agent ID to update
    - **`agent_data`** `dict` - Fields to update (partial updates supported)

!!! success "Returns"
    **`Dict[str, Any]`** - Updated agent object

### :material-delete: `client.agents.delete_agent(agent_id)`

Delete an agent from the system.

!!! danger "Warning"
    This action is irreversible. Consider deactivating instead of deleting.

=== "Example"

    ```python
    response = client.agents.delete_agent(123)
    print("Agent deleted successfully")
    ```

=== "Safe Alternative"

    ```python
    # Recommended: Deactivate instead of delete
    client.agents.update_agent(123, {"active": False})
    ```

!!! info "Parameters"
    - **`agent_id`** `int` - Agent ID to delete

!!! success "Returns"
    **`Dict[str, Any]`** - API response confirming deletion

---

## :material-account: Contacts API

Manage customer contacts and leads.

### :material-format-list-bulleted: `client.contacts.list_contacts(params=None)`

Retrieve a list of contacts with optional filtering and search.

=== "Basic Example"

    ```python
    contacts = client.contacts.list_contacts()
    for contact in contacts[:5]:  # Show first 5
        print(f"{contact['first_name']} {contact['last_name']}")
    ```

=== "Advanced Filtering"

    ```python
    # Search and filter contacts
    contacts = client.contacts.list_contacts(params={
        "search": "john",
        "email__contains": "@gmail.com",
        "created_after": "2024-01-01",
        "limit": 25
    })
    ```

=== "Response Structure"

    ```json
    [
      {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "created_at": "2024-01-15T10:30:00Z",
        "properties": []
      }
    ]
    ```

!!! success "Returns"
    **`List[Dict[str, Any]]`** - List of contact objects

!!! tip "Search & Filter Options"
    - `search` - Search across name and email
    - `email__contains` - Filter by email domain
    - `created_after` / `created_before` - Date range filtering
    - `has_properties` - Filter contacts with/without properties

### :material-plus-circle: `client.contacts.create_contact(contact_data)`

Create a new contact in the system.

=== "Basic Contact"

    ```python
    contact = client.contacts.create_contact({
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com"
    })
    print(f"Created contact: {contact['id']}")
    ```

=== "Complete Contact"

    ```python
    contact = client.contacts.create_contact({
        "first_name": "Michael",
        "last_name": "Johnson",
        "email": "michael@example.com",
        "phone": "+1987654321",
        "address": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip_code": "12345",
        "contact_type": "buyer",
        "notes": "First-time homebuyer"
    })
    ```

!!! info "Required Fields"
    - **`first_name`** `str` - Contact's first name
    - **`last_name`** `str` - Contact's last name
    - **`email`** `str` - Valid email address

!!! note "Optional Fields"
    All other fields are optional and can be added later via `update_contact()`

!!! success "Returns"
    **`Dict[str, Any]`** - Created contact object with assigned ID

### :material-file-find: `client.contacts.retrieve_contact(contact_id)`

Retrieve a specific contact by ID.

=== "Basic Retrieval"

    ```python
    contact = client.contacts.retrieve_contact(123)
    print(f"Contact: {contact['first_name']} {contact['last_name']}")
    print(f"Email: {contact['email']}")
    ```

=== "With Properties"

    ```python
    contact = client.contacts.retrieve_contact(123)
    if contact.get('properties'):
        print(f"Properties: {len(contact['properties'])}")
        for prop in contact['properties']:
            print(f"  - {prop['address']}")
    ```

!!! info "Parameters"
    - **`contact_id`** `int` - Unique contact identifier

!!! success "Returns"
    **`Dict[str, Any]`** - Complete contact object including associated properties

### :material-pencil: `client.contacts.update_contact(contact_id, contact_data)`

Update an existing contact's information.

=== "Update Contact Info"

    ```python
    updated_contact = client.contacts.update_contact(123, {
        "phone": "+1555987654",
        "address": "456 Oak Avenue",
        "contact_type": "seller"
    })
    ```

=== "Add Notes"

    ```python
    # Append to existing notes
    contact = client.contacts.retrieve_contact(123)
    existing_notes = contact.get('notes', '')
    
    updated_contact = client.contacts.update_contact(123, {
        "notes": f"{existing_notes}\n\nUpdated: Ready to view properties"
    })
    ```

!!! info "Parameters"
    - **`contact_id`** `int` - Contact ID to update  
    - **`contact_data`** `dict` - Fields to update (supports partial updates)

!!! success "Returns"
    **`Dict[str, Any]`** - Updated contact object

### :material-delete: `client.contacts.delete_contact(contact_id)`

Delete a contact from the system.

!!! danger "Permanent Action"
    Deleting a contact will also remove all associated property relationships and notes.

=== "Delete Contact"

    ```python
    response = client.contacts.delete_contact(123)
    print("Contact deleted successfully")
    ```

=== "Safer Alternative"

    ```python
    # Mark as inactive instead of deleting
    client.contacts.update_contact(123, {
        "active": False,
        "notes": "Contact marked inactive on 2024-01-15"
    })
    ```

!!! info "Parameters"
    - **`contact_id`** `int` - Contact ID to delete

!!! success "Returns"
    **`Dict[str, Any]`** - API response confirming deletion

---

## :material-home: Properties API

Manage properties in the system.

### :material-format-list-bulleted: `client.properties.list_properties(params=None)`

Retrieve a list of properties with filtering options.

=== "All Properties"

    ```python
    properties = client.properties.list_properties()
    print(f"Total properties: {len(properties)}")
    ```

=== "Filter by Status"

    ```python
    # Get active listings
    active_properties = client.properties.list_properties(params={
        "status": "active",
        "property_type": "single_family",
        "limit": 50
    })
    ```

=== "Location Search"

    ```python
    # Search by location
    properties = client.properties.list_properties(params={
        "city": "San Francisco",
        "state": "CA",
        "min_price": 500000,
        "max_price": 1500000
    })
    ```

!!! success "Returns"
    **`List[Dict[str, Any]]`** - List of property objects

!!! tip "Filter Options"
    - `status` - Property status (active, pending, sold, etc.)
    - `property_type` - Type of property
    - `city`, `state`, `zip_code` - Location filters
    - `min_price`, `max_price` - Price range
    - `bedrooms`, `bathrooms` - Room counts

### :material-plus-circle: `client.properties.create_property(property_data)`

Create a new property listing.

=== "Basic Property"

    ```python
    property = client.properties.create_property({
        "address": "123 Main Street",
        "city": "Anytown", 
        "state": "CA",
        "zip_code": "12345",
        "property_type": "single_family"
    })
    ```

=== "Complete Listing"

    ```python
    property = client.properties.create_property({
        "address": "456 Oak Avenue",
        "city": "San Francisco",
        "state": "CA", 
        "zip_code": "94102",
        "property_type": "condo",
        "bedrooms": 2,
        "bathrooms": 2,
        "square_feet": 1200,
        "list_price": 850000,
        "description": "Beautiful 2BR/2BA condo in the heart of the city",
        "features": ["hardwood floors", "stainless appliances", "parking"],
        "status": "active"
    })
    ```

!!! info "Required Fields"
    - **`address`** `str` - Street address
    - **`city`** `str` - City name
    - **`state`** `str` - State abbreviation
    - **`zip_code`** `str` - ZIP/postal code
    - **`property_type`** `str` - Type of property

!!! success "Returns"
    **`Dict[str, Any]`** - Created property object with assigned ID

---

## :material-alert-circle: Error Handling

The client provides specific exception types for robust error handling.

### Exception Types

=== "Available Exceptions"

    ```python
    from open_to_close import (
        OpenToCloseAPIError,    # Base exception
        AuthenticationError,    # Invalid API key
        ValidationError,        # Invalid request data
        NotFoundError,         # Resource not found
        RateLimitError,        # Rate limit exceeded
        ServerError,           # Server errors (5xx)
        NetworkError          # Network issues
    )
    ```

=== "Error Handling Example"

    ```python
    try:
        contact = client.contacts.retrieve_contact(123)
        property = client.properties.create_property(property_data)
    except AuthenticationError:
        print("❌ Check your API key")
    except ValidationError as e:
        print(f"❌ Invalid data: {e}")
    except NotFoundError:
        print("❌ Contact not found")
    except RateLimitError:
        print("⏰ Rate limit exceeded, please wait")
    except ServerError:
        print("🔧 Server error, try again later")
    except NetworkError:
        print("🌐 Network connection issue")
    ```

=== "Best Practices"

    ```python
    import time
    from open_to_close import RateLimitError, NetworkError

    def retry_on_error(func, max_retries=3):
        """Retry function with exponential backoff"""
        for attempt in range(max_retries):
            try:
                return func()
            except (RateLimitError, NetworkError) as e:
                if attempt == max_retries - 1:
                    raise e
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retrying in {wait_time}s... ({attempt + 1}/{max_retries})")
                time.sleep(wait_time)
    ```

!!! warning "Rate Limiting"
    The API has rate limits. Use appropriate delays between requests and implement retry logic with exponential backoff.

---

## :material-page-next: Pagination

Handle large datasets efficiently with pagination.

=== "Basic Pagination"

    ```python
    # Get first page
    page_1 = client.contacts.list_contacts(params={
        "limit": 50,
        "offset": 0
    })

    # Get second page  
    page_2 = client.contacts.list_contacts(params={
        "limit": 50,
        "offset": 50
    })
    ```

=== "Iterate All Pages"

    ```python
    def get_all_contacts(client):
        """Get all contacts across multiple pages"""
        all_contacts = []
        offset = 0
        limit = 100
        
        while True:
            page = client.contacts.list_contacts(params={
                "limit": limit,
                "offset": offset
            })
            
            if not page:  # No more results
                break
                
            all_contacts.extend(page)
            offset += limit
            
            if len(page) < limit:  # Last page
                break
                
        return all_contacts
    ```

!!! tip "Pagination Parameters"
    - **`limit`** - Number of items per page (max 100)
    - **`offset`** - Number of items to skip
    - **`page`** - Page number (alternative to offset)

---

## :material-magnify: Search and Filtering

Powerful search and filtering capabilities across all resources.

=== "Text Search"

    ```python
    # Search contacts by name or email
    results = client.contacts.list_contacts(params={
        "search": "john smith"
    })

    # Search properties by address
    properties = client.properties.list_properties(params={
        "search": "Main Street"
    })
    ```

=== "Field-Specific Filters"

    ```python
    # Email domain filtering
    gmail_contacts = client.contacts.list_contacts(params={
        "email__contains": "@gmail.com"
    })

    # Date range filtering
    recent_contacts = client.contacts.list_contacts(params={
        "created_after": "2024-01-01",
        "created_before": "2024-12-31"
    })

    # Numeric range filtering
    properties = client.properties.list_properties(params={
        "min_price": 300000,
        "max_price": 600000,
        "bedrooms__gte": 3  # Greater than or equal to 3
    })
    ```

=== "Advanced Filtering"

    ```python
    # Multiple conditions
    luxury_properties = client.properties.list_properties(params={
        "property_type": "single_family",
        "min_price": 1000000,
        "city": "San Francisco",
        "bedrooms__gte": 4,
        "status": "active"
    })
    ```

!!! info "Filter Operators"
    - `field__contains` - Text contains substring
    - `field__gt` / `field__gte` - Greater than / greater than or equal
    - `field__lt` / `field__lte` - Less than / less than or equal
    - `field__in` - Value in list (e.g., `status__in=["active","pending"]`) 