# Comprehensive Examples

Real-world usage examples for the Open To Close API client.

## Table of Contents

- [Basic CRUD Operations](#basic-crud-operations)
- [Working with Properties](#working-with-properties)
- [Managing Property Relationships](#managing-property-relationships)
- [Error Handling Patterns](#error-handling-patterns)
- [Bulk Operations](#bulk-operations)
- [Advanced Filtering](#advanced-filtering)
- [Real Estate Workflow Examples](#real-estate-workflow-examples)

## Basic CRUD Operations

### Complete Contact Management

```python
from open_to_close_api import OpenToCloseAPI, NotFoundError, ValidationError

client = OpenToCloseAPI()

# Create a new contact
def create_contact_example():
    contact_data = {
        "first_name": "Sarah",
        "last_name": "Johnson",
        "email": "sarah.johnson@example.com",
        "phone": "+1555123456",
        "notes": "Potential first-time buyer"
    }
    
    try:
        contact = client.contacts.create_contact(contact_data)
        print(f"Created contact: {contact['first_name']} {contact['last_name']} (ID: {contact['id']})")
        return contact
    except ValidationError as e:
        print(f"Invalid contact data: {e}")
        return None

# Update contact information
def update_contact_example(contact_id: int):
    updates = {
        "phone": "+1555987654",
        "notes": "Approved for mortgage pre-qualification"
    }
    
    try:
        updated_contact = client.contacts.update_contact(contact_id, updates)
        print(f"Updated contact {contact_id}")
        return updated_contact
    except NotFoundError:
        print(f"Contact {contact_id} not found")
    except ValidationError as e:
        print(f"Invalid update data: {e}")

# Retrieve and display contact details
def get_contact_details(contact_id: int):
    try:
        contact = client.contacts.retrieve_contact(contact_id)
        print(f"Contact Details:")
        print(f"  Name: {contact['first_name']} {contact['last_name']}")
        print(f"  Email: {contact['email']}")
        print(f"  Phone: {contact['phone']}")
        return contact
    except NotFoundError:
        print(f"Contact {contact_id} not found")
        return None
```

## Working with Properties

### Property Lifecycle Management

```python
def create_property_listing():
    """Create a new property listing with complete information."""
    
    property_data = {
        "address": "456 Oak Avenue",
        "city": "Springfield",
        "state": "CA",
        "zip_code": "90210",
        "property_type": "single_family",
        "bedrooms": 4,
        "bathrooms": 3,
        "square_feet": 2500,
        "lot_size": 0.25,
        "listing_price": 750000,
        "status": "active",
        "description": "Beautiful family home in desirable neighborhood"
    }
    
    try:
        property = client.properties.create_property(property_data)
        print(f"Created property listing: {property['address']} (ID: {property['id']})")
        return property
    except ValidationError as e:
        print(f"Invalid property data: {e}")
        return None

def update_property_status(property_id: int, new_status: str):
    """Update property status (e.g., pending, sold, withdrawn)."""
    
    try:
        updated_property = client.properties.update_property(property_id, {
            "status": new_status
        })
        print(f"Property {property_id} status updated to: {new_status}")
        return updated_property
    except NotFoundError:
        print(f"Property {property_id} not found")
    except ValidationError as e:
        print(f"Invalid status: {e}")

def search_properties_by_criteria():
    """Search for properties based on specific criteria."""
    
    search_params = {
        "city": "Springfield",
        "min_price": 500000,
        "max_price": 800000,
        "bedrooms__gte": 3,  # 3 or more bedrooms
        "property_type": "single_family",
        "status": "active"
    }
    
    try:
        properties = client.properties.list_properties(params=search_params)
        print(f"Found {len(properties)} properties matching criteria:")
        
        for prop in properties:
            print(f"  {prop['address']} - ${prop['listing_price']:,} ({prop['bedrooms']}br/{prop['bathrooms']}ba)")
            
        return properties
    except Exception as e:
        print(f"Error searching properties: {e}")
        return []
```

## Managing Property Relationships

### Complete Property Documentation

```python
def manage_property_documents(property_id: int):
    """Comprehensive property document management."""
    
    # Add multiple document types
    documents_to_create = [
        {
            "title": "Purchase Agreement",
            "description": "Signed purchase agreement",
            "document_type": "contract",
            "file_url": "https://docs.example.com/purchase_agreement.pdf"
        },
        {
            "title": "Property Inspection Report",
            "description": "Professional inspection results",
            "document_type": "inspection",
            "file_url": "https://docs.example.com/inspection_report.pdf"
        },
        {
            "title": "Appraisal Report",
            "description": "Professional property appraisal",
            "document_type": "appraisal",
            "file_url": "https://docs.example.com/appraisal.pdf"
        }
    ]
    
    created_documents = []
    
    for doc_data in documents_to_create:
        try:
            document = client.property_documents.create_property_document(property_id, doc_data)
            created_documents.append(document)
            print(f"Added document: {document['title']}")
        except ValidationError as e:
            print(f"Failed to add document '{doc_data['title']}': {e}")
    
    return created_documents

def track_property_communications(property_id: int):
    """Track all communications related to a property."""
    
    # Add email records
    emails = [
        {
            "subject": "Property Showing Scheduled",
            "body": "Your property showing is scheduled for tomorrow at 2 PM.",
            "to_email": "client@example.com",
            "from_email": "agent@realty.com",
            "sent_date": "2024-01-15T10:00:00Z"
        },
        {
            "subject": "Offer Received",
            "body": "We have received an offer on your property. Please review the attached documents.",
            "to_email": "seller@example.com",
            "from_email": "agent@realty.com",
            "sent_date": "2024-01-16T14:30:00Z"
        }
    ]
    
    for email_data in emails:
        try:
            email = client.property_emails.create_property_email(property_id, email_data)
            print(f"Logged email: {email['subject']}")
        except ValidationError as e:
            print(f"Failed to log email: {e}")
    
    # Add notes
    notes = [
        {
            "title": "Showing Feedback",
            "content": "Buyers were very interested, especially in the kitchen renovation.",
            "note_type": "showing"
        },
        {
            "title": "Price Adjustment",
            "content": "Reduced listing price by $10,000 based on market analysis.",
            "note_type": "pricing"
        }
    ]
    
    for note_data in notes:
        try:
            note = client.property_notes.create_property_note(property_id, note_data)
            print(f"Added note: {note['title']}")
        except ValidationError as e:
            print(f"Failed to add note: {e}")

def manage_property_tasks(property_id: int):
    """Create and manage tasks for property workflow."""
    
    tasks = [
        {
            "title": "Schedule Professional Photography",
            "description": "Arrange for high-quality listing photos",
            "due_date": "2024-01-20",
            "priority": "high",
            "assigned_to": "marketing_team"
        },
        {
            "title": "Order Home Inspection",
            "description": "Schedule comprehensive home inspection",
            "due_date": "2024-01-25",
            "priority": "medium",
            "assigned_to": "transaction_coordinator"
        },
        {
            "title": "Prepare Listing Materials",
            "description": "Create MLS listing and marketing materials",
            "due_date": "2024-01-22",
            "priority": "high",
            "assigned_to": "listing_agent"
        }
    ]
    
    for task_data in tasks:
        try:
            task = client.property_tasks.create_property_task(property_id, task_data)
            print(f"Created task: {task['title']} (Due: {task['due_date']})")
        except ValidationError as e:
            print(f"Failed to create task: {e}")
```

## Error Handling Patterns

### Robust Error Handling

```python
from open_to_close_api import (
    OpenToCloseAPIError,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    NetworkError
)
import time

def robust_api_call_with_retry(func, *args, max_retries=3, **kwargs):
    """Execute API call with retry logic for transient errors."""
    
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
            
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limit hit, waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            raise
            
        except NetworkError as e:
            if attempt < max_retries - 1:
                wait_time = 1
                print(f"Network error, retrying in {wait_time} second...")
                time.sleep(wait_time)
                continue
            raise
            
        except ServerError as e:
            if attempt < max_retries - 1 and e.status_code >= 500:
                wait_time = 2 ** attempt
                print(f"Server error, retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            raise
            
        except (AuthenticationError, ValidationError, NotFoundError):
            # Don't retry these errors
            raise
            
    return None

def safe_contact_operations():
    """Demonstrate safe contact operations with comprehensive error handling."""
    
    # Safe contact creation
    def create_contact_safely(contact_data):
        try:
            return robust_api_call_with_retry(
                client.contacts.create_contact, 
                contact_data
            )
        except AuthenticationError:
            print("Authentication failed. Check your API key.")
            return None
        except ValidationError as e:
            print(f"Invalid contact data: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error creating contact: {e}")
            return None
    
    # Safe contact retrieval
    def get_contact_safely(contact_id):
        try:
            return robust_api_call_with_retry(
                client.contacts.retrieve_contact, 
                contact_id
            )
        except NotFoundError:
            print(f"Contact {contact_id} does not exist")
            return None
        except Exception as e:
            print(f"Error retrieving contact {contact_id}: {e}")
            return None
    
    # Example usage
    contact_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com"
    }
    
    contact = create_contact_safely(contact_data)
    if contact:
        retrieved_contact = get_contact_safely(contact['id'])
        return retrieved_contact
    
    return None
```

## Bulk Operations

### Efficient Bulk Data Management

```python
def bulk_import_contacts(contacts_data: list):
    """Import multiple contacts with progress tracking and error handling."""
    
    successful_imports = []
    failed_imports = []
    
    total_contacts = len(contacts_data)
    
    for i, contact_data in enumerate(contacts_data, 1):
        try:
            contact = client.contacts.create_contact(contact_data)
            successful_imports.append(contact)
            print(f"Progress: {i}/{total_contacts} - Created: {contact['first_name']} {contact['last_name']}")
            
        except ValidationError as e:
            failed_imports.append({
                "data": contact_data,
                "error": str(e)
            })
            print(f"Progress: {i}/{total_contacts} - Failed: {contact_data.get('email', 'Unknown')} - {e}")
        
        except RateLimitError:
            print("Rate limit hit, waiting...")
            time.sleep(5)
            # Retry this contact
            try:
                contact = client.contacts.create_contact(contact_data)
                successful_imports.append(contact)
                print(f"Progress: {i}/{total_contacts} - Created (retry): {contact['first_name']} {contact['last_name']}")
            except Exception as retry_error:
                failed_imports.append({
                    "data": contact_data,
                    "error": str(retry_error)
                })
    
    print(f"\nBulk import completed:")
    print(f"  Successful: {len(successful_imports)}")
    print(f"  Failed: {len(failed_imports)}")
    
    if failed_imports:
        print("\nFailed imports:")
        for failure in failed_imports:
            print(f"  {failure['data'].get('email', 'Unknown')}: {failure['error']}")
    
    return successful_imports, failed_imports

def export_all_properties():
    """Export all properties with pagination."""
    
    all_properties = []
    page_size = 100
    offset = 0
    
    while True:
        try:
            properties = client.properties.list_properties(params={
                "limit": page_size,
                "offset": offset
            })
            
            if not properties:
                break
                
            all_properties.extend(properties)
            print(f"Fetched {len(properties)} properties (Total: {len(all_properties)})")
            
            if len(properties) < page_size:
                break
                
            offset += page_size
            
        except Exception as e:
            print(f"Error fetching properties at offset {offset}: {e}")
            break
    
    print(f"Export completed: {len(all_properties)} total properties")
    return all_properties
```

## Real Estate Workflow Examples

### Complete Transaction Workflow

```python
def complete_listing_workflow():
    """Demonstrate a complete property listing workflow."""
    
    # 1. Create the property listing
    property_data = {
        "address": "789 Elm Street",
        "city": "Beverly Hills",
        "state": "CA",
        "zip_code": "90210",
        "property_type": "single_family",
        "bedrooms": 5,
        "bathrooms": 4,
        "square_feet": 3200,
        "listing_price": 1250000,
        "status": "coming_soon"
    }
    
    try:
        property = client.properties.create_property(property_data)
        property_id = property['id']
        print(f"✓ Created property listing: {property['address']}")
    except Exception as e:
        print(f"✗ Failed to create property: {e}")
        return None
    
    # 2. Add the listing agent and team
    try:
        # Associate contacts with the property
        agent_contact = client.property_contacts.create_property_contact(property_id, {
            "contact_id": 123,  # Assuming existing agent contact
            "relationship_type": "listing_agent"
        })
        print("✓ Associated listing agent")
    except Exception as e:
        print(f"✗ Failed to associate agent: {e}")
    
    # 3. Create initial tasks
    initial_tasks = [
        {
            "title": "Property Preparation",
            "description": "Clean, stage, and prepare property for photos",
            "due_date": "2024-02-01",
            "priority": "high"
        },
        {
            "title": "Professional Photography",
            "description": "Schedule and complete professional photos",
            "due_date": "2024-02-03",
            "priority": "high"
        },
        {
            "title": "MLS Entry",
            "description": "Enter property into MLS system",
            "due_date": "2024-02-05",
            "priority": "medium"
        }
    ]
    
    for task_data in initial_tasks:
        try:
            task = client.property_tasks.create_property_task(property_id, task_data)
            print(f"✓ Created task: {task['title']}")
        except Exception as e:
            print(f"✗ Failed to create task: {e}")
    
    # 4. Add initial documentation
    try:
        listing_agreement = client.property_documents.create_property_document(property_id, {
            "title": "Listing Agreement",
            "description": "Signed listing agreement with seller",
            "document_type": "contract"
        })
        print("✓ Added listing agreement document")
    except Exception as e:
        print(f"✗ Failed to add document: {e}")
    
    # 5. Create initial notes
    try:
        initial_note = client.property_notes.create_property_note(property_id, {
            "title": "Listing Strategy",
            "content": "Luxury market positioning, emphasis on location and recent renovations",
            "note_type": "strategy"
        })
        print("✓ Added initial strategy notes")
    except Exception as e:
        print(f"✗ Failed to add note: {e}")
    
    print(f"\n🏠 Property listing workflow completed for: {property['address']}")
    return property_id

def buyer_inquiry_workflow(property_id: int, buyer_contact_id: int):
    """Handle a buyer inquiry and showing request."""
    
    # 1. Log the inquiry email
    try:
        inquiry_email = client.property_emails.create_property_email(property_id, {
            "subject": "Showing Request",
            "body": "Interested buyer would like to schedule a showing this weekend",
            "to_email": "agent@realty.com",
            "from_email": "buyer@example.com"
        })
        print("✓ Logged buyer inquiry email")
    except Exception as e:
        print(f"✗ Failed to log email: {e}")
    
    # 2. Associate buyer with property
    try:
        buyer_association = client.property_contacts.create_property_contact(property_id, {
            "contact_id": buyer_contact_id,
            "relationship_type": "potential_buyer"
        })
        print("✓ Associated buyer with property")
    except Exception as e:
        print(f"✗ Failed to associate buyer: {e}")
    
    # 3. Create showing task
    try:
        showing_task = client.property_tasks.create_property_task(property_id, {
            "title": "Schedule Property Showing",
            "description": f"Coordinate showing with buyer (Contact ID: {buyer_contact_id})",
            "due_date": "2024-02-10",
            "priority": "high"
        })
        print("✓ Created showing task")
    except Exception as e:
        print(f"✗ Failed to create task: {e}")
    
    # 4. Add buyer interest note
    try:
        interest_note = client.property_notes.create_property_note(property_id, {
            "title": "Buyer Interest",
            "content": f"Buyer (Contact ID: {buyer_contact_id}) expressed strong interest, requesting weekend showing",
            "note_type": "buyer_activity"
        })
        print("✓ Added buyer interest note")
    except Exception as e:
        print(f"✗ Failed to add note: {e}")
    
    print("👥 Buyer inquiry workflow completed")

# Example usage
if __name__ == "__main__":
    # Complete workflow example
    property_id = complete_listing_workflow()
    if property_id:
        buyer_inquiry_workflow(property_id, 456)  # Assuming buyer contact ID 456
```

## Advanced Filtering and Search

### Complex Query Examples

```python
def advanced_property_search():
    """Demonstrate advanced property search capabilities."""
    
    # Search for luxury properties
    luxury_params = {
        "listing_price__gte": 1000000,
        "square_feet__gte": 3000,
        "bedrooms__gte": 4,
        "property_type": "single_family",
        "status": "active"
    }
    
    luxury_properties = client.properties.list_properties(params=luxury_params)
    print(f"Found {len(luxury_properties)} luxury properties")
    
    # Search by location and price range
    location_params = {
        "city__in": "Beverly Hills,Malibu,Santa Monica",
        "listing_price__range": "500000,2000000",
        "status": "active"
    }
    
    location_properties = client.properties.list_properties(params=location_params)
    print(f"Found {len(location_properties)} properties in target locations")
    
    # Search contacts by criteria
    contact_params = {
        "email__contains": "@gmail.com",
        "created_date__gte": "2024-01-01",
        "tags__contains": "first_time_buyer"
    }
    
    filtered_contacts = client.contacts.list_contacts(params=contact_params)
    print(f"Found {len(filtered_contacts)} Gmail contacts created this year")

def generate_market_report():
    """Generate a comprehensive market report."""
    
    # Get active listings by price range
    price_ranges = [
        (0, 500000),
        (500000, 750000),
        (750000, 1000000),
        (1000000, float('inf'))
    ]
    
    report = {}
    
    for min_price, max_price in price_ranges:
        params = {
            "status": "active",
            "listing_price__gte": min_price
        }
        
        if max_price != float('inf'):
            params["listing_price__lt"] = max_price
            range_name = f"${min_price:,} - ${max_price:,}"
        else:
            range_name = f"${min_price:,}+"
        
        try:
            properties = client.properties.list_properties(params=params)
            report[range_name] = {
                "count": len(properties),
                "properties": properties
            }
            print(f"{range_name}: {len(properties)} active listings")
        except Exception as e:
            print(f"Error fetching {range_name}: {e}")
    
    return report
```

These examples demonstrate the full capabilities of the Open To Close API client, from basic operations to complex real estate workflows. Use these patterns as templates for your own implementations. 