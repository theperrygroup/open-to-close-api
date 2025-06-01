# Property Notes API

The Property Notes API allows you to manage notes and annotations associated with specific properties in the Open To Close platform. This includes creating, retrieving, updating, and deleting internal notes that help track important information throughout the property lifecycle.

## Overview

Property notes are internal annotations that help agents and team members track important information about properties. Common use cases include:

- Client preferences and requirements
- Property condition observations
- Meeting summaries and follow-ups
- Internal reminders and action items
- Historical context and background information

## Client Access

Access the Property Notes API through the main client:

```python
from open_to_close import OpenToCloseAPI

client = OpenToCloseAPI()
notes_api = client.property_notes
```

---

## Methods

### `list_property_notes(property_id, params=None)`

Retrieve a list of notes for a specific property.

**Parameters:**

- `property_id` (int): The ID of the property
- `params` (dict, optional): Query parameters for filtering

**Returns:** List of property note dictionaries

**Raises:**

- `OpenToCloseAPIError`: If the API request fails
- `NotFoundError`: If the property is not found
- `ValidationError`: If parameters are invalid
- `AuthenticationError`: If authentication fails

=== "Basic Usage"

    ```python
    # Get all notes for a property
    notes = client.property_notes.list_property_notes(123)
    
    for note in notes:
        print(f"Note: {note['content'][:50]}... - {note['author']}")
    ```

=== "With Filtering"

    ```python
    # Get notes with filtering
    agent_notes = client.property_notes.list_property_notes(
        123, 
        params={"author": "John Agent"}
    )
    
    # Filter by priority and date range
    important_notes = client.property_notes.list_property_notes(
        123,
        params={
            "priority": "high",
            "created_after": "2024-01-01"
        }
    )
    ```

=== "Response Example"

    ```python
    [
        {
            "id": 101,
            "property_id": 123,
            "content": "Client showed strong interest in this property. Mentioned they love the kitchen layout.",
            "author": "John Agent",
            "priority": "medium",
            "tags": ["client-feedback", "kitchen"],
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "is_private": false
        },
        {
            "id": 102,
            "property_id": 123,
            "content": "Need to follow up on inspection report. Minor electrical issues noted.",
            "author": "Jane Agent",
            "priority": "high",
            "tags": ["follow-up", "inspection", "electrical"],
            "created_at": "2024-01-16T14:20:00Z",
            "updated_at": "2024-01-16T14:20:00Z",
            "is_private": true
        }
    ]
    ```

---

### `create_property_note(property_id, note_data)`

Add a note to a specific property.

**Parameters:**

- `property_id` (int): The ID of the property
- `note_data` (dict): Note information

**Returns:** Dictionary representing the newly created property note

**Raises:**

- `OpenToCloseAPIError`: If the API request fails
- `ValidationError`: If note data is invalid
- `NotFoundError`: If the property is not found
- `AuthenticationError`: If authentication fails

=== "Basic Usage"

    ```python
    note = client.property_notes.create_property_note(123, {
        "content": "Client showed strong interest in this property.",
        "author": "John Agent",
        "priority": "medium"
    })
    
    print(f"Created note {note['id']}: {note['content'][:30]}...")
    ```

=== "With Full Details"

    ```python
    note = client.property_notes.create_property_note(123, {
        "content": "Comprehensive inspection completed. Property is in excellent condition with minor cosmetic updates needed in the guest bathroom.",
        "author": "Jane Inspector",
        "priority": "high",
        "tags": ["inspection", "condition", "bathroom"],
        "is_private": False,
        "category": "inspection"
    })
    ```

=== "Response Example"

    ```python
    {
        "id": 103,
        "property_id": 123,
        "content": "Client showed strong interest in this property.",
        "author": "John Agent",
        "priority": "medium",
        "tags": [],
        "created_at": "2024-01-17T09:15:00Z",
        "updated_at": "2024-01-17T09:15:00Z",
        "is_private": false,
        "category": "general"
    }
    ```

---

### `retrieve_property_note(property_id, note_id)`

Retrieve a specific note for a specific property.

**Parameters:**

- `property_id` (int): The ID of the property
- `note_id` (int): The ID of the note to retrieve

**Returns:** Dictionary representing the property note

**Raises:**

- `NotFoundError`: If the property or note is not found
- `OpenToCloseAPIError`: If the API request fails
- `AuthenticationError`: If authentication fails

=== "Basic Usage"

    ```python
    note = client.property_notes.retrieve_property_note(123, 101)
    print(f"Note content: {note['content']}")
    print(f"Note author: {note['author']}")
    ```

=== "Error Handling"

    ```python
    from open_to_close.exceptions import NotFoundError
    
    try:
        note = client.property_notes.retrieve_property_note(123, 999)
    except NotFoundError:
        print("Note not found")
    ```

=== "Response Example"

    ```python
    {
        "id": 101,
        "property_id": 123,
        "content": "Client showed strong interest in this property. Mentioned they love the kitchen layout and the natural lighting in the living room.",
        "author": "John Agent",
        "priority": "medium",
        "tags": ["client-feedback", "kitchen", "lighting"],
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z",
        "is_private": false,
        "category": "client-interaction",
        "attachments": []
    }
    ```

---

### `update_property_note(property_id, note_id, note_data)`

Update a specific note for a specific property.

**Parameters:**

- `property_id` (int): The ID of the property
- `note_id` (int): The ID of the note to update
- `note_data` (dict): Fields to update

**Returns:** Dictionary representing the updated property note

**Raises:**

- `NotFoundError`: If the property or note is not found
- `ValidationError`: If note data is invalid
- `OpenToCloseAPIError`: If the API request fails
- `AuthenticationError`: If authentication fails

=== "Basic Usage"

    ```python
    updated_note = client.property_notes.update_property_note(
        123, 101, 
        {"priority": "high"}
    )
    ```

=== "Multiple Fields"

    ```python
    updated_note = client.property_notes.update_property_note(
        123, 101, 
        {
            "content": "Client showed strong interest and submitted an offer!",
            "priority": "high",
            "tags": ["client-feedback", "offer-submitted"],
            "category": "offer"
        }
    )
    ```

=== "Response Example"

    ```python
    {
        "id": 101,
        "property_id": 123,
        "content": "Client showed strong interest and submitted an offer!",
        "author": "John Agent",
        "priority": "high",
        "tags": ["client-feedback", "offer-submitted"],
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-17T11:45:00Z",
        "is_private": false,
        "category": "offer"
    }
    ```

---

### `delete_property_note(property_id, note_id)`

Remove a note from a specific property.

**Parameters:**

- `property_id` (int): The ID of the property
- `note_id` (int): The ID of the note to remove

**Returns:** Dictionary containing the API response

**Raises:**

- `NotFoundError`: If the property or note is not found
- `OpenToCloseAPIError`: If the API request fails
- `AuthenticationError`: If authentication fails

=== "Basic Usage"

    ```python
    result = client.property_notes.delete_property_note(123, 101)
    print("Note deleted successfully")
    ```

=== "With Error Handling"

    ```python
    from open_to_close.exceptions import NotFoundError
    
    try:
        result = client.property_notes.delete_property_note(123, 101)
        print("Note deleted successfully")
    except NotFoundError:
        print("Note not found or already deleted")
    ```

=== "Response Example"

    ```python
    {
        "success": True,
        "message": "Note deleted successfully",
        "deleted_id": 101
    }
    ```

---

## Common Use Cases

### Property Showing Notes

```python
# Add notes during property showing
showing_note = client.property_notes.create_property_note(123, {
    "content": "Showed property to the Johnson family. They were impressed with the master suite and backyard. Concerned about the age of the HVAC system.",
    "author": "Sarah Agent",
    "priority": "medium",
    "tags": ["showing", "johnson-family", "hvac-concern"],
    "category": "showing"
})

# Follow up with additional information
follow_up = client.property_notes.create_property_note(123, {
    "content": "Provided HVAC inspection report to Johnson family. System was serviced last year and is in good condition.",
    "author": "Sarah Agent",
    "priority": "medium",
    "tags": ["follow-up", "johnson-family", "hvac-report"],
    "category": "follow-up"
})
```

### Inspection and Maintenance Tracking

```python
# Document inspection findings
inspection_note = client.property_notes.create_property_note(123, {
    "content": "Home inspection completed. Minor issues: loose handrail on stairs, small leak under kitchen sink, recommend gutter cleaning.",
    "author": "Mike Inspector",
    "priority": "high",
    "tags": ["inspection", "handrail", "plumbing", "gutters"],
    "category": "inspection"
})

# Track resolution of issues
resolution_note = client.property_notes.create_property_note(123, {
    "content": "All inspection items addressed: handrail tightened, sink leak repaired, gutters cleaned.",
    "author": "Property Manager",
    "priority": "medium",
    "tags": ["resolved", "maintenance"],
    "category": "maintenance"
})
```

### Client Communication Log

```python
# Log client interactions
communication_notes = [
    {
        "content": "Initial client consultation. Looking for 3BR/2BA in suburban area, budget $400-450k.",
        "tags": ["consultation", "requirements"],
        "category": "client-interaction"
    },
    {
        "content": "Sent property listings matching criteria. Client interested in 3 properties for viewing.",
        "tags": ["listings-sent", "interested"],
        "category": "communication"
    },
    {
        "content": "Scheduled showings for this weekend. Client particularly excited about this property.",
        "tags": ["showing-scheduled", "excited"],
        "category": "scheduling"
    }
]

for note_data in communication_notes:
    note_data.update({
        "author": "Lisa Agent",
        "priority": "medium"
    })
    client.property_notes.create_property_note(123, note_data)
```

### Team Collaboration

```python
# Get all notes for team review
all_notes = client.property_notes.list_property_notes(123)

# Filter by category for specific workflows
inspection_notes = client.property_notes.list_property_notes(
    123, 
    params={"category": "inspection"}
)

client_notes = client.property_notes.list_property_notes(
    123, 
    params={"category": "client-interaction"}
)

# Create summary note for team
summary_content = f"""
Property Summary:
- Total notes: {len(all_notes)}
- Inspection notes: {len(inspection_notes)}
- Client interaction notes: {len(client_notes)}
- Last activity: {max(note['updated_at'] for note in all_notes)}
"""

client.property_notes.create_property_note(123, {
    "content": summary_content,
    "author": "Team Lead",
    "priority": "low",
    "tags": ["summary", "team-review"],
    "category": "summary"
})
```

---

## Note Categories

Common note categories for organization:

| Category | Description | Use Cases |
|----------|-------------|-----------|
| `general` | General notes | Miscellaneous observations |
| `client-interaction` | Client communications | Meetings, calls, preferences |
| `showing` | Property showings | Showing feedback, reactions |
| `inspection` | Inspections and assessments | Condition reports, issues |
| `maintenance` | Maintenance and repairs | Work orders, completions |
| `marketing` | Marketing activities | Listing updates, promotions |
| `offer` | Offers and negotiations | Offer details, counteroffers |
| `closing` | Closing process | Documentation, timeline |
| `follow-up` | Follow-up actions | Reminders, next steps |

---

## Priority Levels

| Priority | Description | Use Cases |
|----------|-------------|-----------|
| `low` | Informational notes | General observations, FYI items |
| `medium` | Standard notes | Regular updates, standard follow-ups |
| `high` | Important notes | Urgent issues, critical information |
| `urgent` | Critical notes | Immediate action required |

---

## Error Handling

```python
from open_to_close.exceptions import (
    NotFoundError, 
    ValidationError, 
    OpenToCloseAPIError
)

try:
    note = client.property_notes.create_property_note(123, {
        "content": "This is a test note.",
        "author": "Test Agent",
        "priority": "medium"
    })
except ValidationError as e:
    print(f"Invalid note data: {e}")
except NotFoundError:
    print("Property not found")
except OpenToCloseAPIError as e:
    print(f"API error: {e}")
```

---

## Best Practices

1. **Be descriptive**: Write clear, detailed notes that provide context
2. **Use consistent authors**: Maintain consistent author names for tracking
3. **Categorize appropriately**: Use categories to organize notes by type
4. **Set proper priorities**: Use priority levels to highlight important information
5. **Tag effectively**: Use tags for easy searching and filtering
6. **Update when needed**: Keep notes current by updating them as situations change
7. **Respect privacy**: Use private notes for sensitive internal information
8. **Regular cleanup**: Archive or delete outdated notes periodically

---

## Related Resources

- [Properties API](properties.md) - Manage property information
- [Property Contacts API](property-contacts.md) - Manage property contacts
- [Property Documents API](property-documents.md) - Manage property documents
- [Property Tasks API](property-tasks.md) - Manage property tasks
- [Error Handling Guide](../guides/error-handling.md) - Comprehensive error handling