# Property Emails API

The Property Emails API allows you to manage email communications associated with specific properties in the Open To Close platform. This includes tracking email correspondence, managing communication history, and organizing property-related email threads.

## Overview

Property emails help track all communication related to a specific property throughout its lifecycle. This includes:

- Client communications and updates
- Agent-to-agent correspondence
- Vendor and service provider emails
- Marketing and promotional emails
- System-generated notifications

## Client Access

Access the Property Emails API through the main client:

```python
from open_to_close import OpenToCloseAPI

client = OpenToCloseAPI()
emails_api = client.property_emails
```

---

## Methods

### `list_property_emails(property_id, params=None)`

Retrieve a list of emails for a specific property.

**Parameters:**

- `property_id` (int): The ID of the property
- `params` (dict, optional): Query parameters for filtering

**Returns:** List of property email dictionaries

**Raises:**

- `OpenToCloseAPIError`: If the API request fails
- `NotFoundError`: If the property is not found
- `ValidationError`: If parameters are invalid
- `AuthenticationError`: If authentication fails

=== "Basic Usage"

    ```python
    # Get all emails for a property
    emails = client.property_emails.list_property_emails(123)
    
    for email in emails:
        print(f"Email: {email['subject']} - {email['status']}")
    ```

=== "With Filtering"

    ```python
    # Get emails with filtering
    sent_emails = client.property_emails.list_property_emails(
        123, 
        params={"status": "sent"}
    )
    
    # Filter by date range and recipient
    recent_emails = client.property_emails.list_property_emails(
        123,
        params={
            "sent_after": "2024-01-01",
            "recipient": "client@example.com"
        }
    )
    ```

=== "Response Example"

    ```python
    [
        {
            "id": 789,
            "property_id": 123,
            "subject": "Property Update - Inspection Scheduled",
            "body": "Your property inspection has been scheduled for...",
            "sender": "agent@realty.com",
            "recipient": "client@example.com",
            "status": "sent",
            "sent_at": "2024-01-15T10:30:00Z",
            "created_at": "2024-01-15T10:25:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "thread_id": "thread_abc123"
        },
        {
            "id": 790,
            "property_id": 123,
            "subject": "Re: Property Update - Inspection Scheduled",
            "body": "Thank you for the update. I'll be available at...",
            "sender": "client@example.com",
            "recipient": "agent@realty.com",
            "status": "received",
            "sent_at": "2024-01-15T14:20:00Z",
            "created_at": "2024-01-15T14:20:00Z",
            "updated_at": "2024-01-15T14:20:00Z",
            "thread_id": "thread_abc123"
        }
    ]
    ```

---

### `create_property_email(property_id, email_data)`

Add an email to a specific property.

**Parameters:**

- `property_id` (int): The ID of the property
- `email_data` (dict): Email information

**Returns:** Dictionary representing the newly created property email

**Raises:**

- `OpenToCloseAPIError`: If the API request fails
- `ValidationError`: If email data is invalid
- `NotFoundError`: If the property is not found
- `AuthenticationError`: If authentication fails

=== "Basic Usage"

    ```python
    email = client.property_emails.create_property_email(123, {
        "subject": "Property Update",
        "body": "The property status has been updated.",
        "recipient": "client@example.com"
    })
    
    print(f"Created email {email['id']}: {email['subject']}")
    ```

=== "With Full Details"

    ```python
    email = client.property_emails.create_property_email(123, {
        "subject": "Inspection Report Available",
        "body": "The inspection report for your property is now available...",
        "recipient": "client@example.com",
        "cc": ["agent2@realty.com"],
        "bcc": ["manager@realty.com"],
        "priority": "high",
        "thread_id": "thread_abc123"
    })
    ```

=== "Response Example"

    ```python
    {
        "id": 791,
        "property_id": 123,
        "subject": "Property Update",
        "body": "The property status has been updated.",
        "sender": "current_user@realty.com",
        "recipient": "client@example.com",
        "status": "draft",
        "sent_at": null,
        "created_at": "2024-01-17T09:15:00Z",
        "updated_at": "2024-01-17T09:15:00Z",
        "thread_id": "thread_def456"
    }
    ```

---

### `retrieve_property_email(property_id, email_id)`

Retrieve a specific email for a specific property.

**Parameters:**

- `property_id` (int): The ID of the property
- `email_id` (int): The ID of the email to retrieve

**Returns:** Dictionary representing the property email

**Raises:**

- `NotFoundError`: If the property or email is not found
- `OpenToCloseAPIError`: If the API request fails
- `AuthenticationError`: If authentication fails

=== "Basic Usage"

    ```python
    email = client.property_emails.retrieve_property_email(123, 789)
    print(f"Email subject: {email['subject']}")
    print(f"Email status: {email['status']}")
    ```

=== "Error Handling"

    ```python
    from open_to_close.exceptions import NotFoundError
    
    try:
        email = client.property_emails.retrieve_property_email(123, 999)
    except NotFoundError:
        print("Email not found")
    ```

=== "Response Example"

    ```python
    {
        "id": 789,
        "property_id": 123,
        "subject": "Property Update - Inspection Scheduled",
        "body": "Your property inspection has been scheduled for January 20th at 2:00 PM...",
        "sender": "agent@realty.com",
        "recipient": "client@example.com",
        "cc": ["assistant@realty.com"],
        "bcc": [],
        "status": "sent",
        "priority": "normal",
        "sent_at": "2024-01-15T10:30:00Z",
        "created_at": "2024-01-15T10:25:00Z",
        "updated_at": "2024-01-15T10:30:00Z",
        "thread_id": "thread_abc123",
        "attachments": [
            {
                "name": "inspection_details.pdf",
                "url": "https://example.com/attachments/inspection_details.pdf"
            }
        ]
    }
    ```

---

### `update_property_email(property_id, email_id, email_data)`

Update a specific email for a specific property.

**Parameters:**

- `property_id` (int): The ID of the property
- `email_id` (int): The ID of the email to update
- `email_data` (dict): Fields to update

**Returns:** Dictionary representing the updated property email

**Raises:**

- `NotFoundError`: If the property or email is not found
- `ValidationError`: If email data is invalid
- `OpenToCloseAPIError`: If the API request fails
- `AuthenticationError`: If authentication fails

=== "Basic Usage"

    ```python
    updated_email = client.property_emails.update_property_email(
        123, 789, 
        {"status": "sent"}
    )
    ```

=== "Multiple Fields"

    ```python
    updated_email = client.property_emails.update_property_email(
        123, 789, 
        {
            "subject": "Updated: Property Inspection Scheduled",
            "priority": "high",
            "status": "sent"
        }
    )
    ```

=== "Response Example"

    ```python
    {
        "id": 789,
        "property_id": 123,
        "subject": "Updated: Property Inspection Scheduled",
        "body": "Your property inspection has been scheduled for...",
        "sender": "agent@realty.com",
        "recipient": "client@example.com",
        "status": "sent",
        "priority": "high",
        "sent_at": "2024-01-17T11:45:00Z",
        "created_at": "2024-01-15T10:25:00Z",
        "updated_at": "2024-01-17T11:45:00Z",
        "thread_id": "thread_abc123"
    }
    ```

---

### `delete_property_email(property_id, email_id)`

Remove an email from a specific property.

**Parameters:**

- `property_id` (int): The ID of the property
- `email_id` (int): The ID of the email to remove

**Returns:** Dictionary containing the API response

**Raises:**

- `NotFoundError`: If the property or email is not found
- `OpenToCloseAPIError`: If the API request fails
- `AuthenticationError`: If authentication fails

=== "Basic Usage"

    ```python
    result = client.property_emails.delete_property_email(123, 789)
    print("Email deleted successfully")
    ```

=== "With Error Handling"

    ```python
    from open_to_close.exceptions import NotFoundError
    
    try:
        result = client.property_emails.delete_property_email(123, 789)
        print("Email deleted successfully")
    except NotFoundError:
        print("Email not found or already deleted")
    ```

=== "Response Example"

    ```python
    {
        "success": True,
        "message": "Email deleted successfully",
        "deleted_id": 789
    }
    ```

---

## Common Use Cases

### Email Communication Workflow

```python
# 1. Create a draft email
draft_email = client.property_emails.create_property_email(123, {
    "subject": "Property Inspection Update",
    "body": "Dear Client, your property inspection has been scheduled...",
    "recipient": "client@example.com",
    "status": "draft"
})

# 2. Update and send the email
sent_email = client.property_emails.update_property_email(
    123, draft_email['id'],
    {
        "status": "sent",
        "sent_at": "2024-01-17T10:00:00Z"
    }
)

# 3. Track email responses
responses = client.property_emails.list_property_emails(
    123,
    params={
        "thread_id": sent_email['thread_id'],
        "status": "received"
    }
)

print(f"Received {len(responses)} responses")
```

### Email Thread Management

```python
# Get all emails in a thread
thread_emails = client.property_emails.list_property_emails(
    123,
    params={"thread_id": "thread_abc123"}
)

# Sort by creation date to see conversation flow
thread_emails.sort(key=lambda x: x['created_at'])

print("Email Thread:")
for email in thread_emails:
    print(f"  {email['sender']} -> {email['recipient']}: {email['subject']}")
```

### Bulk Email Operations

```python
# Get all unread emails across multiple properties
property_ids = [123, 124, 125]
unread_emails = []

for prop_id in property_ids:
    emails = client.property_emails.list_property_emails(
        prop_id,
        params={"status": "received", "read": False}
    )
    unread_emails.extend(emails)

print(f"Total unread emails: {len(unread_emails)}")

# Mark emails as read
for email in unread_emails:
    client.property_emails.update_property_email(
        email['property_id'],
        email['id'],
        {"read": True}
    )
```

---

## Email Status Types

Common email status values:

| Status | Description |
|--------|-------------|
| `draft` | Email created but not sent |
| `sent` | Email successfully sent |
| `delivered` | Email delivered to recipient |
| `opened` | Email opened by recipient |
| `clicked` | Links in email clicked |
| `bounced` | Email delivery failed |
| `received` | Incoming email received |

---

## Email Priority Levels

| Priority | Description | Use Case |
|----------|-------------|----------|
| `low` | Non-urgent communications | General updates, newsletters |
| `normal` | Standard communications | Regular client updates |
| `high` | Important communications | Urgent updates, deadlines |
| `urgent` | Critical communications | Emergency notifications |

---

## Error Handling

```python
from open_to_close.exceptions import (
    NotFoundError, 
    ValidationError, 
    OpenToCloseAPIError
)

try:
    email = client.property_emails.create_property_email(123, {
        "subject": "Test Email",
        "body": "This is a test email.",
        "recipient": "client@example.com"
    })
except ValidationError as e:
    print(f"Invalid email data: {e}")
except NotFoundError:
    print("Property not found")
except OpenToCloseAPIError as e:
    print(f"API error: {e}")
```

---

## Best Practices

1. **Use clear subjects**: Make email subjects descriptive and searchable
2. **Organize with threads**: Use thread IDs to group related emails
3. **Track status**: Monitor email delivery and read status
4. **Set priorities**: Use appropriate priority levels for different communications
5. **Handle bounces**: Implement logic to handle bounced emails
6. **Archive old emails**: Regularly clean up old email records
7. **Respect privacy**: Ensure compliance with email privacy regulations

---

## Related Resources

- [Properties API](properties.md) - Manage property information
- [Property Contacts API](property-contacts.md) - Manage property contacts
- [Property Notes API](property-notes.md) - Add notes to properties
- [Property Documents API](property-documents.md) - Manage property documents
- [Error Handling Guide](../guides/error-handling.md) - Comprehensive error handling