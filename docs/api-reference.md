# API Reference

Complete reference for all Open To Close API client methods.

## Client Initialization

### OpenToCloseAPI

```python
from open_to_close_api import OpenToCloseAPI

client = OpenToCloseAPI(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None
)
```

**Parameters:**
- `api_key` (str, optional): API key for authentication. If not provided, loads from `OPEN_TO_CLOSE_API_KEY` environment variable.
- `base_url` (str, optional): Base URL for the API. Defaults to production URL.

## Agents API

### client.agents

Manage real estate agents in the system.

#### list_agents(params=None)

Retrieve a list of agents.

**Parameters:**
- `params` (dict, optional): Query parameters for filtering

**Returns:** `List[Dict[str, Any]]` - List of agent objects

**Example:**
```python
# Get all agents
agents = client.agents.list_agents()

# Filter agents
agents = client.agents.list_agents(params={"limit": 50, "active": True})
```

#### create_agent(agent_data)

Create a new agent.

**Parameters:**
- `agent_data` (dict): Agent information

**Returns:** `Dict[str, Any]` - Created agent object

**Example:**
```python
agent = client.agents.create_agent({
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "license_number": "ABC123"
})
```

#### retrieve_agent(agent_id)

Retrieve a specific agent by ID.

**Parameters:**
- `agent_id` (int): Agent ID

**Returns:** `Dict[str, Any]` - Agent object

#### update_agent(agent_id, agent_data)

Update an existing agent.

**Parameters:**
- `agent_id` (int): Agent ID
- `agent_data` (dict): Fields to update

**Returns:** `Dict[str, Any]` - Updated agent object

#### delete_agent(agent_id)

Delete an agent.

**Parameters:**
- `agent_id` (int): Agent ID

**Returns:** `Dict[str, Any]` - API response

## Contacts API

### client.contacts

Manage customer contacts.

#### list_contacts(params=None)

Retrieve a list of contacts.

**Parameters:**
- `params` (dict, optional): Query parameters

**Returns:** `List[Dict[str, Any]]` - List of contact objects

#### create_contact(contact_data)

Create a new contact.

**Parameters:**
- `contact_data` (dict): Contact information

**Returns:** `Dict[str, Any]` - Created contact object

**Example:**
```python
contact = client.contacts.create_contact({
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane@example.com",
    "phone": "+1987654321"
})
```

#### retrieve_contact(contact_id)

Retrieve a specific contact by ID.

**Parameters:**
- `contact_id` (int): Contact ID

**Returns:** `Dict[str, Any]` - Contact object

#### update_contact(contact_id, contact_data)

Update an existing contact.

**Parameters:**
- `contact_id` (int): Contact ID
- `contact_data` (dict): Fields to update

**Returns:** `Dict[str, Any]` - Updated contact object

#### delete_contact(contact_id)

Delete a contact.

**Parameters:**
- `contact_id` (int): Contact ID

**Returns:** `Dict[str, Any]` - API response

## Properties API

### client.properties

Manage properties in the system.

#### list_properties(params=None)

Retrieve a list of properties.

**Parameters:**
- `params` (dict, optional): Query parameters

**Returns:** `List[Dict[str, Any]]` - List of property objects

#### create_property(property_data)

Create a new property.

**Parameters:**
- `property_data` (dict): Property information

**Returns:** `Dict[str, Any]` - Created property object

**Example:**
```python
property = client.properties.create_property({
    "address": "123 Main St",
    "city": "Anytown",
    "state": "CA",
    "zip_code": "12345",
    "property_type": "single_family"
})
```

#### retrieve_property(property_id)

Retrieve a specific property by ID.

#### update_property(property_id, property_data)

Update an existing property.

#### delete_property(property_id)

Delete a property.

## Property Documents API

### client.property_documents

Manage documents associated with properties.

#### list_property_documents(property_id, params=None)

List documents for a specific property.

**Parameters:**
- `property_id` (int): Property ID
- `params` (dict, optional): Query parameters

**Returns:** `List[Dict[str, Any]]` - List of document objects

#### create_property_document(property_id, document_data)

Create a new document for a property.

**Parameters:**
- `property_id` (int): Property ID
- `document_data` (dict): Document information

**Returns:** `Dict[str, Any]` - Created document object

**Example:**
```python
document = client.property_documents.create_property_document(123, {
    "title": "Purchase Agreement",
    "description": "Signed purchase agreement",
    "document_type": "contract",
    "file_url": "https://example.com/document.pdf"
})
```

#### retrieve_property_document(property_id, document_id)

Retrieve a specific document.

#### update_property_document(property_id, document_id, document_data)

Update a document.

#### delete_property_document(property_id, document_id)

Delete a document.

## Property Emails API

### client.property_emails

Manage emails related to properties.

#### list_property_emails(property_id, params=None)

List emails for a property.

#### create_property_email(property_id, email_data)

Create a new email record.

**Example:**
```python
email = client.property_emails.create_property_email(123, {
    "subject": "Property Update",
    "body": "Status update on the property",
    "to_email": "client@example.com",
    "from_email": "agent@realty.com"
})
```

## Property Notes API

### client.property_notes

Manage notes for properties.

#### list_property_notes(property_id, params=None)

List notes for a property.

#### create_property_note(property_id, note_data)

Create a new note.

**Example:**
```python
note = client.property_notes.create_property_note(123, {
    "title": "Inspection Notes",
    "content": "Property inspection completed successfully",
    "note_type": "inspection"
})
```

## Property Tasks API

### client.property_tasks

Manage tasks related to properties.

#### list_property_tasks(property_id, params=None)

List tasks for a property.

#### create_property_task(property_id, task_data)

Create a new task.

**Example:**
```python
task = client.property_tasks.create_property_task(123, {
    "title": "Schedule Inspection",
    "description": "Coordinate property inspection",
    "due_date": "2024-12-31",
    "priority": "high"
})
```

## Property Contacts API

### client.property_contacts

Manage contact relationships with properties.

#### list_property_contacts(property_id, params=None)

List contacts associated with a property.

#### create_property_contact(property_id, contact_data)

Associate a contact with a property.

## Teams API

### client.teams

Manage teams in the organization.

#### list_teams(params=None)

List all teams.

#### create_team(team_data)

Create a new team.

**Example:**
```python
team = client.teams.create_team({
    "name": "Downtown Sales Team",
    "description": "Handles downtown area sales",
    "manager_id": 123
})
```

## Tags API

### client.tags

Manage tags for organizing resources.

#### list_tags(params=None)

List all tags.

#### create_tag(tag_data)

Create a new tag.

**Example:**
```python
tag = client.tags.create_tag({
    "name": "First Time Buyer",
    "color": "#FF5733",
    "category": "client_type"
})
```

## Users API

### client.users

Manage system users.

#### list_users(params=None)

List all users.

#### create_user(user_data)

Create a new user.

**Example:**
```python
user = client.users.create_user({
    "email": "newuser@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "agent"
})
```

## Error Handling

All methods can raise the following exceptions:

- `OpenToCloseAPIError`: Base exception for all API errors
- `AuthenticationError`: Invalid or missing API key
- `ValidationError`: Invalid request data
- `NotFoundError`: Resource not found (404)
- `RateLimitError`: API rate limit exceeded
- `ServerError`: Server error (5xx status codes)
- `NetworkError`: Network connectivity issues

**Example:**
```python
from open_to_close_api import NotFoundError, ValidationError

try:
    contact = client.contacts.retrieve_contact(999999)
except NotFoundError:
    print("Contact does not exist")
except ValidationError as e:
    print(f"Invalid request: {e}")
```

## Pagination

For endpoints that return lists, you can use pagination parameters:

```python
# Get first page with 50 items
contacts = client.contacts.list_contacts(params={
    "limit": 50,
    "offset": 0
})

# Get second page
contacts = client.contacts.list_contacts(params={
    "limit": 50,
    "offset": 50
})
```

## Filtering and Searching

Many list endpoints support filtering and search parameters:

```python
# Filter contacts by email domain
contacts = client.contacts.list_contacts(params={
    "email__contains": "@example.com"
})

# Search properties by address
properties = client.properties.list_properties(params={
    "search": "Main Street"
})
``` 