# Property Documents API

The Property Documents API allows you to manage documents associated with specific properties in the Open To Close platform. This includes uploading, retrieving, updating, and deleting documents such as contracts, photos, inspection reports, and other property-related files.

## Overview

Property documents are files attached to specific properties that help track important paperwork throughout the property lifecycle. Common document types include:

- Purchase agreements and contracts
- Property photos and virtual tours
- Inspection reports and disclosures
- Financial documents and appraisals
- Legal documents and permits

## Client Access

Access the Property Documents API through the main client:

```python
from open_to_close import OpenToCloseAPI

client = OpenToCloseAPI()
documents_api = client.property_documents
```

---

## Methods

### `list_property_documents(property_id, params=None)`

Retrieve a list of documents for a specific property.

**Parameters:**

- `property_id` (int): The ID of the property
- `params` (dict, optional): Query parameters for filtering

**Returns:** List of property document dictionaries

**Raises:**

- `OpenToCloseAPIError`: If the API request fails
- `NotFoundError`: If the property is not found
- `ValidationError`: If parameters are invalid
- `AuthenticationError`: If authentication fails

=== "Basic Usage"

    ```python
    # Get all documents for a property
    documents = client.property_documents.list_property_documents(123)
    
    for document in documents:
        print(f"Document: {document['name']} ({document['type']})")
    ```

=== "With Filtering"

    ```python
    # Get documents with filtering
    contracts = client.property_documents.list_property_documents(
        123, 
        params={"type": "contract"}
    )
    
    # Filter by date range
    recent_docs = client.property_documents.list_property_documents(
        123,
        params={
            "created_after": "2024-01-01",
            "created_before": "2024-12-31"
        }
    )
    ```

=== "Response Example"

    ```python
    [
        {
            "id": 456,
            "property_id": 123,
            "name": "Purchase Agreement",
            "type": "contract",
            "url": "https://example.com/document.pdf",
            "size": 1024000,
            "mime_type": "application/pdf",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "uploaded_by": "John Agent"
        },
        {
            "id": 457,
            "property_id": 123,
            "name": "Property Photos",
            "type": "photo",
            "url": "https://example.com/photos.zip",
            "size": 5120000,
            "mime_type": "application/zip",
            "created_at": "2024-01-16T14:20:00Z",
            "updated_at": "2024-01-16T14:20:00Z",
            "uploaded_by": "Jane Photographer"
        }
    ]
    ```

---

### `create_property_document(property_id, document_data)`

Add a document to a specific property.

**Parameters:**

- `property_id` (int): The ID of the property
- `document_data` (dict): Document information

**Returns:** Dictionary representing the newly created property document

**Raises:**

- `OpenToCloseAPIError`: If the API request fails
- `ValidationError`: If document data is invalid
- `NotFoundError`: If the property is not found
- `AuthenticationError`: If authentication fails

=== "Basic Usage"

    ```python
    document = client.property_documents.create_property_document(123, {
        "name": "Purchase Agreement",
        "type": "contract",
        "url": "https://example.com/document.pdf"
    })
    
    print(f"Created document {document['id']}: {document['name']}")
    ```

=== "With Metadata"

    ```python
    document = client.property_documents.create_property_document(123, {
        "name": "Inspection Report",
        "type": "inspection",
        "url": "https://example.com/inspection.pdf",
        "description": "Professional home inspection report",
        "tags": ["inspection", "structural", "electrical"],
        "visibility": "private"
    })
    ```

=== "Response Example"

    ```python
    {
        "id": 458,
        "property_id": 123,
        "name": "Purchase Agreement",
        "type": "contract",
        "url": "https://example.com/document.pdf",
        "size": 1024000,
        "mime_type": "application/pdf",
        "created_at": "2024-01-17T09:15:00Z",
        "updated_at": "2024-01-17T09:15:00Z",
        "uploaded_by": "Current User"
    }
    ```

---

### `retrieve_property_document(property_id, document_id)`

Retrieve a specific document for a specific property.

**Parameters:**

- `property_id` (int): The ID of the property
- `document_id` (int): The ID of the document to retrieve

**Returns:** Dictionary representing the property document

**Raises:**

- `NotFoundError`: If the property or document is not found
- `OpenToCloseAPIError`: If the API request fails
- `AuthenticationError`: If authentication fails

=== "Basic Usage"

    ```python
    document = client.property_documents.retrieve_property_document(123, 456)
    print(f"Document name: {document['name']}")
    print(f"Document URL: {document['url']}")
    ```

=== "Error Handling"

    ```python
    from open_to_close.exceptions import NotFoundError
    
    try:
        document = client.property_documents.retrieve_property_document(123, 999)
    except NotFoundError:
        print("Document not found")
    ```

=== "Response Example"

    ```python
    {
        "id": 456,
        "property_id": 123,
        "name": "Purchase Agreement",
        "type": "contract",
        "url": "https://example.com/document.pdf",
        "size": 1024000,
        "mime_type": "application/pdf",
        "description": "Final signed purchase agreement",
        "tags": ["contract", "signed"],
        "visibility": "shared",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z",
        "uploaded_by": "John Agent"
    }
    ```

---

### `update_property_document(property_id, document_id, document_data)`

Update a specific document for a specific property.

**Parameters:**

- `property_id` (int): The ID of the property
- `document_id` (int): The ID of the document to update
- `document_data` (dict): Fields to update

**Returns:** Dictionary representing the updated property document

**Raises:**

- `NotFoundError`: If the property or document is not found
- `ValidationError`: If document data is invalid
- `OpenToCloseAPIError`: If the API request fails
- `AuthenticationError`: If authentication fails

=== "Basic Usage"

    ```python
    updated_document = client.property_documents.update_property_document(
        123, 456, 
        {"name": "Updated Purchase Agreement"}
    )
    ```

=== "Multiple Fields"

    ```python
    updated_document = client.property_documents.update_property_document(
        123, 456, 
        {
            "name": "Final Purchase Agreement",
            "description": "Fully executed purchase agreement",
            "tags": ["contract", "signed", "final"],
            "visibility": "public"
        }
    )
    ```

=== "Response Example"

    ```python
    {
        "id": 456,
        "property_id": 123,
        "name": "Updated Purchase Agreement",
        "type": "contract",
        "url": "https://example.com/document.pdf",
        "size": 1024000,
        "mime_type": "application/pdf",
        "description": "Fully executed purchase agreement",
        "tags": ["contract", "signed", "final"],
        "visibility": "public",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-17T11:45:00Z",
        "uploaded_by": "John Agent"
    }
    ```

---

### `delete_property_document(property_id, document_id)`

Remove a document from a specific property.

**Parameters:**

- `property_id` (int): The ID of the property
- `document_id` (int): The ID of the document to remove

**Returns:** Dictionary containing the API response

**Raises:**

- `NotFoundError`: If the property or document is not found
- `OpenToCloseAPIError`: If the API request fails
- `AuthenticationError`: If authentication fails

=== "Basic Usage"

    ```python
    result = client.property_documents.delete_property_document(123, 456)
    print("Document deleted successfully")
    ```

=== "With Error Handling"

    ```python
    from open_to_close.exceptions import NotFoundError
    
    try:
        result = client.property_documents.delete_property_document(123, 456)
        print("Document deleted successfully")
    except NotFoundError:
        print("Document not found or already deleted")
    ```

=== "Response Example"

    ```python
    {
        "success": True,
        "message": "Document deleted successfully",
        "deleted_id": 456
    }
    ```

---

## Common Use Cases

### Document Management Workflow

```python
# 1. Upload a new document
document = client.property_documents.create_property_document(123, {
    "name": "Purchase Agreement Draft",
    "type": "contract",
    "url": "https://example.com/draft.pdf",
    "visibility": "private"
})

# 2. Update document when finalized
final_document = client.property_documents.update_property_document(
    123, document['id'],
    {
        "name": "Purchase Agreement - Final",
        "description": "Signed and executed purchase agreement",
        "visibility": "shared"
    }
)

# 3. List all contract documents
contracts = client.property_documents.list_property_documents(
    123, 
    params={"type": "contract"}
)

# 4. Clean up old drafts
for doc in contracts:
    if "draft" in doc['name'].lower():
        client.property_documents.delete_property_document(123, doc['id'])
```

### Bulk Document Operations

```python
# Get all documents for multiple properties
property_ids = [123, 124, 125]
all_documents = {}

for prop_id in property_ids:
    documents = client.property_documents.list_property_documents(prop_id)
    all_documents[prop_id] = documents

# Find properties missing required documents
required_types = ["contract", "inspection", "appraisal"]

for prop_id, documents in all_documents.items():
    doc_types = {doc['type'] for doc in documents}
    missing_types = set(required_types) - doc_types
    
    if missing_types:
        print(f"Property {prop_id} missing: {', '.join(missing_types)}")
```

---

## Document Types

Common document types supported by the API:

| Type | Description | Examples |
|------|-------------|----------|
| `contract` | Legal agreements | Purchase agreements, leases |
| `photo` | Property images | Listing photos, virtual tours |
| `inspection` | Inspection reports | Home inspections, appraisals |
| `financial` | Financial documents | Loan docs, bank statements |
| `legal` | Legal documents | Deeds, permits, disclosures |
| `marketing` | Marketing materials | Flyers, brochures |
| `other` | Miscellaneous | Any other document type |

---

## Error Handling

```python
from open_to_close.exceptions import (
    NotFoundError, 
    ValidationError, 
    OpenToCloseAPIError
)

try:
    document = client.property_documents.create_property_document(123, {
        "name": "Test Document",
        "type": "contract",
        "url": "https://example.com/test.pdf"
    })
except ValidationError as e:
    print(f"Invalid document data: {e}")
except NotFoundError:
    print("Property not found")
except OpenToCloseAPIError as e:
    print(f"API error: {e}")
```

---

## Best Practices

1. **Use descriptive names**: Make document names clear and searchable
2. **Organize with types**: Use consistent document types for easy filtering
3. **Add metadata**: Include descriptions and tags for better organization
4. **Manage visibility**: Set appropriate visibility levels for sensitive documents
5. **Clean up regularly**: Remove outdated or duplicate documents
6. **Handle errors gracefully**: Always implement proper error handling
7. **Validate URLs**: Ensure document URLs are accessible before creating records

---

## Related Resources

- [Properties API](properties.md) - Manage property information
- [Property Contacts API](property-contacts.md) - Manage property contacts
- [Property Notes API](property-notes.md) - Add notes to properties
- [Error Handling Guide](../guides/error-handling.md) - Comprehensive error handling