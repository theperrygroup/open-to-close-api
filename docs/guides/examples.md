# Comprehensive Examples

Real-world usage examples and implementation patterns for the Open To Close API client with production-ready code and best practices.

!!! info "🎯 What You'll Learn"
    These examples showcase complete workflows, error handling patterns, and advanced techniques used in production real estate applications.

## 🚀 Quick Navigation

<div class="grid cards" markdown>

-   :material-account:{ .lg .middle } **Basic Operations**

    ---

    Essential CRUD operations for contacts, properties, and agents

    [:octicons-arrow-right-24: CRUD Examples](#basic-crud-operations)

-   :material-home:{ .lg .middle } **Property Management**

    ---

    Complete property lifecycle from listing to closing

    [:octicons-arrow-right-24: Property Examples](#working-with-properties)

-   :material-file-document:{ .lg .middle } **Relationships**

    ---

    Managing documents, emails, notes, and tasks

    [:octicons-arrow-right-24: Relationship Examples](#managing-property-relationships)

-   :material-shield:{ .lg .middle } **Error Handling**

    ---

    Production-ready error handling and retry patterns

    [:octicons-arrow-right-24: Error Examples](#error-handling-patterns)

-   :material-database:{ .lg .middle } **Bulk Operations**

    ---

    Efficient bulk data import/export with progress tracking

    [:octicons-arrow-right-24: Bulk Examples](#bulk-operations)

-   :material-chart-line:{ .lg .middle } **Real Estate Workflows**

    ---

    Complete transaction workflows and market analysis

    [:octicons-arrow-right-24: Workflow Examples](#real-estate-workflow-examples)

</div>

## 📋 Basic CRUD Operations

Master the fundamental create, read, update, and delete operations with comprehensive error handling.

!!! success "✅ What's Covered"
    - Complete contact lifecycle management
    - Property and agent operations
    - Error handling best practices
    - Real-world usage patterns

### 👥 Complete Contact Management

!!! example "Contact Lifecycle Examples"

=== "Create Contact"
    ```python
    from open_to_close import OpenToCloseAPI, NotFoundError, ValidationError

    client = OpenToCloseAPI()

    def create_contact_example():
        """Create a new contact with comprehensive data."""
        contact_data = {
            "first_name": "Sarah",
            "last_name": "Johnson", 
            "email": "sarah.johnson@example.com",
            "phone": "+1555123456",
            "contact_type": "buyer",
            "budget_min": 400000,
            "budget_max": 600000,
            "notes": "Potential first-time buyer, pre-approved"
        }
        
        try:
            contact = client.contacts.create_contact(contact_data)
            print(f"✅ Created contact: {contact['first_name']} {contact['last_name']}")
            print(f"   ID: {contact['id']}")
            print(f"   Type: {contact['contact_type']}")
            return contact
        except ValidationError as e:
            print(f"❌ Invalid contact data: {e}")
            return None
    ```

=== "Update Contact"
    ```python
    def update_contact_example(contact_id: int):
        """Update existing contact information."""
        
        # Partial update with new information
        updates = {
            "phone": "+1555987654",
            "budget_max": 650000,
            "notes": "Approved for mortgage pre-qualification - $625k max",
            "preferred_areas": ["Downtown", "Midtown", "Suburbs"]
        }
        
        try:
            updated_contact = client.contacts.update_contact(contact_id, updates)
            print(f"✅ Updated contact {contact_id}")
            print(f"   New budget: ${updates['budget_max']:,}")
            print(f"   Preferred areas: {', '.join(updates['preferred_areas'])}")
            return updated_contact
        except NotFoundError:
            print(f"❌ Contact {contact_id} not found")
        except ValidationError as e:
            print(f"❌ Invalid update data: {e}")
        return None
    ```

=== "Retrieve & Display"
    ```python
    def get_contact_details(contact_id: int):
        """Retrieve and display complete contact information."""
        
        try:
            contact = client.contacts.retrieve_contact(contact_id)
            
            print(f"📋 Contact Details (ID: {contact['id']})")
            print(f"   Name: {contact['first_name']} {contact['last_name']}")
            print(f"   Email: {contact['email']}")
            print(f"   Phone: {contact.get('phone', 'Not provided')}")
            print(f"   Type: {contact.get('contact_type', 'Not specified')}")
            
            if contact.get('budget_min') and contact.get('budget_max'):
                print(f"   Budget: ${contact['budget_min']:,} - ${contact['budget_max']:,}")
            
            if contact.get('preferred_areas'):
                print(f"   Preferred Areas: {', '.join(contact['preferred_areas'])}")
                
            return contact
        except NotFoundError:
            print(f"❌ Contact {contact_id} not found")
            return None
    ```

=== "Complete Example"
    ```python
    def contact_management_demo():
        """Complete contact management workflow."""
        
        # Create a new contact
        contact = create_contact_example()
        if not contact:
            return
        
        contact_id = contact['id']
        
        # Retrieve initial details
        print("\n🔍 Initial Contact Details:")
        get_contact_details(contact_id)
        
        # Update the contact
        print("\n✏️ Updating Contact:")
        update_contact_example(contact_id)
        
        # Retrieve updated details
        print("\n🔍 Updated Contact Details:")
        updated_contact = get_contact_details(contact_id)
        
        print(f"\n🎉 Contact management demo completed!")
        return updated_contact

    # Run the demo
    if __name__ == "__main__":
        contact_management_demo()
    ```

!!! tip "💡 Best Practices"
    - Always handle `ValidationError` for data issues
    - Use `NotFoundError` to handle missing resources
    - Include meaningful contact types and budget information
    - Store notes for future reference and context

## 🏠 Working with Properties

Complete property lifecycle management from listing creation to status updates and advanced search capabilities.

!!! success "✅ Property Operations"
    - Create comprehensive property listings
    - Update property status throughout lifecycle
    - Advanced search and filtering
    - Market analysis and reporting

### 🏡 Property Lifecycle Management

!!! example "Property Management Examples"

=== "Create Listing"
    ```python
    def create_property_listing():
        """Create a new property listing with comprehensive information."""
        
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
            "description": "Beautiful family home in desirable neighborhood",
            "features": ["hardwood floors", "granite counters", "two-car garage"],
            "year_built": 2010,
            "listing_date": "2024-01-15"
        }
        
        try:
            property_obj = client.properties.create_property(property_data)
            print(f"✅ Created property listing:")
            print(f"   Address: {property_obj['address']}")
            print(f"   ID: {property_obj['id']}")
            print(f"   Price: ${property_obj['listing_price']:,}")
            print(f"   Features: {len(property_data['features'])} highlighted features")
            return property_obj
        except ValidationError as e:
            print(f"❌ Invalid property data: {e}")
            return None
    ```

=== "Update Status"
    ```python
    def update_property_status(property_id: int, new_status: str, notes: str = None):
        """Update property status with optional notes."""
        
        update_data = {"status": new_status}
        
        if notes:
            # Append status change note
            update_data["status_notes"] = notes
        
        try:
            updated_property = client.properties.update_property(property_id, update_data)
            print(f"✅ Property {property_id} status updated:")
            print(f"   New Status: {new_status}")
            print(f"   Address: {updated_property['address']}")
            
            if notes:
                print(f"   Notes: {notes}")
                
            return updated_property
        except NotFoundError:
            print(f"❌ Property {property_id} not found")
        except ValidationError as e:
            print(f"❌ Invalid status '{new_status}': {e}")
        return None
    ```

=== "Advanced Search"
    ```python
    def search_properties_by_criteria():
        """Search for properties with detailed filtering."""
        
        search_params = {
            "city": "Springfield",
            "min_price": 500000,
            "max_price": 800000,
            "bedrooms__gte": 3,  # 3 or more bedrooms
            "bathrooms__gte": 2,  # 2 or more bathrooms
            "property_type": "single_family",
            "status": "active",
            "square_feet__gte": 2000  # Minimum 2000 sq ft
        }
        
        try:
            properties = client.properties.list_properties(params=search_params)
            print(f"🔍 Found {len(properties)} properties matching criteria:")
            print(f"   Location: {search_params['city']}")
            print(f"   Price Range: ${search_params['min_price']:,} - ${search_params['max_price']:,}")
            print(f"   Min Bedrooms: {search_params['bedrooms__gte']}")
            print(f"   Min Square Feet: {search_params['square_feet__gte']:,}")
            print()
            
            for i, prop in enumerate(properties, 1):
                print(f"{i}. 📍 {prop['address']}")
                print(f"   💰 ${prop['listing_price']:,}")
                print(f"   🏠 {prop['bedrooms']}br/{prop['bathrooms']}ba • {prop['square_feet']:,} sq ft")
                print(f"   📅 Listed: {prop.get('listing_date', 'N/A')}")
                print()
                
            return properties
        except Exception as e:
            print(f"❌ Error searching properties: {e}")
            return []
    ```

=== "Price Analysis"
    ```python
    def analyze_property_pricing(property_id: int):
        """Analyze property pricing compared to market."""
        
        try:
            # Get the property details
            property_obj = client.properties.retrieve_property(property_id)
            
            # Search for comparable properties
            comp_params = {
                "city": property_obj['city'],
                "property_type": property_obj['property_type'],
                "bedrooms": property_obj['bedrooms'],
                "bathrooms": property_obj['bathrooms'],
                "square_feet__gte": property_obj['square_feet'] * 0.8,  # 80% of size
                "square_feet__lte": property_obj['square_feet'] * 1.2,  # 120% of size
                "status__in": ["active", "pending", "sold"],
                "limit": 10
            }
            
            comparables = client.properties.list_properties(params=comp_params)
            
            if comparables:
                prices = [comp['listing_price'] for comp in comparables if comp['listing_price']]
                avg_price = sum(prices) / len(prices) if prices else 0
                
                print(f"📊 Price Analysis for {property_obj['address']}")
                print(f"   Current Price: ${property_obj['listing_price']:,}")
                print(f"   Market Average: ${avg_price:,.0f}")
                print(f"   Difference: ${property_obj['listing_price'] - avg_price:+,.0f}")
                print(f"   Comparables Found: {len(comparables)}")
                
                percentage_diff = ((property_obj['listing_price'] - avg_price) / avg_price) * 100
                print(f"   % vs Market: {percentage_diff:+.1f}%")
                
                if percentage_diff > 10:
                    print("   💡 Suggestion: Property may be overpriced")
                elif percentage_diff < -10:
                    print("   💡 Suggestion: Property may be underpriced")
                else:
                    print("   ✅ Pricing appears competitive")
                
            return {
                "property": property_obj,
                "comparables": comparables,
                "analysis": {
                    "current_price": property_obj['listing_price'],
                    "market_average": avg_price,
                    "difference": property_obj['listing_price'] - avg_price,
                    "percentage_difference": percentage_diff
                }
            }
            
        except NotFoundError:
            print(f"❌ Property {property_id} not found")
        except Exception as e:
            print(f"❌ Error analyzing property: {e}")
        return None
    ```

=== "Complete Workflow"
    ```python
    def property_management_workflow():
        """Complete property management demonstration."""
        
        print("🏠 Property Management Workflow Demo")
        print("=" * 40)
        
        # 1. Create a new listing
        print("\n1️⃣ Creating New Property Listing:")
        property_obj = create_property_listing()
        if not property_obj:
            return
        
        property_id = property_obj['id']
        
        # 2. Perform market analysis
        print("\n2️⃣ Market Analysis:")
        analysis = analyze_property_pricing(property_id)
        
        # 3. Search for similar properties
        print("\n3️⃣ Finding Comparable Properties:")
        search_properties_by_criteria()
        
        # 4. Update property status
        print("\n4️⃣ Updating Property Status:")
        update_property_status(
            property_id, 
            "pending", 
            "Received offer above asking price"
        )
        
        print("\n🎉 Property management workflow completed!")
        return property_obj

    # Run the demo
    if __name__ == "__main__":
        property_management_workflow()
    ```

!!! tip "💡 Property Best Practices"
    - Include comprehensive property details for better search results
    - Update status regularly to track progress
    - Use comparable properties for pricing guidance  
    - Store detailed notes for status changes
    - Regular market analysis helps with pricing decisions

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

## 📋 What's Next?

These comprehensive examples showcase the full power of the Open To Close API client. Choose your next step:

<div class="grid cards" markdown>

-   :material-rocket:{ .lg .middle } **Quick Start**

    ---

    New to the API? Start with our 5-minute tutorial

    [:octicons-arrow-right-24: Quick Start Guide](../getting-started/quickstart.md)

-   :material-api:{ .lg .middle } **API Reference**

    ---

    Complete technical documentation for all methods

    [:octicons-arrow-right-24: API Documentation](../reference/api-reference.md)

-   :material-wrench:{ .lg .middle } **Troubleshooting**

    ---

    Common issues, solutions, and debugging techniques

    [:octicons-arrow-right-24: Get Help](troubleshooting.md)

-   :material-github:{ .lg .middle } **Contributing**

    ---

    Help improve the client with your contributions

    [:octicons-arrow-right-24: Contribute](../development/contributing.md)

</div>

!!! success "🎯 Examples Mastery Complete!"
    You now have comprehensive, production-ready examples for:
    
    - ✅ Complete CRUD operations with error handling
    - ✅ Advanced property management workflows
    - ✅ Bulk operations with progress tracking
    - ✅ Real estate transaction workflows
    - ✅ Market analysis and reporting patterns
    
    **Ready to build?** Use these patterns as templates for your own implementations. All examples include comprehensive error handling and follow production best practices. 