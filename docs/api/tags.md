# Tags API

The Tags API provides a flexible classification and labeling system for organizing and categorizing data throughout the Open To Close platform. Tags enable efficient filtering, searching, and organization of properties, contacts, and other resources.

!!! abstract "TagsAPI Client"
    Access via `client.tags` - provides full CRUD operations for tag management.

---

## 🚀 Quick Start

```python
from open_to_close import OpenToCloseAPI

client = OpenToCloseAPI()

# List all tags
tags = client.tags.list_tags()

# Get a specific tag
tag_data = client.tags.retrieve_tag(123)

# Create a new tag
new_tag = client.tags.create_tag({
    "name": "Luxury Property",
    "description": "High-end luxury properties",
    "color": "#gold",
    "category": "Property Type"
})
```

---

## 📋 Available Methods

| Method | Description | HTTP Endpoint |
|--------|-------------|---------------|
| `list_tags()` | Get all tags with optional filtering | `GET /tags` |
| `create_tag()` | Create a new tag | `POST /tags` |
| `retrieve_tag()` | Get a specific tag by ID | `GET /tags/{id}` |
| `update_tag()` | Update an existing tag | `PUT /tags/{id}` |
| `delete_tag()` | Delete a tag by ID | `DELETE /tags/{id}` |

---

## 🔍 Method Documentation

### **list_tags()**

Retrieve a list of tags with optional filtering and pagination.

```python
def list_tags(
    self, 
    params: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]
```

**Parameters:**

| Name | Type | Required | Description | Default |
|------|------|----------|-------------|---------|
| `params` | `Dict[str, Any]` | No | Query parameters for filtering, pagination, and sorting | `None` |

**Returns:**

| Type | Description |
|------|-------------|
| `List[Dict[str, Any]]` | List of tag dictionaries |

**Common Query Parameters:**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `limit` | `int` | Maximum number of results to return | `50` |
| `offset` | `int` | Number of results to skip for pagination | `100` |
| `category` | `string` | Filter by tag category | `"Property Type"` |
| `search` | `string` | Search in tag name or description | `"luxury"` |
| `sort` | `string` | Sort field and direction | `"name"` |

=== ":material-list-box: Basic Listing"

    ```python
    # Get all tags
    tags = client.tags.list_tags()
    print(f"Found {len(tags)} tags")
    
    # Display basic info
    for tag in tags:
        print(f"Tag {tag['id']}: {tag.get('name', 'No name')} ({tag.get('category', 'No category')})")
    ```

=== ":material-filter: Filtered Results"

    ```python
    # Get property type tags
    property_tags = client.tags.list_tags(params={
        "category": "Property Type",
        "limit": 25
    })
    
    # Search for luxury-related tags
    luxury_tags = client.tags.list_tags(params={
        "search": "luxury",
        "sort": "name"
    })
    ```

---

### **create_tag()**

Create a new tag with the provided data.

```python
def create_tag(
    self, 
    tag_data: Dict[str, Any]
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tag_data` | `Dict[str, Any]` | Yes | Dictionary containing tag information |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Created tag data with assigned ID |

**Common Tag Fields:**

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `name` | `string` | No | Tag name | `"Luxury Property"` |
| `description` | `string` | No | Tag description | `"High-end properties"` |
| `color` | `string` | No | Tag color (hex or name) | `"#FFD700"` |
| `category` | `string` | No | Tag category | `"Property Type"` |
| `icon` | `string` | No | Tag icon identifier | `"diamond"` |
| `sort_order` | `integer` | No | Display sort order | `1` |

=== ":material-plus: Basic Creation"

    ```python
    # Create a basic tag
    new_tag = client.tags.create_tag({
        "name": "Waterfront",
        "description": "Properties with water access",
        "category": "Location Feature"
    })
    
    print(f"Created tag with ID: {new_tag['id']}")
    print(f"Name: {new_tag['name']}")
    ```

=== ":material-palette: Styled Tag"

    ```python
    # Create a comprehensive styled tag
    tag_data = {
        "name": "Historic District",
        "description": "Properties located in designated historic districts",
        "color": "#8B4513",
        "category": "Location Feature",
        "icon": "historic",
        "sort_order": 5,
        "active": True
    }
    
    new_tag = client.tags.create_tag(tag_data)
    print(f"Created {new_tag['category']} tag: {new_tag['name']}")
    ```

---

### **retrieve_tag()**

Get detailed information about a specific tag by its ID.

```python
def retrieve_tag(
    self, 
    tag_id: int
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tag_id` | `int` | Yes | Unique identifier of the tag to retrieve |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Complete tag data dictionary |

=== ":material-magnify: Basic Retrieval"

    ```python
    # Get a specific tag
    tag_data = client.tags.retrieve_tag(123)
    
    print(f"Tag: {tag_data['name']}")
    print(f"Description: {tag_data.get('description', 'Not provided')}")
    print(f"Category: {tag_data.get('category', 'Uncategorized')}")
    ```

=== ":material-information: Detailed Display"

    ```python
    # Display comprehensive tag information
    tag_data = client.tags.retrieve_tag(123)
    
    print("=== Tag Details ===")
    print(f"ID: {tag_data['id']}")
    print(f"Name: {tag_data.get('name', 'Not specified')}")
    print(f"Description: {tag_data.get('description', 'Not specified')}")
    print(f"Category: {tag_data.get('category', 'Uncategorized')}")
    print(f"Color: {tag_data.get('color', 'Default')}")
    print(f"Icon: {tag_data.get('icon', 'None')}")
    print(f"Sort Order: {tag_data.get('sort_order', 'Not set')}")
    ```

---

### **update_tag()**

Update an existing tag with new or modified data.

```python
def update_tag(
    self, 
    tag_id: int, 
    tag_data: Dict[str, Any]
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tag_id` | `int` | Yes | Unique identifier of the tag to update |
| `tag_data` | `Dict[str, Any]` | Yes | Dictionary containing fields to update |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Updated tag data |

=== ":material-pencil: Basic Updates"

    ```python
    # Update tag information
    updated_tag = client.tags.update_tag(123, {
        "description": "Updated tag description",
        "color": "#FF6B6B"
    })
    
    # Update tag category
    updated_tag = client.tags.update_tag(123, {
        "category": "Premium Features",
        "sort_order": 1
    })
    
    print(f"Updated tag {updated_tag['id']}")
    ```

---

### **delete_tag()**

Delete a tag from the system. Use with caution as this action may be irreversible.

```python
def delete_tag(
    self, 
    tag_id: int
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tag_id` | `int` | Yes | Unique identifier of the tag to delete |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Deletion confirmation response |

!!! warning "Permanent Action"
    ⚠️ Tag deletion may be permanent and will remove the tag from all associated resources. Consider deactivating instead of deleting when possible.

---

## 🏗️ Common Tag Workflows

### **Tag Organization System**

```python
def setup_property_tag_system():
    """Set up a comprehensive property tagging system."""
    
    tag_categories = [
        {
            "category": "Property Type",
            "tags": [
                {"name": "Single Family", "color": "#4ECDC4"},
                {"name": "Condo", "color": "#45B7D1"},
                {"name": "Townhouse", "color": "#FFA07A"},
                {"name": "Multi-Family", "color": "#98D8C8"}
            ]
        },
        {
            "category": "Price Range",
            "tags": [
                {"name": "Luxury", "color": "#FFD700", "icon": "diamond"},
                {"name": "Premium", "color": "#C0C0C0", "icon": "star"},
                {"name": "Standard", "color": "#87CEEB", "icon": "home"}
            ]
        },
        {
            "category": "Features",
            "tags": [
                {"name": "Pool", "color": "#00CED1", "icon": "pool"},
                {"name": "Garage", "color": "#8B4513", "icon": "garage"},
                {"name": "Garden", "color": "#32CD32", "icon": "leaf"}
            ]
        }
    ]
    
    created_tags = []
    for category_info in tag_categories:
        for i, tag_info in enumerate(category_info["tags"]):
            tag_data = {
                "name": tag_info["name"],
                "category": category_info["category"],
                "color": tag_info["color"],
                "sort_order": i + 1
            }
            if "icon" in tag_info:
                tag_data["icon"] = tag_info["icon"]
                
            new_tag = client.tags.create_tag(tag_data)
            created_tags.append(new_tag)
            print(f"Created {new_tag['category']} tag: {new_tag['name']}")
    
    return created_tags

# Usage
tag_system = setup_property_tag_system()
```

### **Tag Management Operations**

```python
class TagManager:
    """Helper class for managing tag operations."""
    
    def __init__(self, client):
        self.client = client
    
    def get_tags_by_category(self, category):
        """Get all tags in a specific category."""
        return self.client.tags.list_tags(params={
            "category": category
        })
    
    def search_tags(self, search_term):
        """Search tags by name or description."""
        return self.client.tags.list_tags(params={
            "search": search_term,
            "limit": 50
        })
    
    def get_tag_hierarchy(self):
        """Get tags organized by category."""
        all_tags = self.client.tags.list_tags()
        hierarchy = {}
        
        for tag in all_tags:
            category = tag.get("category", "Uncategorized")
            if category not in hierarchy:
                hierarchy[category] = []
            hierarchy[category].append(tag)
        
        # Sort tags within each category
        for category in hierarchy:
            hierarchy[category].sort(key=lambda x: x.get("sort_order", 999))
        
        return hierarchy
    
    def bulk_update_category(self, old_category, new_category):
        """Update category for all tags in a category."""
        tags = self.get_tags_by_category(old_category)
        updated_tags = []
        
        for tag in tags:
            try:
                updated_tag = self.client.tags.update_tag(tag["id"], {
                    "category": new_category
                })
                updated_tags.append(updated_tag)
            except Exception as e:
                print(f"Failed to update tag {tag['id']}: {e}")
        
        return updated_tags

# Usage
tag_manager = TagManager(client)
luxury_tags = tag_manager.get_tags_by_category("Luxury")
tag_hierarchy = tag_manager.get_tag_hierarchy()
```

---

## 🆘 Error Handling

All tag methods can raise these exceptions:

!!! warning "Common Exceptions"
    - **`AuthenticationError`**: Invalid or missing API key
    - **`ValidationError`**: Invalid tag data or parameters
    - **`NotFoundError`**: Tag not found (retrieve, update, delete)
    - **`OpenToCloseAPIError`**: General API error

```python
from open_to_close.exceptions import (
    NotFoundError, 
    ValidationError, 
    AuthenticationError
)

def robust_tag_operations(tag_id):
    """Example of comprehensive error handling."""
    try:
        # Attempt tag operations
        tag_data = client.tags.retrieve_tag(tag_id)
        
        updated_tag = client.tags.update_tag(tag_id, {
            "description": "Updated description"
        })
        
        return updated_tag
        
    except NotFoundError:
        print(f"Tag {tag_id} does not exist")
        return None
        
    except ValidationError as e:
        print(f"Invalid data provided: {e}")
        return None
        
    except AuthenticationError:
        print("Authentication failed - check your API key")
        return None
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

---

## 📚 Related Resources

**Related APIs:**
- **[Properties API](properties.md)** - Tag properties for organization
- **[Contacts API](contacts.md)** - Tag contacts and leads
- All other APIs support tagging for enhanced organization

---

*Tags provide powerful organization and filtering capabilities. Master these operations to build flexible classification systems.* 