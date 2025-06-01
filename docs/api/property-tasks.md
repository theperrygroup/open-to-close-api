# Property Tasks API

The Property Tasks API allows you to manage tasks and action items associated with specific properties in the Open To Close platform. This includes creating, retrieving, updating, and deleting tasks that help track workflow and ensure important activities are completed throughout the property lifecycle.

## Overview

Property tasks help organize and track work that needs to be completed for specific properties. Common use cases include:

- Scheduling property inspections and appraisals
- Managing document collection and review
- Tracking maintenance and repair work
- Coordinating showings and open houses
- Following up on client communications
- Managing closing process activities

## Client Access

Access the Property Tasks API through the main client:

```python
from open_to_close import OpenToCloseAPI

client = OpenToCloseAPI()
tasks_api = client.property_tasks
```

---

## Methods

### `list_property_tasks(property_id, params=None)`

Retrieve a list of tasks for a specific property.

**Parameters:**

- `property_id` (int): The ID of the property
- `params` (dict, optional): Query parameters for filtering

**Returns:** List of property task dictionaries

**Raises:**

- `OpenToCloseAPIError`: If the API request fails
- `NotFoundError`: If the property is not found
- `ValidationError`: If parameters are invalid
- `AuthenticationError`: If authentication fails

=== "Basic Usage"

    ```python
    # Get all tasks for a property
    tasks = client.property_tasks.list_property_tasks(123)
    
    for task in tasks:
        print(f"Task: {task['title']} - {task['status']} (Due: {task['due_date']})")
    ```

=== "With Filtering"

    ```python
    # Get tasks with filtering
    pending_tasks = client.property_tasks.list_property_tasks(
        123, 
        params={"status": "pending"}
    )
    
    # Filter by assignee and priority
    urgent_tasks = client.property_tasks.list_property_tasks(
        123,
        params={
            "assignee": "John Agent",
            "priority": "high"
        }
    )
    ```

=== "Response Example"

    ```python
    [
        {
            "id": 201,
            "property_id": 123,
            "title": "Schedule inspection",
            "description": "Arrange property inspection with certified inspector.",
            "status": "pending",
            "priority": "high",
            "assignee": "John Agent",
            "due_date": "2024-01-20",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "completed_at": null,
            "tags": ["inspection", "urgent"]
        },
        {
            "id": 202,
            "property_id": 123,
            "title": "Upload listing photos",
            "description": "Take and upload high-quality photos for property listing.",
            "status": "completed",
            "priority": "medium",
            "assignee": "Jane Photographer",
            "due_date": "2024-01-18",
            "created_at": "2024-01-14T14:20:00Z",
            "updated_at": "2024-01-17T16:45:00Z",
            "completed_at": "2024-01-17T16:45:00Z",
            "tags": ["photos", "marketing"]
        }
    ]
    ```

---

### `create_property_task(property_id, task_data)`

Add a task to a specific property.

**Parameters:**

- `property_id` (int): The ID of the property
- `task_data` (dict): Task information

**Returns:** Dictionary representing the newly created property task

**Raises:**

- `OpenToCloseAPIError`: If the API request fails
- `ValidationError`: If task data is invalid
- `NotFoundError`: If the property is not found
- `AuthenticationError`: If authentication fails

=== "Basic Usage"

    ```python
    task = client.property_tasks.create_property_task(123, {
        "title": "Schedule inspection",
        "description": "Arrange property inspection with buyer.",
        "due_date": "2024-01-15"
    })
    
    print(f"Created task {task['id']}: {task['title']}")
    ```

=== "With Full Details"

    ```python
    task = client.property_tasks.create_property_task(123, {
        "title": "Prepare closing documents",
        "description": "Gather and prepare all necessary documents for property closing including deed, title insurance, and settlement statement.",
        "assignee": "Legal Team",
        "priority": "high",
        "due_date": "2024-01-25",
        "tags": ["closing", "documents", "legal"],
        "category": "closing"
    })
    ```

=== "Response Example"

    ```python
    {
        "id": 203,
        "property_id": 123,
        "title": "Schedule inspection",
        "description": "Arrange property inspection with buyer.",
        "status": "pending",
        "priority": "medium",
        "assignee": null,
        "due_date": "2024-01-15",
        "created_at": "2024-01-17T09:15:00Z",
        "updated_at": "2024-01-17T09:15:00Z",
        "completed_at": null,
        "tags": [],
        "category": "general"
    }
    ```

---

### `retrieve_property_task(property_id, task_id)`

Retrieve a specific task for a specific property.

**Parameters:**

- `property_id` (int): The ID of the property
- `task_id` (int): The ID of the task to retrieve

**Returns:** Dictionary representing the property task

**Raises:**

- `NotFoundError`: If the property or task is not found
- `OpenToCloseAPIError`: If the API request fails
- `AuthenticationError`: If authentication fails

=== "Basic Usage"

    ```python
    task = client.property_tasks.retrieve_property_task(123, 201)
    print(f"Task title: {task['title']}")
    print(f"Task status: {task['status']}")
    print(f"Due date: {task['due_date']}")
    ```

=== "Error Handling"

    ```python
    from open_to_close.exceptions import NotFoundError
    
    try:
        task = client.property_tasks.retrieve_property_task(123, 999)
    except NotFoundError:
        print("Task not found")
    ```

=== "Response Example"

    ```python
    {
        "id": 201,
        "property_id": 123,
        "title": "Schedule inspection",
        "description": "Arrange property inspection with certified inspector. Contact preferred inspector and coordinate with buyer's schedule.",
        "status": "pending",
        "priority": "high",
        "assignee": "John Agent",
        "due_date": "2024-01-20",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z",
        "completed_at": null,
        "tags": ["inspection", "urgent"],
        "category": "inspection",
        "notes": "Buyer prefers morning appointments",
        "estimated_hours": 2
    }
    ```

---

### `update_property_task(property_id, task_id, task_data)`

Update a specific task for a specific property.

**Parameters:**

- `property_id` (int): The ID of the property
- `task_id` (int): The ID of the task to update
- `task_data` (dict): Fields to update

**Returns:** Dictionary representing the updated property task

**Raises:**

- `NotFoundError`: If the property or task is not found
- `ValidationError`: If task data is invalid
- `OpenToCloseAPIError`: If the API request fails
- `AuthenticationError`: If authentication fails

=== "Basic Usage"

    ```python
    updated_task = client.property_tasks.update_property_task(
        123, 201, 
        {"status": "completed"}
    )
    ```

=== "Multiple Fields"

    ```python
    updated_task = client.property_tasks.update_property_task(
        123, 201, 
        {
            "status": "in_progress",
            "assignee": "Jane Agent",
            "priority": "urgent",
            "notes": "Inspector confirmed for tomorrow at 10 AM"
        }
    )
    ```

=== "Mark as Complete"

    ```python
    from datetime import datetime
    
    completed_task = client.property_tasks.update_property_task(
        123, 201, 
        {
            "status": "completed",
            "completed_at": datetime.now().isoformat(),
            "notes": "Inspection completed successfully. Report available."
        }
    )
    ```

=== "Response Example"

    ```python
    {
        "id": 201,
        "property_id": 123,
        "title": "Schedule inspection",
        "description": "Arrange property inspection with certified inspector.",
        "status": "completed",
        "priority": "high",
        "assignee": "John Agent",
        "due_date": "2024-01-20",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-17T11:45:00Z",
        "completed_at": "2024-01-17T11:45:00Z",
        "tags": ["inspection", "urgent"],
        "category": "inspection"
    }
    ```

---

### `delete_property_task(property_id, task_id)`

Remove a task from a specific property.

**Parameters:**

- `property_id` (int): The ID of the property
- `task_id` (int): The ID of the task to remove

**Returns:** Dictionary containing the API response

**Raises:**

- `NotFoundError`: If the property or task is not found
- `OpenToCloseAPIError`: If the API request fails
- `AuthenticationError`: If authentication fails

=== "Basic Usage"

    ```python
    result = client.property_tasks.delete_property_task(123, 201)
    print("Task deleted successfully")
    ```

=== "With Error Handling"

    ```python
    from open_to_close.exceptions import NotFoundError
    
    try:
        result = client.property_tasks.delete_property_task(123, 201)
        print("Task deleted successfully")
    except NotFoundError:
        print("Task not found or already deleted")
    ```

=== "Response Example"

    ```python
    {
        "success": True,
        "message": "Task deleted successfully",
        "deleted_id": 201
    }
    ```

---

## Common Use Cases

### Property Listing Workflow

```python
# Create tasks for new property listing
listing_tasks = [
    {
        "title": "Professional photography",
        "description": "Schedule and complete professional property photography",
        "assignee": "Photography Team",
        "priority": "high",
        "due_date": "2024-01-20",
        "category": "marketing"
    },
    {
        "title": "Create property description",
        "description": "Write compelling property description for listing",
        "assignee": "Marketing Team",
        "priority": "medium",
        "due_date": "2024-01-22",
        "category": "marketing"
    },
    {
        "title": "Upload to MLS",
        "description": "Upload property listing to Multiple Listing Service",
        "assignee": "Listing Agent",
        "priority": "high",
        "due_date": "2024-01-25",
        "category": "listing"
    }
]

for task_data in listing_tasks:
    task = client.property_tasks.create_property_task(123, task_data)
    print(f"Created task: {task['title']}")
```

### Inspection and Due Diligence

```python
# Create inspection-related tasks
inspection_tasks = [
    {
        "title": "Schedule home inspection",
        "description": "Coordinate home inspection with buyer and inspector",
        "priority": "urgent",
        "due_date": "2024-01-18",
        "category": "inspection"
    },
    {
        "title": "Review inspection report",
        "description": "Review inspection report and identify any issues",
        "priority": "high",
        "due_date": "2024-01-22",
        "category": "inspection"
    },
    {
        "title": "Address inspection items",
        "description": "Coordinate repairs or negotiations based on inspection",
        "priority": "medium",
        "due_date": "2024-01-25",
        "category": "maintenance"
    }
]

for task_data in inspection_tasks:
    client.property_tasks.create_property_task(123, task_data)
```

### Task Management and Tracking

```python
# Get all pending tasks
pending_tasks = client.property_tasks.list_property_tasks(
    123, 
    params={"status": "pending"}
)

print(f"Pending tasks: {len(pending_tasks)}")

# Update task status as work progresses
for task in pending_tasks:
    if task['title'] == "Professional photography":
        # Mark as in progress
        client.property_tasks.update_property_task(
            123, task['id'],
            {
                "status": "in_progress",
                "notes": "Photographer scheduled for tomorrow"
            }
        )

# Get overdue tasks
from datetime import datetime, date

overdue_tasks = []
for task in pending_tasks:
    if task['due_date'] and date.fromisoformat(task['due_date']) < date.today():
        overdue_tasks.append(task)

print(f"Overdue tasks: {len(overdue_tasks)}")
```

### Team Assignment and Workload

```python
# Assign tasks to team members
team_assignments = {
    "John Agent": ["Schedule inspection", "Client communication"],
    "Jane Photographer": ["Professional photography", "Virtual tour"],
    "Legal Team": ["Document review", "Title search"]
}

# Get all unassigned tasks
unassigned_tasks = client.property_tasks.list_property_tasks(
    123,
    params={"assignee": None}
)

# Assign tasks based on type
for task in unassigned_tasks:
    for assignee, task_types in team_assignments.items():
        if any(task_type.lower() in task['title'].lower() for task_type in task_types):
            client.property_tasks.update_property_task(
                123, task['id'],
                {"assignee": assignee}
            )
            break

# Get workload by assignee
assignee_workload = {}
all_tasks = client.property_tasks.list_property_tasks(123)

for task in all_tasks:
    if task['assignee'] and task['status'] != 'completed':
        assignee = task['assignee']
        if assignee not in assignee_workload:
            assignee_workload[assignee] = 0
        assignee_workload[assignee] += 1

print("Current workload:")
for assignee, count in assignee_workload.items():
    print(f"  {assignee}: {count} tasks")
```

---

## Task Status Types

Common task status values:

| Status | Description | Use Cases |
|--------|-------------|-----------|
| `pending` | Task created but not started | New tasks, waiting for assignment |
| `in_progress` | Task currently being worked on | Active work in progress |
| `completed` | Task finished successfully | Work completed |
| `cancelled` | Task cancelled or no longer needed | Changed requirements |
| `on_hold` | Task temporarily paused | Waiting for dependencies |
| `overdue` | Task past due date | Missed deadlines |

---

## Priority Levels

| Priority | Description | Use Cases |
|----------|-------------|-----------|
| `low` | Non-urgent tasks | Nice-to-have items, future planning |
| `medium` | Standard priority | Regular workflow tasks |
| `high` | Important tasks | Critical path items |
| `urgent` | Critical tasks | Immediate attention required |

---

## Task Categories

Common task categories for organization:

| Category | Description | Examples |
|----------|-------------|----------|
| `general` | General tasks | Miscellaneous activities |
| `marketing` | Marketing activities | Photography, listings, advertising |
| `inspection` | Inspections and assessments | Home inspections, appraisals |
| `maintenance` | Maintenance and repairs | Repairs, improvements |
| `legal` | Legal activities | Document review, contracts |
| `closing` | Closing process | Final preparations, documentation |
| `communication` | Client communication | Calls, emails, meetings |
| `showing` | Property showings | Tours, open houses |

---

## Error Handling

```python
from open_to_close.exceptions import (
    NotFoundError, 
    ValidationError, 
    OpenToCloseAPIError
)

try:
    task = client.property_tasks.create_property_task(123, {
        "title": "Test Task",
        "description": "This is a test task.",
        "due_date": "2024-01-20"
    })
except ValidationError as e:
    print(f"Invalid task data: {e}")
except NotFoundError:
    print("Property not found")
except OpenToCloseAPIError as e:
    print(f"API error: {e}")
```

---

## Best Practices

1. **Use clear titles**: Make task titles descriptive and actionable
2. **Set realistic due dates**: Allow adequate time for task completion
3. **Assign appropriately**: Match tasks to team members' skills and availability
4. **Track progress**: Regularly update task status and notes
5. **Prioritize effectively**: Use priority levels to focus on critical tasks
6. **Categorize consistently**: Use categories to organize and filter tasks
7. **Add detailed descriptions**: Provide clear instructions and context
8. **Monitor deadlines**: Track due dates and address overdue tasks promptly

---

## Related Resources

- [Properties API](properties.md) - Manage property information
- [Property Notes API](property-notes.md) - Add notes to properties
- [Property Documents API](property-documents.md) - Manage property documents
- [Property Contacts API](property-contacts.md) - Manage property contacts
- [Teams API](teams.md) - Manage team assignments
- [Error Handling Guide](../guides/error-handling.md) - Comprehensive error handling