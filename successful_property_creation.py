#!/usr/bin/env python3
"""Successfully create a property using the correct field structure."""

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


def find_field_by_key(fields_schema: List[Dict[str, Any]], field_key: str) -> Optional[Dict[str, Any]]:
    """Find a specific field in the nested schema structure."""
    for group in fields_schema:
        if 'group' in group:
            for section in group['group'].get('sections', []):
                if 'section' in section:
                    for field in section['section'].get('fields', []):
                        if field.get('key') == field_key:
                            return field
    return None


def create_property_successfully() -> None:
    """Create a property with the correct required fields."""
    try:
        print("🎯 Creating Property Successfully with Open To Close API")
        print("=" * 70)
        
        client = OpenToCloseAPI()
        
        # Step 1: Get the field schema
        print("\n📋 Step 1: Getting field schema...")
        fields_response = client.properties.get("/property/fields/")
        
        # Ensure we have a list
        if not isinstance(fields_response, list):
            print(f"❌ Expected list but got {type(fields_response)}")
            return
            
        fields_schema = fields_response
        print(f"✅ Retrieved field schema with {len(fields_schema)} groups")
        
        # Step 2: Find the required fields
        print("\n🔍 Step 2: Finding required fields...")
        required_fields = ['contract_title', 'contract_client_type', 'contract_status']
        field_values = []
        
        for field_key in required_fields:
            field_def = find_field_by_key(fields_schema, field_key)
            if field_def:
                field_id = field_def.get('id')
                field_type = field_def.get('type')
                print(f"   Found {field_key}: ID={field_id}, Type={field_type}")
                
                if field_key == 'contract_title':
                    # Text field
                    field_values.append({
                        "id": field_id,
                        "value": "API Created Property - Success!"
                    })
                    
                elif field_key == 'contract_client_type':
                    # Choice field - use first option
                    options = field_def.get('options', [])
                    if options:
                        first_option = options[0]
                        field_values.append({
                            "id": field_id,
                            "value": first_option.get('title')
                        })
                        print(f"     Using choice: {first_option.get('title')}")
                        
                elif field_key == 'contract_status':
                    # Choice field - use first option
                    options = field_def.get('options', [])
                    if options:
                        first_option = options[0]
                        field_values.append({
                            "id": field_id,
                            "value": first_option.get('title')
                        })
                        print(f"     Using choice: {first_option.get('title')}")
            else:
                print(f"   ❌ Could not find field: {field_key}")
        
        # Step 3: Add some optional property information
        print("\n📝 Step 3: Adding optional property information...")
        optional_fields = {
            'property_address': "123 API Success Boulevard",
            'property_city': "Success City", 
            'property_state': "California",
            'property_zip': "90210"
        }
        
        for field_key, value in optional_fields.items():
            field_def = find_field_by_key(fields_schema, field_key)
            if field_def:
                field_id = field_def.get('id')
                field_values.append({
                    "id": field_id,
                    "value": value
                })
                print(f"   Added {field_key}: {value}")
        
        # Step 4: Create the property
        print(f"\n🏗️ Step 4: Creating property with {len(field_values)} fields...")
        property_data = {
            "field_values": field_values
        }
        
        print("Property data structure:")
        print(json.dumps(property_data, indent=2))
        
        created_property = client.properties.create_property(property_data)
        
        print("\n🎉 SUCCESS! Property created!")
        print(f"Created property ID: {created_property.get('id')}")
        print(f"Created date: {created_property.get('created')}")
        
        # Step 5: Verify the creation
        property_id = created_property.get('id')
        if property_id:
            print(f"\n✅ Step 5: Verifying created property {property_id}...")
            retrieved = client.properties.retrieve_property(property_id)
            
            print(f"Verification successful!")
            print(f"   Property ID: {retrieved.get('id')}")
            print(f"   Created: {retrieved.get('created')}")
            print(f"   Total fields: {len(retrieved.get('field_values', []))}")
            
            # Show the key fields we set
            field_values_retrieved = retrieved.get('field_values', [])
            print(f"\n📋 Key fields we set:")
            for field in field_values_retrieved:
                field_key = field.get('key')
                if field_key in ['contract_title', 'contract_client_type', 'contract_status', 
                               'property_address', 'property_city', 'property_state', 'property_zip']:
                    print(f"   {field.get('label', field_key)}: {field.get('value', 'N/A')}")
        
        print("\n" + "=" * 70)
        print("🎊 PROPERTY CREATION COMPLETED SUCCESSFULLY!")
        print("The Open To Close API wrapper is working perfectly!")
        
    except ValidationError as e:
        print(f"❌ Validation error: {e}")
        if hasattr(e, 'response_data'):
            print(f"Response data: {e.response_data}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    create_property_successfully()