# Examples

This guide provides practical examples of using the Open To Close API Python client for common real estate workflows. Each example includes complete, runnable code with explanations.

## Getting Started

All examples assume you have the client installed and configured:

```python
from open_to_close import OpenToCloseAPI

# Initialize the client (API key from environment or config)
client = OpenToCloseAPI()
```

---

## Property Management Examples

### Creating and Managing a New Property Listing

```python
from open_to_close import OpenToCloseAPI
from open_to_close.exceptions import ValidationError, NotFoundError

client = OpenToCloseAPI()

# 1. Create a new property
property_data = {
    "address": "123 Main Street",
    "city": "San Francisco",
    "state": "CA",
    "zip_code": "94102",
    "property_type": "single_family",
    "bedrooms": 3,
    "bathrooms": 2,
    "square_feet": 1800,
    "lot_size": 0.25,
    "year_built": 1995,
    "listing_price": 850000,
    "status": "active"
}

try:
    property_obj = client.properties.create_property(property_data)
    property_id = property_obj['id']
    print(f"Created property {property_id}: {property_obj['address']}")
    
    # 2. Add property notes
    initial_note = client.property_notes.create_property_note(property_id, {
        "content": "Beautiful Victorian home with original hardwood floors and updated kitchen. Great location near parks and schools.",
        "author": "Listing Agent",
        "priority": "medium",
        "tags": ["listing", "features"],
        "category": "marketing"
    })
    
    # 3. Create marketing tasks
    marketing_tasks = [
        {
            "title": "Professional Photography",
            "description": "Schedule professional photographer for high-quality listing photos",
            "priority": "high",
            "due_date": "2024-02-01",
            "category": "marketing",
            "assignee": "Photography Team"
        },
        {
            "title": "Create Virtual Tour",
            "description": "Create 3D virtual tour for online listing",
            "priority": "medium",
            "due_date": "2024-02-03",
            "category": "marketing",
            "assignee": "Marketing Team"
        },
        {
            "title": "Write Property Description",
            "description": "Create compelling property description highlighting key features",
            "priority": "medium",
            "due_date": "2024-02-02",
            "category": "marketing",
            "assignee": "Marketing Team"
        }
    ]
    
    for task_data in marketing_tasks:
        task = client.property_tasks.create_property_task(property_id, task_data)
        print(f"Created task: {task['title']}")
    
    # 4. Upload property documents
    documents = [
        {
            "name": "Property Disclosure",
            "type": "legal",
            "url": "https://example.com/docs/disclosure.pdf",
            "description": "Seller property disclosure statement"
        },
        {
            "name": "Floor Plan",
            "type": "marketing",
            "url": "https://example.com/docs/floorplan.pdf",
            "description": "Architectural floor plan"
        }
    ]
    
    for doc_data in documents:
        document = client.property_documents.create_property_document(property_id, doc_data)
        print(f"Uploaded document: {document['name']}")
    
    print(f"\nProperty listing setup complete for {property_obj['address']}")
    
except ValidationError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"Error creating property: {e}")
```

### Property Search and Filtering

```python
# Search for properties by various criteria
def search_properties_example():
    client = OpenToCloseAPI()
    
    # 1. Search by location
    sf_properties = client.properties.list_properties(params={
        "city": "San Francisco",
        "state": "CA"
    })
    print(f"Found {len(sf_properties)} properties in San Francisco")
    
    # 2. Search by price range
    affordable_properties = client.properties.list_properties(params={
        "min_price": 500000,
        "max_price": 800000,
        "status": "active"
    })
    print(f"Found {len(affordable_properties)} properties in price range")
    
    # 3. Search by property features
    family_homes = client.properties.list_properties(params={
        "bedrooms__gte": 3,
        "bathrooms__gte": 2,
        "property_type": "single_family"
    })
    print(f"Found {len(family_homes)} family homes")
    
    # 4. Get property details with related data
    for prop in sf_properties[:3]:  # First 3 properties
        property_id = prop['id']
        
        # Get property notes
        notes = client.property_notes.list_property_notes(property_id)
        
        # Get property tasks
        tasks = client.property_tasks.list_property_tasks(property_id)
        
        # Get property documents
        documents = client.property_documents.list_property_documents(property_id)
        
        print(f"\nProperty: {prop['address']}")
        print(f"  Notes: {len(notes)}")
        print(f"  Tasks: {len(tasks)}")
        print(f"  Documents: {len(documents)}")

search_properties_example()
```

---

## Client and Contact Management

### Managing Client Relationships

```python
def client_management_example():
    client = OpenToCloseAPI()
    
    # 1. Create a new contact (buyer)
    buyer_data = {
        "first_name": "John",
        "last_name": "Smith",
        "email": "john.smith@email.com",
        "phone": "(555) 123-4567",
        "contact_type": "buyer",
        "status": "active",
        "notes": "First-time homebuyer, pre-approved for $600k"
    }
    
    buyer = client.contacts.create_contact(buyer_data)
    buyer_id = buyer['id']
    print(f"Created buyer contact: {buyer['first_name']} {buyer['last_name']}")
    
    # 2. Find properties matching buyer criteria
    matching_properties = client.properties.list_properties(params={
        "max_price": 600000,
        "bedrooms__gte": 2,
        "status": "active"
    })
    
    print(f"Found {len(matching_properties)} properties matching buyer criteria")
    
    # 3. Associate buyer with interested properties
    for prop in matching_properties[:3]:  # First 3 matches
        property_id = prop['id']
        
        # Create property contact relationship
        property_contact = client.property_contacts.create_property_contact(property_id, {
            "contact_id": buyer_id,
            "relationship_type": "interested_buyer",
            "notes": "Matches buyer criteria, scheduled for showing"
        })
        
        # Add note about buyer interest
        client.property_notes.create_property_note(property_id, {
            "content": f"Buyer {buyer['first_name']} {buyer['last_name']} expressed interest. Pre-approved for $600k.",
            "author": "Agent",
            "priority": "medium",
            "tags": ["buyer-interest", "showing"],
            "category": "client-interaction"
        })
        
        # Create showing task
        client.property_tasks.create_property_task(property_id, {
            "title": f"Schedule showing for {buyer['first_name']} {buyer['last_name']}",
            "description": f"Coordinate property showing with buyer. Contact: {buyer['phone']}",
            "priority": "high",
            "due_date": "2024-02-05",
            "category": "showing",
            "tags": ["showing", "buyer"]
        })
        
        print(f"Associated buyer with property: {prop['address']}")

client_management_example()
```

### Team Collaboration Workflow

```python
def team_collaboration_example():
    client = OpenToCloseAPI()
    
    # 1. Get team information
    teams = client.teams.list_teams()
    if teams:
        team = teams[0]  # Use first team
        team_id = team['id']
        print(f"Working with team: {team['name']}")
        
        # Get team members
        team_users = client.users.list_users(params={"team_id": team_id})
        print(f"Team has {len(team_users)} members")
    
    # 2. Assign tasks to team members
    property_id = 123  # Example property ID
    
    # Create tasks for different team roles
    team_tasks = [
        {
            "title": "Market Analysis",
            "description": "Prepare comparative market analysis for pricing strategy",
            "assignee": "Market Analyst",
            "priority": "high",
            "due_date": "2024-02-03",
            "category": "analysis"
        },
        {
            "title": "Legal Review",
            "description": "Review property documents and contracts",
            "assignee": "Legal Team",
            "priority": "high",
            "due_date": "2024-02-04",
            "category": "legal"
        },
        {
            "title": "Marketing Campaign",
            "description": "Launch marketing campaign across all channels",
            "assignee": "Marketing Team",
            "priority": "medium",
            "due_date": "2024-02-06",
            "category": "marketing"
        }
    ]
    
    for task_data in team_tasks:
        task = client.property_tasks.create_property_task(property_id, task_data)
        print(f"Assigned task '{task['title']}' to {task['assignee']}")
    
    # 3. Track team progress
    all_tasks = client.property_tasks.list_property_tasks(property_id)
    
    # Group tasks by assignee
    tasks_by_assignee = {}
    for task in all_tasks:
        assignee = task.get('assignee', 'Unassigned')
        if assignee not in tasks_by_assignee:
            tasks_by_assignee[assignee] = []
        tasks_by_assignee[assignee].append(task)
    
    print("\nTeam workload summary:")
    for assignee, tasks in tasks_by_assignee.items():
        pending_count = len([t for t in tasks if t['status'] == 'pending'])
        completed_count = len([t for t in tasks if t['status'] == 'completed'])
        print(f"  {assignee}: {pending_count} pending, {completed_count} completed")

team_collaboration_example()
```

---

## Transaction Management

### Complete Property Sale Workflow

```python
def property_sale_workflow():
    client = OpenToCloseAPI()
    
    property_id = 123  # Example property ID
    
    # 1. Property goes under contract
    print("=== PROPERTY UNDER CONTRACT ===")
    
    # Update property status
    client.properties.update_property(property_id, {
        "status": "under_contract",
        "contract_date": "2024-01-15"
    })
    
    # Add contract note
    client.property_notes.create_property_note(property_id, {
        "content": "Property under contract. Buyer: John Smith. Contract price: $825,000. Closing date: February 15, 2024.",
        "author": "Listing Agent",
        "priority": "high",
        "tags": ["contract", "under-contract"],
        "category": "offer"
    })
    
    # 2. Create closing timeline tasks
    closing_tasks = [
        {
            "title": "Order Home Inspection",
            "description": "Coordinate home inspection within 7 days of contract",
            "priority": "urgent",
            "due_date": "2024-01-22",
            "category": "inspection"
        },
        {
            "title": "Order Appraisal",
            "description": "Order property appraisal for buyer's lender",
            "priority": "high",
            "due_date": "2024-01-25",
            "category": "appraisal"
        },
        {
            "title": "Title Search",
            "description": "Order title search and title insurance",
            "priority": "high",
            "due_date": "2024-01-30",
            "category": "legal"
        },
        {
            "title": "Prepare Closing Documents",
            "description": "Prepare all closing documents and coordinate with title company",
            "priority": "medium",
            "due_date": "2024-02-10",
            "category": "closing"
        }
    ]
    
    for task_data in closing_tasks:
        task = client.property_tasks.create_property_task(property_id, task_data)
        print(f"Created closing task: {task['title']}")
    
    # 3. Track inspection process
    print("\n=== INSPECTION PHASE ===")
    
    # Mark inspection task as completed
    inspection_tasks = client.property_tasks.list_property_tasks(
        property_id, 
        params={"category": "inspection"}
    )
    
    if inspection_tasks:
        inspection_task = inspection_tasks[0]
        client.property_tasks.update_property_task(
            property_id, 
            inspection_task['id'],
            {
                "status": "completed",
                "notes": "Inspection completed. Minor issues identified."
            }
        )
    
    # Upload inspection report
    client.property_documents.create_property_document(property_id, {
        "name": "Home Inspection Report",
        "type": "inspection",
        "url": "https://example.com/docs/inspection_report.pdf",
        "description": "Professional home inspection report"
    })
    
    # Add inspection notes
    client.property_notes.create_property_note(property_id, {
        "content": "Home inspection completed. Minor issues: loose handrail, small roof leak. Seller agreed to repairs before closing.",
        "author": "Buyer's Agent",
        "priority": "medium",
        "tags": ["inspection", "repairs"],
        "category": "inspection"
    })
    
    # 4. Closing preparation
    print("\n=== CLOSING PREPARATION ===")
    
    # Update tasks as they're completed
    closing_task_updates = [
        ("Order Appraisal", "completed", "Appraisal ordered, scheduled for next week"),
        ("Title Search", "in_progress", "Title company processing search"),
        ("Prepare Closing Documents", "pending", "Waiting for final loan approval")
    ]
    
    all_tasks = client.property_tasks.list_property_tasks(property_id)
    
    for task_title, new_status, notes in closing_task_updates:
        matching_tasks = [t for t in all_tasks if task_title in t['title']]
        if matching_tasks:
            task = matching_tasks[0]
            client.property_tasks.update_property_task(
                property_id,
                task['id'],
                {
                    "status": new_status,
                    "notes": notes
                }
            )
            print(f"Updated task '{task_title}': {new_status}")
    
    # 5. Final closing
    print("\n=== CLOSING COMPLETED ===")
    
    # Update property to sold
    client.properties.update_property(property_id, {
        "status": "sold",
        "sale_date": "2024-02-15",
        "sale_price": 825000
    })
    
    # Add closing note
    client.property_notes.create_property_note(property_id, {
        "content": "Closing completed successfully! Final sale price: $825,000. Keys transferred to buyer.",
        "author": "Closing Agent",
        "priority": "high",
        "tags": ["closed", "sold"],
        "category": "closing"
    })
    
    # Mark all remaining tasks as completed
    pending_tasks = client.property_tasks.list_property_tasks(
        property_id,
        params={"status": "pending"}
    )
    
    for task in pending_tasks:
        client.property_tasks.update_property_task(
            property_id,
            task['id'],
            {"status": "completed"}
        )
    
    print("Property sale workflow completed!")

property_sale_workflow()
```

---

## Bulk Operations and Data Management

### Bulk Property Updates

```python
def bulk_property_operations():
    client = OpenToCloseAPI()
    
    # 1. Get all active properties
    active_properties = client.properties.list_properties(params={
        "status": "active"
    })
    
    print(f"Processing {len(active_properties)} active properties")
    
    # 2. Bulk update property tags
    for prop in active_properties:
        property_id = prop['id']
        
        # Add seasonal marketing tag
        existing_tags = prop.get('tags', [])
        if 'spring_2024' not in existing_tags:
            updated_tags = existing_tags + ['spring_2024']
            client.properties.update_property(property_id, {
                "tags": updated_tags
            })
    
    # 3. Generate marketing tasks for properties without recent activity
    from datetime import datetime, timedelta
    
    cutoff_date = datetime.now() - timedelta(days=30)
    
    for prop in active_properties:
        property_id = prop['id']
        
        # Check for recent marketing tasks
        recent_tasks = client.property_tasks.list_property_tasks(
            property_id,
            params={
                "category": "marketing",
                "created_after": cutoff_date.isoformat()
            }
        )
        
        if not recent_tasks:
            # Create marketing refresh task
            client.property_tasks.create_property_task(property_id, {
                "title": "Marketing Refresh",
                "description": "Review and refresh property marketing materials",
                "priority": "medium",
                "due_date": (datetime.now() + timedelta(days=7)).date().isoformat(),
                "category": "marketing",
                "tags": ["refresh", "spring_2024"]
            })
            print(f"Created marketing refresh task for {prop['address']}")
    
    # 4. Generate property performance report
    print("\n=== PROPERTY PERFORMANCE REPORT ===")
    
    performance_data = []
    
    for prop in active_properties:
        property_id = prop['id']
        
        # Get property metrics
        notes_count = len(client.property_notes.list_property_notes(property_id))
        tasks_count = len(client.property_tasks.list_property_tasks(property_id))
        docs_count = len(client.property_documents.list_property_documents(property_id))
        
        # Calculate days on market
        listing_date = prop.get('listing_date')
        if listing_date:
            days_on_market = (datetime.now().date() - 
                            datetime.fromisoformat(listing_date).date()).days
        else:
            days_on_market = 0
        
        performance_data.append({
            'address': prop['address'],
            'price': prop.get('listing_price', 0),
            'days_on_market': days_on_market,
            'notes': notes_count,
            'tasks': tasks_count,
            'documents': docs_count,
            'activity_score': notes_count + tasks_count + docs_count
        })
    
    # Sort by activity score
    performance_data.sort(key=lambda x: x['activity_score'], reverse=True)
    
    print("Top 5 most active properties:")
    for i, prop_data in enumerate(performance_data[:5], 1):
        print(f"{i}. {prop_data['address']}")
        print(f"   Price: ${prop_data['price']:,}")
        print(f"   Days on market: {prop_data['days_on_market']}")
        print(f"   Activity score: {prop_data['activity_score']}")
        print()

bulk_property_operations()
```

### Data Export and Reporting

```python
def generate_reports():
    client = OpenToCloseAPI()
    
    # 1. Property inventory report
    print("=== PROPERTY INVENTORY REPORT ===")
    
    all_properties = client.properties.list_properties()
    
    # Group by status
    status_counts = {}
    price_ranges = {"Under $500k": 0, "$500k-$750k": 0, "$750k-$1M": 0, "Over $1M": 0}
    
    for prop in all_properties:
        status = prop.get('status', 'unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
        
        price = prop.get('listing_price', 0)
        if price < 500000:
            price_ranges["Under $500k"] += 1
        elif price < 750000:
            price_ranges["$500k-$750k"] += 1
        elif price < 1000000:
            price_ranges["$750k-$1M"] += 1
        else:
            price_ranges["Over $1M"] += 1
    
    print("Properties by status:")
    for status, count in status_counts.items():
        print(f"  {status}: {count}")
    
    print("\nProperties by price range:")
    for range_name, count in price_ranges.items():
        print(f"  {range_name}: {count}")
    
    # 2. Team productivity report
    print("\n=== TEAM PRODUCTIVITY REPORT ===")
    
    # Get all tasks from last 30 days
    from datetime import datetime, timedelta
    
    cutoff_date = datetime.now() - timedelta(days=30)
    
    all_tasks = []
    for prop in all_properties[:10]:  # Sample first 10 properties
        tasks = client.property_tasks.list_property_tasks(prop['id'])
        all_tasks.extend(tasks)
    
    # Group by assignee
    assignee_stats = {}
    
    for task in all_tasks:
        assignee = task.get('assignee', 'Unassigned')
        if assignee not in assignee_stats:
            assignee_stats[assignee] = {
                'total': 0,
                'completed': 0,
                'pending': 0,
                'overdue': 0
            }
        
        assignee_stats[assignee]['total'] += 1
        
        if task['status'] == 'completed':
            assignee_stats[assignee]['completed'] += 1
        elif task['status'] == 'pending':
            assignee_stats[assignee]['pending'] += 1
            
            # Check if overdue
            due_date = task.get('due_date')
            if due_date and datetime.fromisoformat(due_date).date() < datetime.now().date():
                assignee_stats[assignee]['overdue'] += 1
    
    print("Team member productivity:")
    for assignee, stats in assignee_stats.items():
        if stats['total'] > 0:
            completion_rate = (stats['completed'] / stats['total']) * 100
            print(f"  {assignee}:")
            print(f"    Total tasks: {stats['total']}")
            print(f"    Completed: {stats['completed']} ({completion_rate:.1f}%)")
            print(f"    Pending: {stats['pending']}")
            print(f"    Overdue: {stats['overdue']}")
            print()
    
    # 3. Export data to CSV format (conceptual)
    print("=== DATA EXPORT ===")
    
    # Prepare CSV data
    csv_data = []
    csv_headers = ["Address", "City", "State", "Price", "Status", "Bedrooms", "Bathrooms", "Square Feet"]
    
    for prop in all_properties:
        row = [
            prop.get('address', ''),
            prop.get('city', ''),
            prop.get('state', ''),
            prop.get('listing_price', 0),
            prop.get('status', ''),
            prop.get('bedrooms', 0),
            prop.get('bathrooms', 0),
            prop.get('square_feet', 0)
        ]
        csv_data.append(row)
    
    print(f"Prepared {len(csv_data)} property records for export")
    print("CSV Headers:", ", ".join(csv_headers))
    print("Sample row:", csv_data[0] if csv_data else "No data")

generate_reports()
```

---

## Error Handling and Best Practices

### Robust Error Handling

```python
from open_to_close import OpenToCloseAPI
from open_to_close.exceptions import (
    NotFoundError, 
    ValidationError, 
    AuthenticationError,
    OpenToCloseAPIError
)
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def robust_api_operations():
    client = OpenToCloseAPI()
    
    def safe_api_call(operation, *args, **kwargs):
        """Wrapper for API calls with retry logic and error handling"""
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                return operation(*args, **kwargs)
            
            except AuthenticationError:
                logger.error("Authentication failed - check API key")
                raise
            
            except NotFoundError as e:
                logger.warning(f"Resource not found: {e}")
                return None
            
            except ValidationError as e:
                logger.error(f"Validation error: {e}")
                raise
            
            except OpenToCloseAPIError as e:
                if attempt < max_retries - 1:
                    logger.warning(f"API error (attempt {attempt + 1}): {e}. Retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    logger.error(f"API error after {max_retries} attempts: {e}")
                    raise
            
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise
    
    # Example: Safely create property with validation
    def create_property_safely(property_data):
        # Validate required fields
        required_fields = ['address', 'city', 'state']
        missing_fields = [field for field in required_fields if not property_data.get(field)]
        
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Clean and validate data
        cleaned_data = {}
        for key, value in property_data.items():
            if value is not None and value != '':
                cleaned_data[key] = value
        
        # Make API call with retry logic
        return safe_api_call(client.properties.create_property, cleaned_data)
    
    # Example usage
    property_data = {
        "address": "456 Oak Street",
        "city": "Los Angeles",
        "state": "CA",
        "zip_code": "90210",
        "listing_price": 750000
    }
    
    try:
        property_obj = create_property_safely(property_data)
        if property_obj:
            logger.info(f"Successfully created property: {property_obj['id']}")
        else:
            logger.warning("Property creation returned None")
    
    except Exception as e:
        logger.error(f"Failed to create property: {e}")
    
    # Example: Batch operations with error handling
    def batch_update_properties(property_updates):
        """Update multiple properties with individual error handling"""
        results = []
        
        for property_id, update_data in property_updates.items():
            try:
                updated_property = safe_api_call(
                    client.properties.update_property,
                    property_id,
                    update_data
                )
                
                if updated_property:
                    results.append({
                        'property_id': property_id,
                        'status': 'success',
                        'data': updated_property
                    })
                    logger.info(f"Updated property {property_id}")
                else:
                    results.append({
                        'property_id': property_id,
                        'status': 'not_found',
                        'error': 'Property not found'
                    })
            
            except Exception as e:
                results.append({
                    'property_id': property_id,
                    'status': 'error',
                    'error': str(e)
                })
                logger.error(f"Failed to update property {property_id}: {e}")
        
        return results
    
    # Example batch update
    updates = {
        123: {"status": "active"},
        124: {"listing_price": 650000},
        999: {"status": "sold"}  # This might not exist
    }
    
    results = batch_update_properties(updates)
    
    # Summary
    success_count = len([r for r in results if r['status'] == 'success'])
    error_count = len([r for r in results if r['status'] == 'error'])
    not_found_count = len([r for r in results if r['status'] == 'not_found'])
    
    logger.info(f"Batch update results: {success_count} success, {error_count} errors, {not_found_count} not found")

robust_api_operations()
```

---

## Integration Patterns

### Webhook Integration Example

```python
# Example webhook handler for property updates
from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)

@app.route('/webhook/property-update', methods=['POST'])
def handle_property_update():
    """Handle property update webhooks from Open To Close"""
    
    # Verify webhook signature (if configured)
    signature = request.headers.get('X-OTC-Signature')
    if signature:
        # Verify signature here
        pass
    
    data = request.json
    event_type = data.get('event_type')
    property_data = data.get('property')
    
    if event_type == 'property.status_changed':
        handle_property_status_change(property_data)
    elif event_type == 'property.price_changed':
        handle_property_price_change(property_data)
    
    return jsonify({'status': 'received'})

def handle_property_status_change(property_data):
    """Handle property status changes"""
    client = OpenToCloseAPI()
    
    property_id = property_data['id']
    new_status = property_data['status']
    
    # Add automated note
    client.property_notes.create_property_note(property_id, {
        "content": f"Property status automatically changed to {new_status}",
        "author": "System",
        "priority": "low",
        "tags": ["automated", "status-change"],
        "category": "system"
    })
    
    # Create follow-up tasks based on status
    if new_status == 'under_contract':
        # Create closing timeline tasks
        closing_tasks = [
            {
                "title": "Schedule Inspection",
                "description": "Coordinate property inspection",
                "priority": "urgent",
                "due_date": "2024-02-01",
                "category": "inspection"
            }
        ]
        
        for task_data in closing_tasks:
            client.property_tasks.create_property_task(property_id, task_data)

if __name__ == '__main__':
    app.run(debug=True)
```

This comprehensive examples guide demonstrates practical usage patterns for the Open To Close API, covering everything from basic property management to complex transaction workflows and integration patterns. Each example includes proper error handling and follows best practices for production use.

---

## Related Resources

- [API Reference](../api/index.md) - Complete API documentation
- [Error Handling Guide](error-handling.md) - Comprehensive error handling
- [Best Practices](best-practices.md) - Development best practices
- [Integration Patterns](integration-patterns.md) - Integration strategies