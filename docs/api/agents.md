# Agents API

The Agents API provides comprehensive management for real estate agents within the Open To Close platform. This includes agent profiles, contact information, assignments, and team management.

!!! abstract "AgentsAPI Client"
    Access via `client.agents` - provides full CRUD operations for agent management.

---

## 🚀 Quick Start

```python
from open_to_close import OpenToCloseAPI

client = OpenToCloseAPI()

# List all agents
agents = client.agents.list_agents()

# Get a specific agent
agent_data = client.agents.retrieve_agent(123)

# Create a new agent
new_agent = client.agents.create_agent({
    "name": "John Smith",
    "email": "john.smith@realty.com",
    "phone": "+1234567890",
    "license_number": "RE123456"
})
```

---

## 📋 Available Methods

| Method | Description | HTTP Endpoint |
|--------|-------------|---------------|
| `list_agents()` | Get all agents with optional filtering | `GET /agents` |
| `create_agent()` | Create a new agent | `POST /agents` |
| `retrieve_agent()` | Get a specific agent by ID | `GET /agents/{id}` |
| `update_agent()` | Update an existing agent | `PUT /agents/{id}` |
| `delete_agent()` | Delete an agent by ID | `DELETE /agents/{id}` |

---

## 🔍 Method Documentation

### **list_agents()**

Retrieve a list of agents with optional filtering and pagination.

```python
def list_agents(
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
| `List[Dict[str, Any]]` | List of agent dictionaries |

**Common Query Parameters:**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `limit` | `int` | Maximum number of results to return | `50` |
| `offset` | `int` | Number of results to skip for pagination | `100` |
| `status` | `string` | Filter by agent status | `"Active"` |
| `team_id` | `int` | Filter by team assignment | `5` |
| `sort` | `string` | Sort field and direction | `"name"` |

=== ":material-list-box: Basic Listing"

    ```python
    # Get all agents
    agents = client.agents.list_agents()
    print(f"Found {len(agents)} agents")
    
    # Display basic info
    for agent in agents:
        print(f"Agent {agent['id']}: {agent.get('name', 'No name')}")
    ```

=== ":material-filter: Filtered Results"

    ```python
    # Get active agents only
    active_agents = client.agents.list_agents(params={
        "status": "Active",
        "limit": 25
    })
    
    # Get agents by team
    team_agents = client.agents.list_agents(params={
        "team_id": 5,
        "sort": "name"
    })
    ```

=== ":material-page-next: Pagination"

    ```python
    # Paginate through all agents
    all_agents = []
    offset = 0
    limit = 100
    
    while True:
        batch = client.agents.list_agents(params={
            "limit": limit,
            "offset": offset
        })
        
        if not batch:
            break
            
        all_agents.extend(batch)
        offset += limit
    
    print(f"Total agents: {len(all_agents)}")
    ```

---

### **create_agent()**

Create a new agent with the provided data.

```python
def create_agent(
    self, 
    agent_data: Dict[str, Any]
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_data` | `Dict[str, Any]` | Yes | Dictionary containing agent information |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Created agent data with assigned ID |

**Common Agent Fields:**

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `name` | `string` | No | Agent's full name | `"John Smith"` |
| `email` | `string` | No | Email address | `"john@realty.com"` |
| `phone` | `string` | No | Phone number | `"+1234567890"` |
| `license_number` | `string` | No | Real estate license number | `"RE123456"` |
| `team_id` | `integer` | No | Team assignment | `5` |
| `status` | `string` | No | Agent status | `"Active"` |
| `hire_date` | `string` | No | Date of hire (ISO format) | `"2024-01-15"` |
| `commission_rate` | `number` | No | Commission rate (decimal) | `0.06` |

=== ":material-plus: Basic Creation"

    ```python
    # Create a basic agent profile
    new_agent = client.agents.create_agent({
        "name": "Sarah Johnson",
        "email": "sarah.johnson@realty.com",
        "phone": "+1555123456"
    })
    
    print(f"Created agent with ID: {new_agent['id']}")
    print(f"Name: {new_agent['name']}")
    ```

=== ":material-account-tie: Complete Profile"

    ```python
    # Create a comprehensive agent profile
    agent_data = {
        "name": "Michael Davis",
        "email": "michael.davis@realty.com",
        "phone": "+1555987654",
        "license_number": "RE987654",
        "team_id": 3,
        "status": "Active",
        "hire_date": "2024-01-15",
        "commission_rate": 0.06,
        "specialties": ["Residential", "Luxury Homes"],
        "bio": "Experienced agent specializing in luxury residential properties"
    }
    
    new_agent = client.agents.create_agent(agent_data)
    print(f"Created agent {new_agent['name']} with license {new_agent['license_number']}")
    ```

=== ":material-account-supervisor: Team Assignment"

    ```python
    # Create agent with team assignment
    team_agent = client.agents.create_agent({
        "name": "Jennifer Wilson",
        "email": "jennifer@realty.com",
        "phone": "+1555456789",
        "team_id": 2,
        "role": "Senior Agent",
        "mentor_id": 15  # Assigned to existing agent as mentor
    })
    ```

---

### **retrieve_agent()**

Get detailed information about a specific agent by their ID.

```python
def retrieve_agent(
    self, 
    agent_id: int
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `int` | Yes | Unique identifier of the agent to retrieve |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Complete agent data dictionary |

=== ":material-magnify: Basic Retrieval"

    ```python
    # Get a specific agent
    agent_data = client.agents.retrieve_agent(123)
    
    print(f"Agent: {agent_data['name']}")
    print(f"Email: {agent_data.get('email', 'Not provided')}")
    print(f"Status: {agent_data.get('status', 'Unknown')}")
    ```

=== ":material-information: Detailed Display"

    ```python
    # Display comprehensive agent information
    agent_data = client.agents.retrieve_agent(123)
    
    print("=== Agent Profile ===")
    print(f"ID: {agent_data['id']}")
    print(f"Name: {agent_data.get('name', 'Not specified')}")
    print(f"Email: {agent_data.get('email', 'Not specified')}")
    print(f"Phone: {agent_data.get('phone', 'Not specified')}")
    print(f"License: {agent_data.get('license_number', 'Not specified')}")
    print(f"Team: {agent_data.get('team_id', 'Unassigned')}")
    print(f"Status: {agent_data.get('status', 'Unknown')}")
    
    if agent_data.get('commission_rate'):
        print(f"Commission Rate: {agent_data['commission_rate']*100}%")
    ```

=== ":material-shield-check: Error Handling"

    ```python
    from open_to_close.exceptions import NotFoundError
    
    def safe_get_agent(agent_id):
        try:
            agent_data = client.agents.retrieve_agent(agent_id)
            return agent_data
        except NotFoundError:
            print(f"Agent {agent_id} not found")
            return None
        except Exception as e:
            print(f"Error retrieving agent {agent_id}: {e}")
            return None
    
    # Usage
    agent_data = safe_get_agent(123)
    if agent_data:
        print(f"Found agent: {agent_data['name']}")
    ```

---

### **update_agent()**

Update an existing agent with new or modified data.

```python
def update_agent(
    self, 
    agent_id: int, 
    agent_data: Dict[str, Any]
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `int` | Yes | Unique identifier of the agent to update |
| `agent_data` | `Dict[str, Any]` | Yes | Dictionary containing fields to update |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Updated agent data |

=== ":material-pencil: Basic Updates"

    ```python
    # Update agent contact information
    updated_agent = client.agents.update_agent(123, {
        "email": "new.email@realty.com",
        "phone": "+1555999888"
    })
    
    # Update agent status
    updated_agent = client.agents.update_agent(123, {
        "status": "On Leave"
    })
    
    print(f"Updated agent {updated_agent['id']}")
    ```

=== ":material-account-edit: Profile Changes"

    ```python
    # Update agent profile and assignments
    def update_agent_profile(agent_id, profile_updates):
        return client.agents.update_agent(agent_id, {
            **profile_updates,
            "last_updated": datetime.now().isoformat()
        })
    
    # Update team assignment
    def reassign_agent_team(agent_id, new_team_id):
        return client.agents.update_agent(agent_id, {
            "team_id": new_team_id,
            "reassignment_date": datetime.now().isoformat()
        })
    
    # Usage
    updated_agent = update_agent_profile(123, {
        "commission_rate": 0.07,
        "specialties": ["Commercial", "Investment Properties"]
    })
    ```

=== ":material-update: Status Management"

    ```python
    # Agent status management functions
    def activate_agent(agent_id):
        return client.agents.update_agent(agent_id, {
            "status": "Active",
            "activation_date": datetime.now().isoformat()
        })
    
    def deactivate_agent(agent_id, reason=None):
        update_data = {
            "status": "Inactive",
            "deactivation_date": datetime.now().isoformat()
        }
        if reason:
            update_data["deactivation_reason"] = reason
        
        return client.agents.update_agent(agent_id, update_data)
    
    # Usage
    activated_agent = activate_agent(123)
    deactivated_agent = deactivate_agent(124, "Left company")
    ```

---

### **delete_agent()**

Delete an agent from the system. Use with caution as this action may be irreversible.

```python
def delete_agent(
    self, 
    agent_id: int
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `int` | Yes | Unique identifier of the agent to delete |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Deletion confirmation response |

!!! warning "Permanent Action"
    ⚠️ Agent deletion may be permanent and could affect related records (properties, contacts, transactions). Consider updating the status to "Inactive" instead of deleting when possible.

=== ":material-delete: Basic Deletion"

    ```python
    # Delete an agent
    result = client.agents.delete_agent(123)
    print("Agent deleted successfully")
    ```

=== ":material-shield-alert: Safe Deletion"

    ```python
    def safe_delete_agent(agent_id, confirm=False):
        """Safely delete an agent with confirmation."""
        if not confirm:
            print("This will permanently delete the agent.")
            print("Call with confirm=True to proceed.")
            return None
            
        try:
            # Check if agent has active assignments
            agent_data = client.agents.retrieve_agent(agent_id)
            if agent_data.get('status') == 'Active':
                print("Warning: Agent is currently active")
                print("Consider deactivating instead of deleting")
                
            result = client.agents.delete_agent(agent_id)
            print(f"Agent {agent_id} deleted successfully")
            return result
            
        except Exception as e:
            print(f"Error deleting agent {agent_id}: {e}")
            return None
    
    # Usage
    safe_delete_agent(123, confirm=True)
    ```

=== ":material-archive: Alternative: Deactivate"

    ```python
    # Instead of deleting, deactivate the agent
    def archive_agent(agent_id, reason=None):
        """Archive an agent instead of deleting them."""
        update_data = {
            "status": "Archived",
            "archived_date": datetime.now().isoformat(),
            "active": False
        }
        if reason:
            update_data["archive_reason"] = reason
            
        return client.agents.update_agent(agent_id, update_data)
    
    # Usage
    archived_agent = archive_agent(123, "Agent retired")
    print(f"Agent {archived_agent['id']} archived")
    ```

---

## 🏗️ Common Agent Workflows

### **Agent Onboarding Workflow**

```python
from datetime import datetime

def onboard_new_agent(agent_info, team_id=None):
    """Complete workflow for onboarding a new agent."""
    
    # Step 1: Create the agent profile
    agent_data = {
        "name": agent_info["name"],
        "email": agent_info["email"],
        "phone": agent_info["phone"],
        "license_number": agent_info.get("license_number"),
        "hire_date": datetime.now().strftime("%Y-%m-%d"),
        "status": "Active"
    }
    
    if team_id:
        agent_data["team_id"] = team_id
    
    new_agent = client.agents.create_agent(agent_data)
    agent_id = new_agent['id']
    
    # Step 2: Set up initial assignments (if applicable)
    if agent_info.get("mentor_id"):
        client.agents.update_agent(agent_id, {
            "mentor_id": agent_info["mentor_id"]
        })
    
    print(f"Successfully onboarded agent {new_agent['name']} (ID: {agent_id})")
    return new_agent

# Usage
new_agent = onboard_new_agent({
    "name": "Alex Thompson",
    "email": "alex.thompson@realty.com",
    "phone": "+1555147258",
    "license_number": "RE147258"
}, team_id=3)
```

### **Agent Performance Tracking**

```python
class AgentManager:
    """Helper class for managing agent operations."""
    
    def __init__(self, client):
        self.client = client
    
    def get_team_agents(self, team_id):
        """Get all agents in a specific team."""
        return self.client.agents.list_agents(params={
            "team_id": team_id,
            "status": "Active"
        })
    
    def update_commission_rates(self, agent_updates):
        """Bulk update commission rates for multiple agents."""
        results = []
        for agent_id, new_rate in agent_updates.items():
            try:
                updated_agent = self.client.agents.update_agent(agent_id, {
                    "commission_rate": new_rate,
                    "rate_update_date": datetime.now().isoformat()
                })
                results.append(updated_agent)
            except Exception as e:
                print(f"Failed to update agent {agent_id}: {e}")
        
        return results
    
    def get_agent_summary(self, agent_id):
        """Get comprehensive agent information."""
        try:
            agent = self.client.agents.retrieve_agent(agent_id)
            
            summary = {
                "basic_info": {
                    "name": agent.get("name"),
                    "email": agent.get("email"),
                    "status": agent.get("status")
                },
                "professional_info": {
                    "license": agent.get("license_number"),
                    "team_id": agent.get("team_id"),
                    "hire_date": agent.get("hire_date")
                },
                "performance": {
                    "commission_rate": agent.get("commission_rate"),
                    "specialties": agent.get("specialties", [])
                }
            }
            
            return summary
            
        except Exception as e:
            print(f"Error getting agent summary: {e}")
            return None

# Usage
agent_manager = AgentManager(client)
team_agents = agent_manager.get_team_agents(5)
agent_summary = agent_manager.get_agent_summary(123)
```

---

## 🆘 Error Handling

All agent methods can raise these exceptions:

!!! warning "Common Exceptions"
    - **`AuthenticationError`**: Invalid or missing API key
    - **`ValidationError`**: Invalid agent data or parameters
    - **`NotFoundError`**: Agent not found (retrieve, update, delete)
    - **`OpenToCloseAPIError`**: General API error

```python
from open_to_close.exceptions import (
    NotFoundError, 
    ValidationError, 
    AuthenticationError
)

def robust_agent_operations(agent_id):
    """Example of comprehensive error handling."""
    try:
        # Attempt agent operations
        agent_data = client.agents.retrieve_agent(agent_id)
        
        updated_agent = client.agents.update_agent(agent_id, {
            "status": "Active"
        })
        
        return updated_agent
        
    except NotFoundError:
        print(f"Agent {agent_id} does not exist")
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
- **[Teams API](teams.md)** - Team management and assignments
- **[Users API](users.md)** - User account management
- **[Properties API](properties.md)** - Property assignments and management
- **[Contacts API](contacts.md)** - Client and lead management

---

*Agents are key users in the Open To Close platform. Master these operations to build comprehensive agent management systems.* 