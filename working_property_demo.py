#!/usr/bin/env python3
"""Working demo of Open To Close Property API operations."""

import os
import sys
import json
from typing import Dict, Any, Optional, List

# Add the open_to_close package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from open_to_close import OpenToCloseAPI
from open_to_close.exceptions import (
    AuthenticationError,
    ValidationError,
    OpenToCloseAPIError,
    NotFoundError
)


def demo_list_properties() -> List[Dict[str, Any]]:
    """Demonstrate listing properties (this works)."""
    try:
        print("📋 Listing Properties")
        print("-" * 50)
        
        client = OpenToCloseAPI()
        properties = client.properties.list_properties()
        
        print(f"✅ Found {len(properties)} properties")
        
        for i, prop in enumerate(properties, 1):
            print(f"\nProperty {i}:")
            print(f"  ID: {prop.get('id')}")
            print(f"  Created: {prop.get('created')}")
            print(f"  Timezone: {prop.get('timezone')}")
            
            # Show some field values if available
            field_values = prop.get('field_values', [])
            print(f"  Field Values: {len(field_values)} fields")
            
            for field in field_values[:3]:  # Show first 3 fields
                label = field.get('label', 'Unknown')
                value = field.get('value', 'N/A')
                print(f"    - {label}: {value}")
                
        return properties
        
    except Exception as e:
        print(f"❌ Error listing properties: {e}")
        return []


def demo_retrieve_property(property_id: int) -> Optional[Dict[str, Any]]:
    """Demonstrate retrieving a specific property."""
    try:
        print(f"\n🔍 Retrieving Property ID: {property_id}")
        print("-" * 50)
        
        client = OpenToCloseAPI()
        property_data = client.properties.retrieve_property(property_id)
        
        print("✅ Property retrieved successfully!")
        print(f"Property Details:")
        print(f"  ID: {property_data.get('id')}")
        print(f"  Created: {property_data.get('created')}")
        print(f"  Timezone: {property_data.get('timezone')}")
        
        # Show field values
        field_values = property_data.get('field_values', [])
        print(f"  Total Fields: {len(field_values)}")
        
        print("\nAll Field Values:")
        for field in field_values:
            label = field.get('label', 'Unknown')
            value = field.get('value', 'N/A')
            field_type = field.get('type', 'unknown')
            key = field.get('key', 'unknown')
            print(f"    - {label} ({key}): {value} [{field_type}]")
        
        return property_data
        
    except NotFoundError:
        print(f"❌ Property {property_id} not found")
        return None
    except Exception as e:
        print(f"❌ Error retrieving property {property_id}: {e}")
        return None


def demo_update_property(property_id: int) -> Optional[Dict[str, Any]]:
    """Demonstrate updating a property (using PATCH which is supported)."""
    try:
        print(f"\n✏️ Updating Property ID: {property_id}")
        print("-" * 50)
        
        client = OpenToCloseAPI()
        
        # Try to update with some basic fields that might exist
        # Note: Since we don't know the exact schema, we'll try common field structures
        update_data = {
            "notes": "Updated via API demo script",
            "last_modified": "2025-06-03T17:55:00Z"
        }
        
        print(f"Attempting to update with data: {json.dumps(update_data, indent=2)}")
        
        updated_property = client.properties.update_property(property_id, update_data)
        
        print("✅ Property updated successfully!")
        print(f"Updated Property ID: {updated_property.get('id')}")
        
        return updated_property
        
    except ValidationError as e:
        print(f"❌ Validation error: {e}")
        print("Note: The update fields may not match the API schema")
        return None
    except NotFoundError:
        print(f"❌ Property {property_id} not found")
        return None
    except Exception as e:
        print(f"❌ Error updating property {property_id}: {e}")
        return None


def explain_property_creation_limitation() -> None:
    """Explain why property creation doesn't work."""
    print("\n🚫 Property Creation Limitation")
    print("-" * 50)
    print("❌ Creating new properties via POST is not supported by this API.")
    print("📋 Supported methods for /properties endpoint:")
    print("   - GET: List and retrieve properties")
    print("   - PATCH: Update existing properties") 
    print("\n💡 This suggests that properties are created through other means:")
    print("   - Via the Open To Close web interface")
    print("   - Through other API endpoints")
    print("   - Via import/integration processes")
    print("\n✅ What you CAN do with the Properties API:")
    print("   - List all properties")
    print("   - Retrieve specific property details")
    print("   - Update existing property information")


def main() -> None:
    """Main demo function."""
    print("🏠 Open To Close Properties API Demo")
    print("=" * 60)
    
    # Step 1: List properties
    properties = demo_list_properties()
    
    if not properties:
        print("\n❌ No properties found. Cannot demonstrate retrieve/update operations.")
        explain_property_creation_limitation()
        return
    
    # Step 2: Get the first property ID for demo
    first_property = properties[0]
    property_id = first_property.get('id')
    
    if property_id:
        # Step 3: Retrieve specific property
        property_data = demo_retrieve_property(property_id)
        
        # Step 4: Try to update the property
        if property_data:
            updated_property = demo_update_property(property_id)
    
    # Step 5: Explain limitations
    explain_property_creation_limitation()
    
    print("\n" + "=" * 60)
    print("✅ Demo completed!")
    print("This demonstrates the working functionality of the Properties API wrapper.")


if __name__ == "__main__":
    main()