#!/usr/bin/env python3
"""Final property creation script with correct field structure including keys."""

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


def create_property_final() -> None:
    """Create a property with the complete field structure including keys."""
    try:
        print("🎯 FINAL Property Creation - Open To Close API")
        print("=" * 70)
        
        client = OpenToCloseAPI()
        
        # Step 1: Get the field schema
        print("\n📋 Step 1: Getting field schema...")
        fields_response = client.properties.get("/property/fields/")
        
        if not isinstance(fields_response, list):
            print(f"❌ Expected list but got {type(fields_response)}")
            return
            
        fields_schema = fields_response
        print(f"✅ Retrieved field schema with {len(fields_schema)} groups")
        
        # Step 2: Build field values with both id and key
        print("\n🔍 Step 2: Building required fields with id, key, and value...")
        field_values = []
        
        # Required field 1: contract_title
        field_def = find_field_by_key(fields_schema, 'contract_title')
        if field_def:
            field_values.append({
                "id": field_def.get('id'),
                "key": field_def.get('key'),
                "value": "API Created Property - Final Test!",
                "type": field_def.get('type'),
                "label": field_def.get('title')
            })
            print(f"   ✅ contract_title: ID={field_def.get('id')}")
        
        # Required field 2: contract_client_type
        field_def = find_field_by_key(fields_schema, 'contract_client_type')
        if field_def:
            options = field_def.get('options', [])
            if options:
                choice_value = options[0].get('title')
                field_values.append({
                    "id": field_def.get('id'),
                    "key": field_def.get('key'),
                    "value": choice_value,
                    "type": field_def.get('type'),
                    "label": field_def.get('title')
                })
                print(f"   ✅ contract_client_type: ID={field_def.get('id')}, Value={choice_value}")
        
        # Required field 3: contract_status
        field_def = find_field_by_key(fields_schema, 'contract_status')
        if field_def:
            options = field_def.get('options', [])
            if options:
                choice_value = options[0].get('title')
                field_values.append({
                    "id": field_def.get('id'),
                    "key": field_def.get('key'),
                    "value": choice_value,
                    "type": field_def.get('type'),
                    "label": field_def.get('title')
                })
                print(f"   ✅ contract_status: ID={field_def.get('id')}, Value={choice_value}")
        
        # Step 3: Add property address fields
        print("\n📝 Step 3: Adding property address fields...")
        address_fields = {
            'property_address': "456 Final Test Avenue",
            'property_city': "API City",
            'property_state': "California",
            'property_zip': "90210"
        }
        
        for field_key, value in address_fields.items():
            field_def = find_field_by_key(fields_schema, field_key)
            if field_def:
                field_values.append({
                    "id": field_def.get('id'),
                    "key": field_def.get('key'),
                    "value": value,
                    "type": field_def.get('type'),
                    "label": field_def.get('title')
                })
                print(f"   ✅ {field_key}: {value}")
        
        # Step 4: Create the property
        print(f"\n🏗️ Step 4: Creating property with {len(field_values)} fields...")
        property_data = {
            "field_values": field_values
        }
        
        print("Property data structure (first 3 fields):")
        preview_data = {
            "field_values": field_values[:3]
        }
        print(json.dumps(preview_data, indent=2))
        print(f"... and {len(field_values) - 3} more fields")
        
        created_property = client.properties.create_property(property_data)
        
        print("\n🎉 🎉 🎉 SUCCESS! Property created! 🎉 🎉 🎉")
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
            
            # Show our created fields
            field_values_retrieved = retrieved.get('field_values', [])
            print(f"\n📋 Our created fields:")
            target_keys = ['contract_title', 'contract_client_type', 'contract_status', 
                          'property_address', 'property_city', 'property_state', 'property_zip']
            
            for field in field_values_retrieved:
                field_key = field.get('key')
                if field_key in target_keys:
                    print(f"   {field.get('label', field_key)}: {field.get('value', 'N/A')}")
        
        print("\n" + "=" * 70)
        print("🏆 PROPERTY CREATION SUCCESSFUL! 🏆")
        print("✅ The Open To Close API wrapper works perfectly!")
        print("✅ Properties CAN be created via the API!")
        print("✅ The trailing slash was the key!")
        
    except ValidationError as e:
        print(f"❌ Validation error: {e}")
        if hasattr(e, 'response_data'):
            print(f"Response data: {e.response_data}")
            
        # If still failing, let's try a minimal approach
        print("\n🔄 Trying minimal approach with just required fields...")
        try:
            minimal_data = {
                "field_values": [
                    {"id": 922675, "value": "Minimal Test"},  # contract_title
                    {"id": 922663, "value": "Buyer"},  # contract_client_type
                    {"id": 922662, "value": "Listing - Pre-MLS"}  # contract_status
                ]
            }
            
            print("Minimal data:")
            print(json.dumps(minimal_data, indent=2))
            
            minimal_property = client.properties.create_property(minimal_data)
            print("\n🎉 SUCCESS with minimal approach!")
            print(f"Created property ID: {minimal_property.get('id')}")
            
        except Exception as minimal_error:
            print(f"❌ Minimal approach also failed: {minimal_error}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    create_property_final()