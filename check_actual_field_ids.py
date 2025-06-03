#!/usr/bin/env python3
"""Check the actual field IDs in the existing property."""

import os
import sys
import json
from typing import Dict, Any, Optional, List

# Add the open_to_close package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from open_to_close import OpenToCloseAPI


def check_actual_field_ids() -> None:
    """Check the actual field IDs being used in existing properties."""
    try:
        print("🔍 Checking Actual Field IDs in Existing Property")
        print("=" * 60)
        
        client = OpenToCloseAPI()
        
        # Get existing properties
        print("\n📋 Getting existing properties...")
        properties = client.properties.list_properties()
        
        if not properties:
            print("❌ No existing properties found")
            return
            
        property_id = properties[0].get('id')
        print(f"✅ Found property {property_id}")
        
        # Get detailed property info
        print(f"\n🔍 Getting detailed info for property {property_id}...")
        property_data = client.properties.retrieve_property(property_id)
        
        field_values = property_data.get('field_values', [])
        print(f"✅ Property has {len(field_values)} fields")
        
        # Look for the required fields
        required_fields = ['contract_title', 'contract_client_type', 'contract_status']
        print(f"\n📝 Required field IDs in existing property:")
        
        actual_field_data = {}
        for field in field_values:
            field_key = field.get('key')
            if field_key in required_fields:
                field_id = field.get('id')
                field_value = field.get('value')
                field_type = field.get('type')
                
                actual_field_data[field_key] = {
                    'id': field_id,
                    'value': field_value,
                    'type': field_type
                }
                
                print(f"   {field_key}:")
                print(f"     ID: {field_id}")
                print(f"     Value: '{field_value}'")
                print(f"     Type: {field_type}")
        
        # Now try creating a property using the ACTUAL field IDs from existing property
        print(f"\n🏗️ Attempting property creation with ACTUAL field IDs...")
        
        field_values_for_creation = []
        
        if 'contract_title' in actual_field_data:
            field_values_for_creation.append({
                "id": actual_field_data['contract_title']['id'],
                "value": "ACTUAL ID Test Property"
            })
            
        if 'contract_client_type' in actual_field_data:
            field_values_for_creation.append({
                "id": actual_field_data['contract_client_type']['id'],
                "value": actual_field_data['contract_client_type']['value']  # Use same value as existing
            })
            
        if 'contract_status' in actual_field_data:
            field_values_for_creation.append({
                "id": actual_field_data['contract_status']['id'],
                "value": actual_field_data['contract_status']['value']  # Use same value as existing
            })
        
        creation_data = {
            "field_values": field_values_for_creation
        }
        
        print("Creation data with actual field IDs:")
        print(json.dumps(creation_data, indent=2))
        
        # Try to create
        try:
            created_property = client.properties.create_property(creation_data)
            print("\n🎉 🎉 🎉 SUCCESS! Property created with actual field IDs!")
            print(f"Created property ID: {created_property.get('id')}")
            print(f"Created date: {created_property.get('created')}")
            
        except Exception as create_error:
            print(f"\n❌ Still failed with actual field IDs: {create_error}")
            
            # Let's also compare schema IDs vs actual IDs
            print(f"\n🔍 Comparing schema field IDs vs actual field IDs...")
            
            schema_response = client.properties.get("/property/fields/")
            print(f"Schema field IDs found:")
            
            for group in schema_response:
                if 'group' in group:
                    for section in group['group'].get('sections', []):
                        if 'section' in section:
                            for field in section['section'].get('fields', []):
                                field_key = field.get('key')
                                if field_key in required_fields:
                                    schema_id = field.get('id')
                                    actual_id = actual_field_data.get(field_key, {}).get('id')
                                    match = "✅" if schema_id == actual_id else "❌"
                                    print(f"   {field_key}: Schema={schema_id}, Actual={actual_id} {match}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    check_actual_field_ids()