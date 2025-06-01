# API Reference

Complete technical reference for all Open To Close API client methods with comprehensive examples and error handling guides.

!!! info "🔍 What You'll Find Here"
    This reference covers every available method, parameter, and response format. All examples are tested and production-ready.

## 🎯 API Overview

<div class="grid cards" markdown>

-   :material-api:{ .lg .middle } **Client Setup**

    ---

    Initialize and configure the API client for your application

    [:octicons-arrow-right-24: Client Initialization](#client-initialization)

-   :material-account-group:{ .lg .middle } **Agents API**

    ---

    Manage real estate agents and their profiles

    [:octicons-arrow-right-24: Agents Methods](#agents-api)

-   :material-contacts:{ .lg .middle } **Contacts API**

    ---

    Handle customer contacts and lead management

    [:octicons-arrow-right-24: Contacts Methods](#contacts-api)

-   :material-home:{ .lg .middle } **Properties API**

    ---

    Manage property listings and related data

    [:octicons-arrow-right-24: Properties Methods](#properties-api)

-   :material-file-document:{ .lg .middle } **Property Relations**

    ---

    Documents, emails, notes, tasks, and contact relationships

    [:octicons-arrow-right-24: Relationship APIs](#property-relations-api)

-   :material-alert-circle:{ .lg .middle } **Error Handling**

    ---

    Exception types and robust error handling patterns

    [:octicons-arrow-right-24: Error Reference](#error-handling)

</div>

## 🔧 Client Initialization

### OpenToCloseAPI

Initialize the main API client to access all endpoints.

!!! example "🚀 Client Setup Examples"

=== "Environment Variable (Recommended)"
    ```python
    from open_to_close import OpenToCloseAPI

    # Load API key from OPEN_TO_CLOSE_API_KEY environment variable
    client = OpenToCloseAPI()
    ```

    !!! tip "💡 Best Practice"
        Using environment variables keeps your API key secure and out of your code.

=== "Direct API Key"
    ```python
    from open_to_close import OpenToCloseAPI

    # Explicit API key (not recommended for production)
    client = OpenToCloseAPI(api_key="your_api_key_here")
    ```

    !!! warning "⚠️ Security Note"
        Only use direct API keys for testing. Never commit API keys to version control.

=== "Custom Configuration"
    ```python
    from open_to_close import OpenToCloseAPI

    # Custom API endpoint and settings
    client = OpenToCloseAPI(
        api_key="your_api_key_here",
        base_url="https://staging-api.opentoclose.com/v1",
        timeout=30,
        retry_count=3
    )
    ```

!!! info "📋 Parameters"
    | Parameter | Type | Description | Default |
    |-----------|------|-------------|---------|
    | **`api_key`** | `str, optional` | API key for authentication | From environment |
    | **`base_url`** | `str, optional` | Base URL for the API | Production URL |
    | **`timeout`** | `int, optional` | Request timeout in seconds | 30 |
    | **`retry_count`** | `int, optional` | Number of retry attempts | 3 |

---

## 👥 Agents API

Manage real estate agents in the system.

!!! success "✅ Available Methods"
    - `list_agents()` - Get all agents with filtering
    - `create_agent()` - Add new agent to system
    - `retrieve_agent()` - Get specific agent details
    - `update_agent()` - Modify agent information
    - `delete_agent()` - Remove agent from system

### :material-format-list-bulleted: `client.agents.list_agents(params=None)`

Retrieve a list of agents with optional filtering.

!!! example "📋 Agent Listing Examples"

=== "Basic Listing"
    ```python
    # Get all agents
    agents = client.agents.list_agents()
    print(f"Found {len(agents)} agents")
    
    for agent in agents[:5]:  # Show first 5
        print(f"- {agent['name']} ({agent['email']})")
    ```

=== "Advanced Filtering"
    ```python
    # Filter active agents with pagination
    agents = client.agents.list_agents(params={
        "limit": 50,
        "active": True,
        "office_id": 123,
        "license_state": "CA"
    })
    
    print(f"Found {len(agents)} active agents in California")
    ```

=== "Response Structure"
    ```json
    [
      {
        "id": 1,
        "name": "John Doe",
        "email": "john@realty.com",
        "phone": "+1234567890",
        "license_number": "ABC123",
        "active": true,
        "office_id": 123,
        "specialties": ["luxury", "first-time-buyers"],
        "created_at": "2024-01-15T10:30:00Z"
      }
    ]
    ```

!!! success "Returns"
    **`List[Dict[str, Any]]`** - List of agent objects

!!! tip "🔍 Query Parameters"
    | Parameter | Type | Description |
    |-----------|------|-------------|
    | `limit` | `int` | Number of results to return (max 100) |
    | `offset` | `int` | Number of results to skip |
    | `active` | `bool` | Filter by active status |
    | `office_id` | `int` | Filter by office |
    | `license_state` | `str` | Filter by license state |

### :material-plus-circle: `client.agents.create_agent(agent_data)`

Create a new agent in the system.

!!! example "👤 Agent Creation Examples"

=== "Basic Agent"
    ```python
    new_agent = client.agents.create_agent({
        "name": "Jane Smith",
        "email": "jane@realty.com",
        "license_number": "XYZ789"
    })
    print(f"Created agent with ID: {new_agent['id']}")
    ```

=== "Complete Agent Profile"
    ```python
    agent_data = {
        "name": "Michael Johnson",
        "email": "michael@realty.com",
        "phone": "+1987654321",
        "license_number": "DEF456",
        "office_id": 123,
        "bio": "Specialist in luxury waterfront properties",
        "specialties": ["luxury", "waterfront", "investment"],
        "years_experience": 8,
        "languages": ["English", "Spanish"]
    }
    
    new_agent = client.agents.create_agent(agent_data)
    print(f"✅ Created agent: {new_agent['name']}")
    ```

!!! info "📋 Required Fields"
    | Field | Type | Description |
    |-------|------|-------------|
    | **`name`** | `str` | Full name of the agent |
    | **`email`** | `str` | Valid email address |
    | **`license_number`** | `str` | Real estate license number |

!!! note "📝 Optional Fields"
    | Field | Type | Description |
    |-------|------|-------------|
    | `phone` | `str` | Phone number |
    | `office_id` | `int` | Associated office ID |
    | `bio` | `str` | Agent biography |
    | `specialties` | `List[str]` | Areas of specialization |
    | `years_experience` | `int` | Years in real estate |
    | `languages` | `List[str]` | Languages spoken |

!!! success "Returns"
    **`Dict[str, Any]`** - Created agent object with assigned ID

### :material-file-find: `client.agents.retrieve_agent(agent_id)`

Retrieve a specific agent by ID.

!!! example "🔍 Agent Retrieval Examples"

=== "Basic Retrieval"
    ```python
    agent = client.agents.retrieve_agent(123)
    print(f"Agent: {agent['name']} - {agent['email']}")
    print(f"License: {agent['license_number']}")
    
    if agent.get('specialties'):
        print(f"Specialties: {', '.join(agent['specialties'])}")
    ```

=== "With Error Handling"
    ```python
    from open_to_close import NotFoundError

    try:
        agent = client.agents.retrieve_agent(999999)
        print(f"Found agent: {agent['name']}")
    except NotFoundError:
        print("❌ Agent not found!")
    ```

!!! info "📋 Parameters"
    - **`agent_id`** `int` - Unique agent identifier

!!! success "Returns"
    **`Dict[str, Any]`** - Complete agent object with all fields

!!! warning "⚠️ Exceptions"
    - `NotFoundError` - Agent with specified ID doesn't exist
    - `AuthenticationError` - Invalid API key

### :material-pencil: `client.agents.update_agent(agent_id, agent_data)`

Update an existing agent's information.

!!! example "✏️ Agent Update Examples"

=== "Partial Update"
    ```python
    updated_agent = client.agents.update_agent(123, {
        "phone": "+1555123456",
        "bio": "Specialist in luxury homes and investment properties"
    })
    print(f"✅ Updated agent: {updated_agent['name']}")
    ```

=== "Status Changes"
    ```python
    # Deactivate agent
    agent = client.agents.update_agent(123, {
        "active": False,
        "notes": "Agent moved to different office"
    })
    
    # Update specialties
    agent = client.agents.update_agent(123, {
        "specialties": ["luxury", "waterfront", "commercial"]
    })
    ```

!!! info "📋 Parameters"
    - **`agent_id`** `int` - Agent ID to update
    - **`agent_data`** `dict` - Fields to update (partial updates supported)

!!! success "Returns"
    **`Dict[str, Any]`** - Updated agent object

### :material-delete: `client.agents.delete_agent(agent_id)`

Delete an agent from the system.

!!! danger "🚨 Permanent Action"
    This action is irreversible and will remove all agent associations. Consider deactivating instead.

!!! example "🗑️ Agent Deletion Examples"

=== "Delete Agent"
    ```python
    response = client.agents.delete_agent(123)
    print("✅ Agent deleted successfully")
    ```

=== "Recommended Alternative"
    ```python
    # Safer approach: Deactivate instead of delete
    client.agents.update_agent(123, {
        "active": False,
        "notes": "Agent account deactivated on 2024-01-15"
    })
    print("✅ Agent deactivated safely")
    ```

!!! info "📋 Parameters"
    - **`agent_id`** `int` - Agent ID to delete

!!! success "Returns"
    **`Dict[str, Any]`** - API response confirming deletion

---

## 👥 Contacts API

Manage customer contacts and leads.

!!! success "✅ Available Methods"
    - `list_contacts()` - Get all contacts with filtering
    - `create_contact()` - Add new contact to system
    - `retrieve_contact()` - Get specific contact details  
    - `update_contact()` - Modify contact information
    - `delete_contact()` - Remove contact from system

### :material-format-list-bulleted: `client.contacts.list_contacts(params=None)`

Retrieve a list of contacts with optional filtering and search.

!!! example "📋 Contact Listing Examples"

=== "Basic Listing"
    ```python
    contacts = client.contacts.list_contacts()
    for contact in contacts[:5]:  # Show first 5
        name = f"{contact['first_name']} {contact['last_name']}"
        print(f"- {name} ({contact['email']})")
    ```

=== "Advanced Search & Filter"
    ```python
    # Search and filter contacts
    contacts = client.contacts.list_contacts(params={
        "search": "john",
        "email__contains": "@gmail.com",
        "contact_type": "buyer",
        "created_after": "2024-01-01",
        "limit": 25
    })
    
    print(f"Found {len(contacts)} buyer contacts named John with Gmail")
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
        "contact_type": "buyer",
        "address": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip_code": "12345",
        "created_at": "2024-01-15T10:30:00Z",
        "properties": []
      }
    ]
    ```

!!! success "Returns"
    **`List[Dict[str, Any]]`** - List of contact objects

!!! tip "🔍 Search & Filter Options"
    | Parameter | Description | Example |
    |-----------|-------------|---------|
    | `search` | Search across name and email | `"john smith"` |
    | `email__contains` | Filter by email domain | `"@gmail.com"` |
    | `contact_type` | Filter by contact type | `"buyer"`, `"seller"` |
    | `created_after` | Date range filtering | `"2024-01-01"` |
    | `has_properties` | Filter by property ownership | `true`, `false` |

### :material-plus-circle: `client.contacts.create_contact(contact_data)`

Create a new contact in the system.

!!! example "👤 Contact Creation Examples"

=== "Basic Contact"
    ```python
    contact = client.contacts.create_contact({
        "first_name": "Jane",
        "last_name": "Smith", 
        "email": "jane@example.com"
    })
    print(f"✅ Created contact with ID: {contact['id']}")
    ```

=== "Complete Contact Profile"
    ```python
    contact_data = {
        "first_name": "Michael",
        "last_name": "Johnson",
        "email": "michael@example.com",
        "phone": "+1987654321",
        "address": "456 Oak Street",
        "city": "San Francisco",
        "state": "CA",
        "zip_code": "94102",
        "contact_type": "buyer",
        "budget_min": 500000,
        "budget_max": 800000,
        "preferred_areas": ["SOMA", "Mission Bay"],
        "notes": "First-time homebuyer, pre-approved for $750k"
    }
    
    contact = client.contacts.create_contact(contact_data)
    print(f"✅ Created contact: {contact['first_name']} {contact['last_name']}")
    ```

!!! info "📋 Required Fields"
    | Field | Type | Description |
    |-------|------|-------------|
    | **`first_name`** | `str` | Contact's first name |
    | **`last_name`** | `str` | Contact's last name |
    | **`email`** | `str` | Valid email address |

!!! note "📝 Optional Fields"
    | Field | Type | Description |
    |-------|------|-------------|
    | `phone` | `str` | Phone number |
    | `contact_type` | `str` | Type: "buyer", "seller", "investor" |
    | `address`, `city`, `state`, `zip_code` | `str` | Contact address |
    | `budget_min`, `budget_max` | `int` | Budget range |
    | `preferred_areas` | `List[str]` | Preferred neighborhoods |
    | `notes` | `str` | Additional notes |

!!! success "Returns"
    **`Dict[str, Any]`** - Created contact object with assigned ID

### :material-file-find: `client.contacts.retrieve_contact(contact_id)`

Retrieve a specific contact by ID.

!!! example "🔍 Contact Retrieval Examples"

=== "Basic Retrieval"
    ```python
    contact = client.contacts.retrieve_contact(123)
    print(f"Contact: {contact['first_name']} {contact['last_name']}")
    print(f"Email: {contact['email']}")
    print(f"Type: {contact.get('contact_type', 'Not specified')}")
    ```

=== "With Property Information"
    ```python
    contact = client.contacts.retrieve_contact(123)
    
    if contact.get('properties'):
        print(f"📍 Properties ({len(contact['properties'])}):")
        for prop in contact['properties']:
            print(f"  - {prop['address']} (${prop.get('price', 'N/A')})")
    else:
        print("No properties associated")
    ```

!!! info "📋 Parameters"
    - **`contact_id`** `int` - Unique contact identifier

!!! success "Returns"
    **`Dict[str, Any]`** - Complete contact object including associated properties

### :material-pencil: `client.contacts.update_contact(contact_id, contact_data)`

Update an existing contact's information.

!!! example "✏️ Contact Update Examples"

=== "Basic Information Update"
    ```python
    updated_contact = client.contacts.update_contact(123, {
        "phone": "+1555987654",
        "address": "789 Pine Street",
        "contact_type": "seller"
    })
    print(f"✅ Updated contact: {updated_contact['first_name']}")
    ```

=== "Budget and Preferences"
    ```python
    # Update buyer preferences
    contact = client.contacts.update_contact(123, {
        "budget_min": 600000,
        "budget_max": 900000,
        "preferred_areas": ["SOMA", "Financial District", "Mission Bay"],
        "notes": "Budget increased after promotion. Interested in condos."
    })
    ```

=== "Append Notes"
    ```python
    # Get existing contact to preserve notes
    contact = client.contacts.retrieve_contact(123)
    existing_notes = contact.get('notes', '')
    
    updated_contact = client.contacts.update_contact(123, {
        "notes": f"{existing_notes}\n\n[{datetime.now().date()}] Viewed 3 properties today."
    })
    ```

!!! info "📋 Parameters"
    - **`contact_id`** `int` - Contact ID to update
    - **`contact_data`** `dict` - Fields to update (supports partial updates)

!!! success "Returns"
    **`Dict[str, Any]`** - Updated contact object

### :material-delete: `client.contacts.delete_contact(contact_id)`

Delete a contact from the system.

!!! danger "🚨 Permanent Action"
    Deleting a contact will also remove all associated property relationships and notes.

!!! example "🗑️ Contact Deletion Examples"

=== "Delete Contact"
    ```python
    response = client.contacts.delete_contact(123)
    print("✅ Contact deleted successfully")
    ```

=== "Recommended Alternative"
    ```python
    # Mark as inactive instead of deleting
    client.contacts.update_contact(123, {
        "active": False,
        "notes": "Contact marked inactive - moved out of area"
    })
    print("✅ Contact deactivated safely")
    ```

!!! info "📋 Parameters"
    - **`contact_id`** `int` - Contact ID to delete

!!! success "Returns"
    **`Dict[str, Any]`** - API response confirming deletion

---

## 🏠 Properties API

Manage properties in the system.

!!! success "✅ Available Methods"
    - `list_properties()` - Get all properties with filtering
    - `create_property()` - Add new property listing
    - `retrieve_property()` - Get specific property details
    - `update_property()` - Modify property information
    - `delete_property()` - Remove property from system

### :material-format-list-bulleted: `client.properties.list_properties(params=None)`

Retrieve a list of properties with filtering options.

!!! example "🏠 Property Listing Examples"

=== "All Properties"
    ```python
    properties = client.properties.list_properties()
    print(f"Total properties: {len(properties)}")
    
    for prop in properties[:3]:  # Show first 3
        print(f"📍 {prop.get('address', 'Address N/A')}")
        print(f"   ${prop.get('list_price', 'Price N/A'):,}")
    ```

=== "Filter by Status & Type"
    ```python
    # Get active single-family homes
    active_properties = client.properties.list_properties(params={
        "status": "active",
        "property_type": "single_family",
        "bedrooms__gte": 3,
        "limit": 50
    })
    
    print(f"Found {len(active_properties)} active 3+ BR homes")
    ```

=== "Location & Price Search"
    ```python
    # Search by location and price range
    properties = client.properties.list_properties(params={
        "city": "San Francisco",
        "state": "CA",
        "min_price": 500000,
        "max_price": 1500000,
        "property_type__in": ["condo", "townhouse"]
    })
    
    print(f"Found {len(properties)} SF condos/townhouses $500K-$1.5M")
    ```

!!! success "Returns"
    **`List[Dict[str, Any]]`** - List of property objects

!!! tip "🔍 Filter Options"
    | Parameter | Type | Description |
    |-----------|------|-------------|
    | `status` | `str` | "active", "pending", "sold", "off_market" |
    | `property_type` | `str` | "single_family", "condo", "townhouse", etc. |
    | `city`, `state`, `zip_code` | `str` | Location filters |
    | `min_price`, `max_price` | `int` | Price range |
    | `bedrooms`, `bathrooms` | `int` | Room counts |
    | `bedrooms__gte` | `int` | Minimum bedrooms |
    | `square_feet__gte` | `int` | Minimum square footage |

### :material-plus-circle: `client.properties.create_property(property_data)`

Create a new property listing.

!!! example "🏠 Property Creation Examples"

=== "Basic Property"
    ```python
    property_data = {
        "address": "123 Main Street",
        "city": "Anytown",
        "state": "CA", 
        "zip_code": "12345",
        "property_type": "single_family"
    }
    
    property_obj = client.properties.create_property(property_data)
    print(f"✅ Created property with ID: {property_obj['id']}")
    ```

=== "Complete Listing"
    ```python
    property_data = {
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
        "status": "active",
        "agent_id": 123,
        "listing_date": "2024-01-15"
    }
    
    property_obj = client.properties.create_property(property_data)
    print(f"✅ Listed property: {property_obj['address']}")
    ```

!!! info "📋 Required Fields"
    | Field | Type | Description |
    |-------|------|-------------|
    | **`address`** | `str` | Street address |
    | **`city`** | `str` | City name |
    | **`state`** | `str` | State abbreviation |
    | **`zip_code`** | `str` | ZIP/postal code |
    | **`property_type`** | `str` | Type of property |

!!! note "📝 Optional Fields"  
    | Field | Type | Description |
    |-------|------|-------------|
    | `bedrooms`, `bathrooms` | `int` | Room counts |
    | `square_feet` | `int` | Property size |
    | `list_price` | `int` | Listing price |
    | `description` | `str` | Property description |
    | `features` | `List[str]` | Property features |
    | `status` | `str` | Listing status |
    | `agent_id` | `int` | Listing agent |

!!! success "Returns"
    **`Dict[str, Any]`** - Created property object with assigned ID

---

## ⚠️ Error Handling

The client provides specific exception types for robust error handling.

!!! warning "🛡️ Production-Ready Error Handling"
    Always implement comprehensive error handling for production applications.

### Exception Types

!!! example "🚨 Available Exceptions"

=== "Exception Hierarchy"
    ```python
    from open_to_close import (
        OpenToCloseAPIError,    # Base exception
        AuthenticationError,    # Invalid API key
        ValidationError,        # Invalid request data
        NotFoundError,         # Resource not found
        RateLimitError,        # Rate limit exceeded
        ServerError,           # Server errors (5xx)
        NetworkError          # Network connection issues
    )
    ```

=== "Complete Error Handling"
    ```python
    from open_to_close import *
    
    def safe_api_call():
        try:
            contact = client.contacts.retrieve_contact(123)
            property_obj = client.properties.create_property(property_data)
            return contact, property_obj
            
        except AuthenticationError:
            print("🔐 Check your API key configuration")
            
        except ValidationError as e:
            print(f"📝 Invalid data: {e}")
            print("Please verify all required fields are included")
            
        except NotFoundError as e:
            print(f"🔍 Resource not found: {e}")
            
        except RateLimitError:
            print("⏱️ Rate limit exceeded, please wait before retrying")
            
        except ServerError as e:
            print(f"🔧 Server error: {e}")
            print("The issue is on our end, please try again later")
            
        except NetworkError as e:
            print(f"🌐 Network connection issue: {e}")
            
        except OpenToCloseAPIError as e:
            print(f"⚠️ Unexpected API error: {e}")
            
        return None, None
    ```

=== "Retry with Backoff"
    ```python
    import time
    from open_to_close import RateLimitError, NetworkError, ServerError

    def retry_api_call(func, max_retries=3, backoff_factor=2):
        """Execute API call with exponential backoff retry logic"""
        
        for attempt in range(max_retries):
            try:
                return func()
                
            except (RateLimitError, NetworkError, ServerError) as e:
                if attempt == max_retries - 1:
                    raise e  # Last attempt, re-raise the exception
                
                wait_time = backoff_factor ** attempt
                print(f"⏳ Retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
    
    # Usage
    def get_contact():
        return client.contacts.retrieve_contact(123)
    
    contact = retry_api_call(get_contact)
    ```

!!! info "📋 Exception Details"
    | Exception | HTTP Status | Description | Typical Response |
    |-----------|-------------|-------------|------------------|
    | `AuthenticationError` | 401 | Invalid API key | Check credentials |
    | `ValidationError` | 400 | Invalid request data | Fix data format |
    | `NotFoundError` | 404 | Resource doesn't exist | Verify ID |
    | `RateLimitError` | 429 | Too many requests | Wait and retry |
    | `ServerError` | 5xx | Server-side issues | Try again later |
    | `NetworkError` | - | Connection problems | Check internet |

---

## 📄 Pagination & Search

Handle large datasets efficiently with built-in pagination and powerful search capabilities.

### Pagination

!!! example "📄 Pagination Examples"

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
    
    print(f"Page 1: {len(page_1)} contacts")
    print(f"Page 2: {len(page_2)} contacts")
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
            print(f"📄 Loaded page with {len(page)} contacts")
            
            offset += limit
            
            if len(page) < limit:  # Last page
                break
                
        return all_contacts
    
    all_contacts = get_all_contacts(client)
    print(f"✅ Total contacts loaded: {len(all_contacts)}")
    ```

=== "Page-Based Pagination"
    ```python
    # Alternative: use page parameter instead of offset
    page_3 = client.properties.list_properties(params={
        "page": 3,
        "limit": 25
    })
    ```

!!! tip "📋 Pagination Parameters"
    | Parameter | Type | Description | Max Value |
    |-----------|------|-------------|-----------|
    | **`limit`** | `int` | Items per page | 100 |
    | **`offset`** | `int` | Items to skip | - |
    | **`page`** | `int` | Page number (alternative to offset) | - |

### Search and Filtering

!!! example "🔍 Search Examples"

=== "Text Search"
    ```python
    # Search contacts by name or email
    results = client.contacts.list_contacts(params={
        "search": "john smith"
    })

    # Search properties by address
    properties = client.properties.list_properties(params={
        "search": "Main Street San Francisco"
    })
    
    print(f"Found {len(results)} contacts and {len(properties)} properties")
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
    mid_range_properties = client.properties.list_properties(params={
        "min_price": 300000,
        "max_price": 600000,
        "bedrooms__gte": 3,  # Greater than or equal to 3
        "bathrooms__lte": 3   # Less than or equal to 3
    })
    ```

=== "Complex Filtering"
    ```python
    # Multiple conditions for luxury properties
    luxury_properties = client.properties.list_properties(params={
        "property_type__in": ["single_family", "condo"],
        "min_price": 1000000,
        "city__in": ["San Francisco", "Palo Alto", "Saratoga"],
        "bedrooms__gte": 4,
        "bathrooms__gte": 3,
        "square_feet__gte": 2000,
        "status": "active",
        "features__contains": "luxury"
    })
    
    print(f"Found {len(luxury_properties)} luxury properties")
    ```

!!! info "🔍 Filter Operators"
    | Operator | Description | Example |
    |----------|-------------|---------|
    | `field__contains` | Text contains substring | `email__contains="@gmail.com"` |
    | `field__in` | Value in list | `status__in=["active","pending"]` |
    | `field__gt` / `field__gte` | Greater than / equal | `price__gte=500000` |
    | `field__lt` / `field__lte` | Less than / equal | `bedrooms__lte=4` |
    | `field__startswith` | Text starts with | `address__startswith="123"` |
    | `field__endswith` | Text ends with | `email__endswith=".com"` |

---

## 📋 What's Next?

Choose your path for deeper exploration:

<div class="grid cards" markdown>

-   :material-code-tags:{ .lg .middle } **Usage Examples**

    ---

    Real-world examples and comprehensive implementation patterns

    [:octicons-arrow-right-24: View Examples](../guides/examples.md)

-   :material-rocket:{ .lg .middle } **Quick Start**

    ---

    Get up and running with a 5-minute tutorial

    [:octicons-arrow-right-24: Quick Start Guide](../getting-started/quickstart.md)

-   :material-wrench:{ .lg .middle } **Troubleshooting**

    ---

    Common issues, solutions, and debugging techniques

    [:octicons-arrow-right-24: Get Help](../guides/troubleshooting.md)

-   :material-github:{ .lg .middle } **Contributing**

    ---

    Join our development community and contribute improvements

    [:octicons-arrow-right-24: Contribute](../development/contributing.md)

</div>

!!! success "🎯 API Mastery Complete!"
    You now have comprehensive knowledge of all available API methods, parameters, and error handling patterns.
    
    **Key takeaways:**
    
    - ✅ All methods support comprehensive filtering and search
    - ✅ Built-in pagination handles large datasets efficiently  
    - ✅ Robust error handling with specific exception types
    - ✅ Production-ready examples with best practices
    
    **Ready to build?** Check out our examples guide for complete implementation patterns! 