# Property Contacts API

The Property Contacts API manages relationships between people and specific properties. This enables tracking of roles like buyers, sellers, agents, inspectors, and other stakeholders involved in property transactions.

!!! abstract "PropertyContactsAPI Client"
    Access via `client.property_contacts` - provides full CRUD operations for property-contact relationships.

---

## 🚀 Quick Start

```python
from open_to_close import OpenToCloseAPI

client = OpenToCloseAPI()

# List contacts for a property
property_contacts = client.property_contacts.list_property_contacts(property_id=123)

# Link a contact to a property
new_link = client.property_contacts.create_property_contact(
    property_id=123,
    contact_data={
        "contact_id": 456,
        "role": "Buyer",
        "primary": True
    }
)
```

---

## 📋 Available Methods

| Method | Description | HTTP Endpoint |
|--------|-------------|---------------|
| `list_property_contacts()` | Get all contacts for a property | `GET /properties/{id}/contacts` |
| `create_property_contact()` | Link a contact to a property | `POST /properties/{id}/contacts` |
| `retrieve_property_contact()` | Get specific property-contact relationship | `GET /properties/{id}/contacts/{contact_id}` |
| `update_property_contact()` | Update property-contact relationship | `PUT /properties/{id}/contacts/{contact_id}` |
| `delete_property_contact()` | Remove contact from property | `DELETE /properties/{id}/contacts/{contact_id}` |

---

## 🔍 Method Documentation

### **list_property_contacts()**

Retrieve all contacts associated with a specific property.

```python
def list_property_contacts(
    self, 
    property_id: int,
    params: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]
```

**Parameters:**

| Name | Type | Required | Description | Default |
|------|------|----------|-------------|---------|
| `property_id` | `int` | Yes | Unique identifier of the property | - |
| `params` | `Dict[str, Any]` | No | Query parameters for filtering | `None` |

**Returns:**

| Type | Description |
|------|-------------|
| `List[Dict[str, Any]]` | List of property-contact relationship dictionaries |

**Example:**
```python
# Get all contacts for a property
contacts = client.property_contacts.list_property_contacts(property_id=123)

# Filter by role
buyers = client.property_contacts.list_property_contacts(
    property_id=123,
    params={"role": "Buyer"}
)
```

---

### **create_property_contact()**

Create a new relationship between a contact and a property.

```python
def create_property_contact(
    self, 
    property_id: int,
    contact_data: Dict[str, Any]
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `property_id` | `int` | Yes | Unique identifier of the property |
| `contact_data` | `Dict[str, Any]` | Yes | Contact relationship data |

**Common Contact Relationship Fields:**

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `contact_id` | `integer` | Yes | ID of the contact to link | `456` |
| `role` | `string` | No | Contact's role in the transaction | `"Buyer"` |
| `primary` | `boolean` | No | Whether this is the primary contact for this role | `true` |
| `start_date` | `string` | No | When the relationship started | `"2024-01-15"` |
| `notes` | `string` | No | Additional notes about the relationship | `"Decision maker"` |

**Example:**
```python
# Link buyer to property
buyer_link = client.property_contacts.create_property_contact(
    property_id=123,
    contact_data={
        "contact_id": 456,
        "role": "Buyer",
        "primary": True,
        "notes": "Primary decision maker"
    }
)
```

---

### **retrieve_property_contact()**

Get details about a specific property-contact relationship.

```python
def retrieve_property_contact(
    self, 
    property_id: int,
    contact_id: int
) -> Dict[str, Any]
```

**Example:**
```python
# Get specific property-contact relationship
relationship = client.property_contacts.retrieve_property_contact(
    property_id=123,
    contact_id=456
)
```

---

### **update_property_contact()**

Update an existing property-contact relationship.

```python
def update_property_contact(
    self, 
    property_id: int,
    contact_id: int,
    contact_data: Dict[str, Any]
) -> Dict[str, Any]
```

**Example:**
```python
# Update contact role
updated_relationship = client.property_contacts.update_property_contact(
    property_id=123,
    contact_id=456,
    contact_data={
        "role": "Seller",
        "primary": False
    }
)
```

---

### **delete_property_contact()**

Remove a contact's association with a property.

```python
def delete_property_contact(
    self, 
    property_id: int,
    contact_id: int
) -> Dict[str, Any]
```

**Example:**
```python
# Remove contact from property
result = client.property_contacts.delete_property_contact(
    property_id=123,
    contact_id=456
)
```

---

## 🏗️ Common Workflows

### **Complete Transaction Setup**

```python
def setup_property_transaction(property_id, buyers, sellers, agents):
    """Set up all contacts for a property transaction."""
    
    # Add sellers
    for i, seller in enumerate(sellers):
        client.property_contacts.create_property_contact(
            property_id=property_id,
            contact_data={
                "contact_id": seller["id"],
                "role": "Seller",
                "primary": i == 0  # First seller is primary
            }
        )
    
    # Add buyers
    for i, buyer in enumerate(buyers):
        client.property_contacts.create_property_contact(
            property_id=property_id,
            contact_data={
                "contact_id": buyer["id"],
                "role": "Buyer",
                "primary": i == 0  # First buyer is primary
            }
        )
    
    # Add agents
    for agent in agents:
        client.property_contacts.create_property_contact(
            property_id=property_id,
            contact_data={
                "contact_id": agent["id"],
                "role": agent["role"],  # "Listing Agent" or "Buyer Agent"
                "primary": True
            }
        )

# Usage
setup_property_transaction(
    property_id=123,
    buyers=[{"id": 101}, {"id": 102}],
    sellers=[{"id": 201}],
    agents=[
        {"id": 301, "role": "Listing Agent"},
        {"id": 302, "role": "Buyer Agent"}
    ]
)
```

---

## 📚 Related Resources

**Related APIs:**
- **[Properties API](properties.md)** - Property management
- **[Contacts API](contacts.md)** - Contact management
- **[Agents API](agents.md)** - Agent management

---

*Property contacts enable comprehensive relationship tracking for real estate transactions.* 