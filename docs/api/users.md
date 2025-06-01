# Users API

The Users API manages user accounts and system access within the Open To Close platform. This includes user authentication, roles, permissions, and account management for all platform users.

!!! abstract "UsersAPI Client"
    Access via `client.users` - provides full CRUD operations for user management.

---

## 🚀 Quick Start

```python
from open_to_close import OpenToCloseAPI

client = OpenToCloseAPI()

# List all users
users = client.users.list_users()

# Get a specific user
user_data = client.users.retrieve_user(123)

# Create a new user
new_user = client.users.create_user({
    "username": "johndoe",
    "email": "john.doe@company.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "Agent"
})
```

---

## 📋 Available Methods

| Method | Description | HTTP Endpoint |
|--------|-------------|---------------|
| `list_users()` | Get all users with optional filtering | `GET /users` |
| `create_user()` | Create a new user | `POST /users` |
| `retrieve_user()` | Get a specific user by ID | `GET /users/{id}` |
| `update_user()` | Update an existing user | `PUT /users/{id}` |
| `delete_user()` | Delete a user by ID | `DELETE /users/{id}` |

---

## 🔍 Method Documentation

### **list_users()**

Retrieve a list of users with optional filtering and pagination.

```python
def list_users(
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
| `List[Dict[str, Any]]` | List of user dictionaries |

**Common Query Parameters:**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `limit` | `int` | Maximum number of results to return | `50` |
| `offset` | `int` | Number of results to skip for pagination | `100` |
| `role` | `string` | Filter by user role | `"Agent"` |
| `status` | `string` | Filter by user status | `"Active"` |
| `sort` | `string` | Sort field and direction | `"last_name"` |

=== ":material-list-box: Basic Listing"

    ```python
    # Get all users
    users = client.users.list_users()
    print(f"Found {len(users)} users")
    
    # Display basic info
    for user in users:
        name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
        print(f"User {user['id']}: {name} ({user.get('role', 'No role')})")
    ```

=== ":material-filter: Filtered Results"

    ```python
    # Get agents only
    agents = client.users.list_users(params={
        "role": "Agent",
        "status": "Active",
        "limit": 25
    })
    
    # Get administrators
    admins = client.users.list_users(params={
        "role": "Administrator",
        "sort": "last_name"
    })
    ```

---

### **create_user()**

Create a new user with the provided data.

```python
def create_user(
    self, 
    user_data: Dict[str, Any]
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `user_data` | `Dict[str, Any]` | Yes | Dictionary containing user information |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Created user data with assigned ID |

**Common User Fields:**

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `username` | `string` | No | Unique username | `"johndoe"` |
| `email` | `string` | No | Email address | `"john@company.com"` |
| `first_name` | `string` | No | First name | `"John"` |
| `last_name` | `string` | No | Last name | `"Doe"` |
| `role` | `string` | No | User role | `"Agent"` |
| `status` | `string` | No | User status | `"Active"` |
| `phone` | `string` | No | Phone number | `"+1234567890"` |
| `department` | `string` | No | Department | `"Sales"` |

=== ":material-plus: Basic Creation"

    ```python
    # Create a basic user
    new_user = client.users.create_user({
        "username": "jsmith",
        "email": "jane.smith@company.com",
        "first_name": "Jane",
        "last_name": "Smith",
        "role": "Agent"
    })
    
    print(f"Created user with ID: {new_user['id']}")
    print(f"Username: {new_user['username']}")
    ```

=== ":material-account: Complete Profile"

    ```python
    # Create a comprehensive user profile
    user_data = {
        "username": "mwilson",
        "email": "michael.wilson@company.com",
        "first_name": "Michael",
        "last_name": "Wilson",
        "role": "Team Lead",
        "status": "Active",
        "phone": "+1555987654",
        "department": "Luxury Sales",
        "hire_date": "2024-01-15",
        "permissions": ["read", "write", "manage_team"]
    }
    
    new_user = client.users.create_user(user_data)
    print(f"Created {new_user['role']}: {new_user['first_name']} {new_user['last_name']}")
    ```

=== ":material-security: Administrator Account"

    ```python
    # Create an administrator account
    admin_user = client.users.create_user({
        "username": "admin_sarah",
        "email": "sarah.admin@company.com",
        "first_name": "Sarah",
        "last_name": "Administrator",
        "role": "Administrator",
        "status": "Active",
        "permissions": ["full_access", "user_management", "system_config"]
    })
    ```

---

### **retrieve_user()**

Get detailed information about a specific user by their ID.

```python
def retrieve_user(
    self, 
    user_id: int
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `user_id` | `int` | Yes | Unique identifier of the user to retrieve |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Complete user data dictionary |

=== ":material-magnify: Basic Retrieval"

    ```python
    # Get a specific user
    user_data = client.users.retrieve_user(123)
    
    name = f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}".strip()
    print(f"User: {name}")
    print(f"Email: {user_data.get('email', 'Not provided')}")
    print(f"Role: {user_data.get('role', 'Unknown')}")
    ```

=== ":material-information: Detailed Display"

    ```python
    # Display comprehensive user information
    user_data = client.users.retrieve_user(123)
    
    print("=== User Profile ===")
    print(f"ID: {user_data['id']}")
    print(f"Username: {user_data.get('username', 'Not specified')}")
    print(f"Name: {user_data.get('first_name', '')} {user_data.get('last_name', '')}")
    print(f"Email: {user_data.get('email', 'Not specified')}")
    print(f"Phone: {user_data.get('phone', 'Not specified')}")
    print(f"Role: {user_data.get('role', 'Not specified')}")
    print(f"Status: {user_data.get('status', 'Unknown')}")
    print(f"Department: {user_data.get('department', 'Not specified')}")
    ```

---

### **update_user()**

Update an existing user with new or modified data.

```python
def update_user(
    self, 
    user_id: int, 
    user_data: Dict[str, Any]
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `user_id` | `int` | Yes | Unique identifier of the user to update |
| `user_data` | `Dict[str, Any]` | Yes | Dictionary containing fields to update |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Updated user data |

=== ":material-pencil: Basic Updates"

    ```python
    # Update user contact information
    updated_user = client.users.update_user(123, {
        "email": "new.email@company.com",
        "phone": "+1555999888"
    })
    
    # Update user role
    updated_user = client.users.update_user(123, {
        "role": "Senior Agent",
        "department": "Luxury Sales"
    })
    
    print(f"Updated user {updated_user['id']}")
    ```

=== ":material-account-edit: Role Management"

    ```python
    # Update user role and permissions
    def promote_user(user_id, new_role, permissions):
        return client.users.update_user(user_id, {
            "role": new_role,
            "permissions": permissions,
            "promotion_date": datetime.now().isoformat()
        })
    
    # Update user status
    def change_user_status(user_id, new_status, reason=None):
        update_data = {
            "status": new_status,
            "status_change_date": datetime.now().isoformat()
        }
        if reason:
            update_data["status_change_reason"] = reason
            
        return client.users.update_user(user_id, update_data)
    
    # Usage
    promoted_user = promote_user(123, "Team Lead", ["read", "write", "manage_team"])
    ```

---

### **delete_user()**

Delete a user from the system. Use with caution as this action may be irreversible.

```python
def delete_user(
    self, 
    user_id: int
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `user_id` | `int` | Yes | Unique identifier of the user to delete |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Deletion confirmation response |

!!! warning "Permanent Action"
    ⚠️ User deletion may be permanent and could affect related records (assignments, communications, transactions). Consider updating the status to "Inactive" instead of deleting when possible.

---

## 🏗️ Common User Workflows

### **User Onboarding Workflow**

```python
def onboard_new_user(user_info, role="Agent"):
    """Complete workflow for onboarding a new user."""
    
    # Step 1: Create the user account
    user_data = {
        "username": user_info["username"],
        "email": user_info["email"],
        "first_name": user_info["first_name"],
        "last_name": user_info["last_name"],
        "role": role,
        "status": "Active",
        "phone": user_info.get("phone"),
        "department": user_info.get("department"),
        "hire_date": datetime.now().strftime("%Y-%m-%d")
    }
    
    new_user = client.users.create_user(user_data)
    user_id = new_user['id']
    
    print(f"Created user: {new_user['first_name']} {new_user['last_name']} (ID: {user_id})")
    return new_user

# Usage
new_user = onboard_new_user({
    "username": "asmith",
    "email": "alex.smith@company.com",
    "first_name": "Alex",
    "last_name": "Smith",
    "phone": "+1555147258",
    "department": "Residential Sales"
})
```

### **User Management Operations**

```python
class UserManager:
    """Helper class for managing user operations."""
    
    def __init__(self, client):
        self.client = client
    
    def get_users_by_role(self, role):
        """Get all users with a specific role."""
        return self.client.users.list_users(params={
            "role": role,
            "status": "Active"
        })
    
    def get_active_users(self):
        """Get all active users."""
        return self.client.users.list_users(params={
            "status": "Active"
        })
    
    def get_user_summary(self, user_id):
        """Get comprehensive user information."""
        try:
            user = self.client.users.retrieve_user(user_id)
            
            summary = {
                "basic_info": {
                    "name": f"{user.get('first_name', '')} {user.get('last_name', '')}".strip(),
                    "username": user.get("username"),
                    "email": user.get("email"),
                    "phone": user.get("phone")
                },
                "role_info": {
                    "role": user.get("role"),
                    "department": user.get("department"),
                    "status": user.get("status")
                },
                "dates": {
                    "hire_date": user.get("hire_date"),
                    "last_login": user.get("last_login")
                }
            }
            
            return summary
            
        except Exception as e:
            print(f"Error getting user summary: {e}")
            return None
    
    def deactivate_user(self, user_id, reason=None):
        """Deactivate a user account."""
        update_data = {
            "status": "Inactive",
            "deactivation_date": datetime.now().isoformat()
        }
        if reason:
            update_data["deactivation_reason"] = reason
            
        return self.client.users.update_user(user_id, update_data)

# Usage
user_manager = UserManager(client)
agents = user_manager.get_users_by_role("Agent")
user_summary = user_manager.get_user_summary(123)
```

---

## 🆘 Error Handling

All user methods can raise these exceptions:

!!! warning "Common Exceptions"
    - **`AuthenticationError`**: Invalid or missing API key
    - **`ValidationError`**: Invalid user data or parameters
    - **`NotFoundError`**: User not found (retrieve, update, delete)
    - **`OpenToCloseAPIError`**: General API error

```python
from open_to_close.exceptions import (
    NotFoundError, 
    ValidationError, 
    AuthenticationError
)

def robust_user_operations(user_id):
    """Example of comprehensive error handling."""
    try:
        # Attempt user operations
        user_data = client.users.retrieve_user(user_id)
        
        updated_user = client.users.update_user(user_id, {
            "status": "Active"
        })
        
        return updated_user
        
    except NotFoundError:
        print(f"User {user_id} does not exist")
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
- **[Agents API](agents.md)** - Agent-specific user management
- **[Teams API](teams.md)** - Team assignments and management
- **[Properties API](properties.md)** - User property assignments

---

*Users are the foundation of platform access and security. Master these operations to build comprehensive user management systems.* 