# Teams API

The Teams API manages team organization and user group management within the Open To Close platform. Teams enable efficient collaboration, role assignment, and hierarchical organization of agents and users.

!!! abstract "TeamsAPI Client"
    Access via `client.teams` - provides full CRUD operations for team management.

---

## 🚀 Quick Start

```python
from open_to_close import OpenToCloseAPI

client = OpenToCloseAPI()

# List all teams
teams = client.teams.list_teams()

# Get a specific team
team_data = client.teams.retrieve_team(123)

# Create a new team
new_team = client.teams.create_team({
    "name": "Downtown Sales Team",
    "description": "Team focused on downtown properties",
    "team_lead_id": 5
})
```

---

## 📋 Available Methods

| Method | Description | HTTP Endpoint |
|--------|-------------|---------------|
| `list_teams()` | Get all teams with optional filtering | `GET /teams` |
| `create_team()` | Create a new team | `POST /teams` |
| `retrieve_team()` | Get a specific team by ID | `GET /teams/{id}` |
| `update_team()` | Update an existing team | `PUT /teams/{id}` |
| `delete_team()` | Delete a team by ID | `DELETE /teams/{id}` |

---

## 🔍 Method Documentation

### **list_teams()**

Retrieve a list of teams with optional filtering and pagination.

```python
def list_teams(
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
| `List[Dict[str, Any]]` | List of team dictionaries |

**Common Query Parameters:**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `limit` | `int` | Maximum number of results to return | `50` |
| `offset` | `int` | Number of results to skip for pagination | `100` |
| `status` | `string` | Filter by team status | `"Active"` |
| `team_lead_id` | `int` | Filter by team lead | `5` |
| `sort` | `string` | Sort field and direction | `"name"` |

=== ":material-list-box: Basic Listing"

    ```python
    # Get all teams
    teams = client.teams.list_teams()
    print(f"Found {len(teams)} teams")
    
    # Display basic info
    for team in teams:
        print(f"Team {team['id']}: {team.get('name', 'No name')}")
    ```

=== ":material-filter: Filtered Results"

    ```python
    # Get active teams only
    active_teams = client.teams.list_teams(params={
        "status": "Active",
        "limit": 25
    })
    
    # Get teams by lead
    teams_by_lead = client.teams.list_teams(params={
        "team_lead_id": 5,
        "sort": "name"
    })
    ```

---

### **create_team()**

Create a new team with the provided data.

```python
def create_team(
    self, 
    team_data: Dict[str, Any]
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `team_data` | `Dict[str, Any]` | Yes | Dictionary containing team information |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Created team data with assigned ID |

**Common Team Fields:**

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `name` | `string` | No | Team name | `"Sales Team A"` |
| `description` | `string` | No | Team description | `"Residential sales team"` |
| `team_lead_id` | `integer` | No | User ID of team lead | `5` |
| `status` | `string` | No | Team status | `"Active"` |
| `specialization` | `string` | No | Team specialization | `"Luxury Homes"` |
| `territory` | `string` | No | Geographic territory | `"Downtown District"` |

=== ":material-plus: Basic Creation"

    ```python
    # Create a basic team
    new_team = client.teams.create_team({
        "name": "West Side Team",
        "description": "Handles west side properties"
    })
    
    print(f"Created team with ID: {new_team['id']}")
    print(f"Name: {new_team['name']}")
    ```

=== ":material-account-supervisor: Complete Team"

    ```python
    # Create a comprehensive team
    team_data = {
        "name": "Luxury Properties Team",
        "description": "Specialized team for high-end residential properties",
        "team_lead_id": 10,
        "status": "Active",
        "specialization": "Luxury Residential",
        "territory": "Beverly Hills District",
        "commission_split": 0.7,
        "target_revenue": 5000000
    }
    
    new_team = client.teams.create_team(team_data)
    print(f"Created team {new_team['name']} led by agent {new_team['team_lead_id']}")
    ```

---

### **retrieve_team()**

Get detailed information about a specific team by its ID.

```python
def retrieve_team(
    self, 
    team_id: int
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `team_id` | `int` | Yes | Unique identifier of the team to retrieve |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Complete team data dictionary |

=== ":material-magnify: Basic Retrieval"

    ```python
    # Get a specific team
    team_data = client.teams.retrieve_team(123)
    
    print(f"Team: {team_data['name']}")
    print(f"Description: {team_data.get('description', 'Not provided')}")
    print(f"Status: {team_data.get('status', 'Unknown')}")
    ```

=== ":material-information: Detailed Display"

    ```python
    # Display comprehensive team information
    team_data = client.teams.retrieve_team(123)
    
    print("=== Team Profile ===")
    print(f"ID: {team_data['id']}")
    print(f"Name: {team_data.get('name', 'Not specified')}")
    print(f"Description: {team_data.get('description', 'Not specified')}")
    print(f"Team Lead ID: {team_data.get('team_lead_id', 'Not assigned')}")
    print(f"Status: {team_data.get('status', 'Unknown')}")
    print(f"Specialization: {team_data.get('specialization', 'General')}")
    print(f"Territory: {team_data.get('territory', 'Not specified')}")
    ```

---

### **update_team()**

Update an existing team with new or modified data.

```python
def update_team(
    self, 
    team_id: int, 
    team_data: Dict[str, Any]
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `team_id` | `int` | Yes | Unique identifier of the team to update |
| `team_data` | `Dict[str, Any]` | Yes | Dictionary containing fields to update |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Updated team data |

=== ":material-pencil: Basic Updates"

    ```python
    # Update team information
    updated_team = client.teams.update_team(123, {
        "description": "Updated team description",
        "status": "Active"
    })
    
    # Change team lead
    updated_team = client.teams.update_team(123, {
        "team_lead_id": 15
    })
    
    print(f"Updated team {updated_team['id']}")
    ```

=== ":material-account-edit: Team Restructuring"

    ```python
    # Update team structure and assignments
    def restructure_team(team_id, new_structure):
        return client.teams.update_team(team_id, {
            "team_lead_id": new_structure["lead_id"],
            "specialization": new_structure["specialization"],
            "territory": new_structure["territory"],
            "restructure_date": datetime.now().isoformat()
        })
    
    # Update team performance targets
    def update_team_targets(team_id, targets):
        return client.teams.update_team(team_id, {
            "target_revenue": targets["revenue"],
            "target_deals": targets["deals"],
            "target_period": targets["period"],
            "targets_updated": datetime.now().isoformat()
        })
    
    # Usage
    updated_team = restructure_team(123, {
        "lead_id": 20,
        "specialization": "Commercial Properties",
        "territory": "Financial District"
    })
    ```

---

### **delete_team()**

Delete a team from the system. Use with caution as this action may be irreversible.

```python
def delete_team(
    self, 
    team_id: int
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `team_id` | `int` | Yes | Unique identifier of the team to delete |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Deletion confirmation response |

!!! warning "Permanent Action"
    ⚠️ Team deletion may be permanent and could affect related records (agent assignments, performance data). Consider updating the status to "Inactive" instead of deleting when possible.

---

## 🏗️ Common Team Workflows

### **Team Formation Workflow**

```python
def create_specialized_team(team_info, lead_agent_id):
    """Create a new specialized team with proper setup."""
    
    # Step 1: Create the team
    team_data = {
        "name": team_info["name"],
        "description": team_info["description"],
        "team_lead_id": lead_agent_id,
        "specialization": team_info["specialization"],
        "territory": team_info.get("territory"),
        "status": "Active",
        "created_date": datetime.now().isoformat()
    }
    
    new_team = client.teams.create_team(team_data)
    team_id = new_team['id']
    
    print(f"Created team: {new_team['name']} (ID: {team_id})")
    return new_team

# Usage
new_team = create_specialized_team({
    "name": "Commercial Division",
    "description": "Dedicated commercial real estate team",
    "specialization": "Commercial Properties",
    "territory": "Business District"
}, lead_agent_id=25)
```

### **Team Management Operations**

```python
class TeamManager:
    """Helper class for managing team operations."""
    
    def __init__(self, client):
        self.client = client
    
    def get_active_teams(self):
        """Get all active teams."""
        return self.client.teams.list_teams(params={
            "status": "Active"
        })
    
    def get_team_by_lead(self, lead_id):
        """Get teams led by a specific agent."""
        return self.client.teams.list_teams(params={
            "team_lead_id": lead_id
        })
    
    def get_team_summary(self, team_id):
        """Get comprehensive team information."""
        try:
            team = self.client.teams.retrieve_team(team_id)
            
            summary = {
                "basic_info": {
                    "name": team.get("name"),
                    "description": team.get("description"),
                    "status": team.get("status")
                },
                "organization": {
                    "lead_id": team.get("team_lead_id"),
                    "specialization": team.get("specialization"),
                    "territory": team.get("territory")
                },
                "performance": {
                    "target_revenue": team.get("target_revenue"),
                    "commission_split": team.get("commission_split")
                }
            }
            
            return summary
            
        except Exception as e:
            print(f"Error getting team summary: {e}")
            return None
    
    def reassign_team_lead(self, team_id, new_lead_id, reason=None):
        """Reassign team leadership."""
        update_data = {
            "team_lead_id": new_lead_id,
            "lead_change_date": datetime.now().isoformat()
        }
        if reason:
            update_data["lead_change_reason"] = reason
            
        return self.client.teams.update_team(team_id, update_data)

# Usage
team_manager = TeamManager(client)
active_teams = team_manager.get_active_teams()
team_summary = team_manager.get_team_summary(123)
```

---

## 🆘 Error Handling

All team methods can raise these exceptions:

!!! warning "Common Exceptions"
    - **`AuthenticationError`**: Invalid or missing API key
    - **`ValidationError`**: Invalid team data or parameters
    - **`NotFoundError`**: Team not found (retrieve, update, delete)
    - **`OpenToCloseAPIError`**: General API error

```python
from open_to_close.exceptions import (
    NotFoundError, 
    ValidationError, 
    AuthenticationError
)

def robust_team_operations(team_id):
    """Example of comprehensive error handling."""
    try:
        # Attempt team operations
        team_data = client.teams.retrieve_team(team_id)
        
        updated_team = client.teams.update_team(team_id, {
            "status": "Active"
        })
        
        return updated_team
        
    except NotFoundError:
        print(f"Team {team_id} does not exist")
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
- **[Agents API](agents.md)** - Manage team members and assignments
- **[Users API](users.md)** - User management and roles
- **[Properties API](properties.md)** - Team property assignments

---

*Teams enable efficient organization and collaboration. Master these operations to build effective team management systems.* 