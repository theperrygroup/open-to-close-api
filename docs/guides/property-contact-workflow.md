# Property and Contact Creation Workflow

This guide demonstrates how to create a complete real estate transaction by creating a property (deal) and associating multiple contacts with it. This workflow is based on successful API testing and uses only verified working field formats.

!!! success "Verified Workflow"
    ✅ This workflow has been tested against the live Open To Close API  
    ✅ All examples use only supported field formats  
    ✅ Complete end-to-end transaction creation

---

## 🎯 Overview

In Open To Close, a **property** represents a real estate transaction or deal. Each property can have multiple **contacts** associated with it through **property-contact associations**. This guide shows how to:

1. Create a new property (transaction)
2. Create multiple contacts with the correct field format
3. Link contacts to the property
4. Verify the complete transaction

---

## 🔑 Key API Requirements

!!! warning "Critical Field Requirements"
    - **Contacts**: Must use `first_name` and `last_name` separately - the `name` field is NOT supported
    - **Properties**: Support flexible creation with title, status, client type, and purchase amount
    - **Associations**: Simple linking by contact ID only

---

## 🚀 Complete Workflow Example

### Step 1: Initialize the Client

```python
from open_to_close import OpenToCloseAPI
from open_to_close.exceptions import (
    OpenToCloseAPIError,
    ValidationError,
    AuthenticationError
)

# Initialize the API client
client = OpenToCloseAPI()
```

### Step 2: Create the Property (Transaction)

```python
# Define property/transaction details
property_info = {
    "title": "123 Main Street Sale Transaction",
    "client_type": "Buyer",  # Options: "Buyer", "Seller", "Dual"
    "status": "Active",      # Options: "pre-mls", "active", "under contract", etc.
    "purchase_amount": 450000
}

# Create the property
property_result = client.properties.create_property(property_info)
property_id = property_result['id']

print(f"✅ Property created with ID: {property_id}")
```

### Step 3: Create Contacts with Correct Field Format

```python
# Define contacts using ONLY supported fields
contacts_to_create = [
    {
        "first_name": "John",
        "last_name": "Smith",
        "email": "john.smith@email.com",
        "phone": "+1-555-0101"
    },
    {
        "first_name": "Sarah", 
        "last_name": "Johnson",
        "email": "sarah.johnson@email.com",
        "phone": "+1-555-0102"
    },
    {
        "first_name": "Michael",
        "last_name": "Brown",
        "email": "michael.brown@email.com",
        "phone": "+1-555-0103"
    },
    {
        "first_name": "Lisa",
        "last_name": "Davis",
        "email": "lisa.davis@email.com",
        "phone": "+1-555-0104"
    }
]

# Create all contacts
created_contacts = []
for i, contact_info in enumerate(contacts_to_create):
    contact_name = f"{contact_info['first_name']} {contact_info['last_name']}"
    print(f"Creating contact {i+1}/{len(contacts_to_create)}: {contact_name}")
    
    contact_result = client.contacts.create_contact(contact_info)
    created_contacts.append(contact_result)
    
    print(f"✅ Contact created with ID: {contact_result['id']}")
```

### Step 4: Link Contacts to Property

```python
# Create property-contact associations
linked_contacts = []
for i, contact in enumerate(created_contacts):
    contact_name = f"{contact['first_name']} {contact['last_name']}"
    print(f"Linking contact {i+1}/{len(created_contacts)}: {contact_name}")
    
    # Create the association
    association = client.property_contacts.create_property_contact(
        property_id=property_id,
        contact_data={"contact_id": contact['id']}
    )
    
    linked_contacts.append(association)
    print(f"✅ Contact linked with association ID: {association['id']}")
```

### Step 5: Verify the Complete Transaction

```python
# Retrieve the property with its contacts
print(f"\n🔍 Verifying transaction {property_id}...")

# Get property details
property_data = client.properties.retrieve_property(property_id)

# Get all associated contacts
property_contacts = client.property_contacts.list_property_contacts(property_id)

print(f"✅ Verification complete:")
print(f"   Property ID: {property_id}")
print(f"   Associated contacts: {len(property_contacts)}")

# Display contact details
for i, pc in enumerate(property_contacts):
    contact = pc['contact']
    contact_name = f"{contact['first_name']} {contact['last_name']}"
    print(f"   {i+1}. {contact_name} (ID: {contact['id']})")
```

---

## 🏗️ Complete Working Example

Here's a complete, working script that you can run:

```python
#!/usr/bin/env python3
"""
Complete Property-Contact Creation Example
Tested against the live Open To Close API
"""

from open_to_close import OpenToCloseAPI
from open_to_close.exceptions import OpenToCloseAPIError
from datetime import datetime
import json

def create_complete_transaction():
    """Create a complete real estate transaction with contacts."""
    
    print("🏠 Creating Complete Real Estate Transaction")
    print("=" * 50)
    
    try:
        # Initialize client
        client = OpenToCloseAPI()
        
        # Step 1: Create property
        print("\n📝 Step 1: Creating property...")
        property_info = {
            "title": "456 Oak Avenue Transaction",
            "client_type": "Buyer",
            "status": "Active", 
            "purchase_amount": 525000
        }
        
        property_result = client.properties.create_property(property_info)
        property_id = property_result['id']
        print(f"✅ Property created with ID: {property_id}")
        
        # Step 2: Create contacts
        print("\n👥 Step 2: Creating contacts...")
        contacts_data = [
            {
                "first_name": "Alice",
                "last_name": "Cooper",
                "email": "alice.cooper@email.com",
                "phone": "+1-555-2001"
            },
            {
                "first_name": "Bob", 
                "last_name": "Wilson",
                "email": "bob.wilson@email.com",
                "phone": "+1-555-2002"
            }
        ]
        
        created_contacts = []
        for contact_data in contacts_data:
            contact_name = f"{contact_data['first_name']} {contact_data['last_name']}"
            print(f"   Creating: {contact_name}")
            
            contact = client.contacts.create_contact(contact_data)
            created_contacts.append(contact)
            print(f"   ✅ Created with ID: {contact['id']}")
        
        # Step 3: Link contacts to property
        print("\n🔗 Step 3: Linking contacts to property...")
        associations = []
        for contact in created_contacts:
            contact_name = f"{contact['first_name']} {contact['last_name']}"
            print(f"   Linking: {contact_name}")
            
            association = client.property_contacts.create_property_contact(
                property_id=property_id,
                contact_data={"contact_id": contact['id']}
            )
            associations.append(association)
            print(f"   ✅ Linked with association ID: {association['id']}")
        
        # Step 4: Verify transaction
        print("\n🔍 Step 4: Verifying transaction...")
        property_contacts = client.property_contacts.list_property_contacts(property_id)
        
        print(f"✅ Transaction verification complete!")
        print(f"   Property ID: {property_id}")
        print(f"   Total contacts: {len(property_contacts)}")
        print(f"   Associations: {len(associations)}")
        
        # Return transaction summary
        return {
            'property_id': property_id,
            'property': property_result,
            'contacts': created_contacts,
            'associations': associations,
            'verification': property_contacts,
            'created_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"❌ Error creating transaction: {e}")
        return None

if __name__ == "__main__":
    result = create_complete_transaction()
    
    if result:
        print(f"\n🎉 SUCCESS: Transaction {result['property_id']} created successfully!")
        
        # Save result for reference
        with open(f"transaction_{result['property_id']}.json", 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"📁 Transaction data saved to transaction_{result['property_id']}.json")
    else:
        print("\n❌ FAILED: Could not create transaction")
```

---

## 🚨 Common Pitfalls to Avoid

### ❌ Using Unsupported Contact Fields

```python
# ❌ DON'T DO THIS - Will cause "Bad request" errors
bad_contact = {
    "name": "John Doe",        # NOT SUPPORTED!
    "company": "ABC Corp",     # May not work
    "title": "Manager"         # May not work
}
```

### ✅ Correct Contact Format

```python
# ✅ DO THIS - Uses only supported fields
good_contact = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "+1555123456"
}
```

---

## 🔧 Helper Functions

### Contact Name Utilities

```python
def get_contact_full_name(contact):
    """Get full name from contact data."""
    first_name = contact.get('first_name', '')
    last_name = contact.get('last_name', '')
    return f"{first_name} {last_name}".strip() or 'N/A'

def format_contact_info(contact):
    """Format contact information for display."""
    name = get_contact_full_name(contact)
    email = contact.get('email', 'No email')
    phone = contact.get('phone', 'No phone')
    return f"{name} | {email} | {phone}"
```

### Transaction Management

```python
def get_transaction_summary(property_id):
    """Get a complete summary of a property transaction."""
    client = OpenToCloseAPI()
    
    # Get property details
    property_data = client.properties.retrieve_property(property_id)
    
    # Get associated contacts
    property_contacts = client.property_contacts.list_property_contacts(property_id)
    
    return {
        'property': property_data,
        'contacts': property_contacts,
        'contact_count': len(property_contacts),
        'retrieved_at': datetime.now().isoformat()
    }

def create_minimal_transaction(title, contact_email):
    """Create a minimal transaction with one contact."""
    client = OpenToCloseAPI()
    
    # Create property
    property_result = client.properties.create_property(title)
    
    # Create contact
    contact_result = client.contacts.create_contact({"email": contact_email})
    
    # Link them
    association = client.property_contacts.create_property_contact(
        property_id=property_result['id'],
        contact_data={"contact_id": contact_result['id']}
    )
    
    return {
        'property_id': property_result['id'],
        'contact_id': contact_result['id'], 
        'association_id': association['id']
    }
```

---

## 📊 Transaction Data Structure

When you create a complete transaction, you'll get data structures like this:

### Property Data
```json
{
  "id": 997625,
  "created": 1749039487
}
```

### Contact Data
```json
{
  "id": 6011149,
  "created": {
    "date": "2025-06-04 01:18:07.797121",
    "timezone_type": 3,
    "timezone": "GMT"
  },
  "first_name": "John",
  "last_name": "Smith",
  "email": "john.smith@email.com",
  "phone": "15550101"
}
```

### Association Data
```json
{
  "id": 7484664,
  "created": {
    "date": "2025-06-04 01:18:08.767548",
    "timezone_type": 3,
    "timezone": "UTC"
  },
  "priority": "",
  "property": {"id": 997625},
  "contact": {
    "id": 6011149,
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@email.com"
  },
  "contact_role": []
}
```

---

## 🎯 Next Steps

After creating your property and contacts:

1. **Add Notes**: Use `client.property_notes.create_property_note()` to add transaction notes
2. **Add Tasks**: Use `client.property_tasks.create_property_task()` to create action items  
3. **Upload Documents**: Use `client.property_documents.create_property_document()` for files
4. **Send Emails**: Use `client.property_emails.create_property_email()` for communication

---

## 🔍 Troubleshooting

### Contact Creation Fails
- ✅ Check that you're using `first_name`/`last_name` instead of `name`
- ✅ Ensure at least one of: `first_name`, `last_name`, `email`, or `phone` is provided
- ✅ Verify email format contains "@" symbol

### Property Creation Fails  
- ✅ Check that the title is provided and non-empty
- ✅ Verify client_type is one of: "Buyer", "Seller", "Dual"
- ✅ Ensure status is valid (e.g., "Active", "pre-mls", "under contract")

### Association Creation Fails
- ✅ Verify both property and contact exist
- ✅ Check that contact_id is an integer
- ✅ Ensure you're using the correct property and contact IDs

---

!!! tip "Testing Your Workflow"
    Always test your property and contact creation workflow in a development environment first. Use the provided examples as a starting point and modify them for your specific needs. 