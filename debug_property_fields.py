#!/usr/bin/env python3
"""Debug script to understand the property fields structure."""

import os
import sys
import json
from typing import Dict, Any, Optional, List

# Add the open_to_close package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from open_to_close import OpenToCloseAPI


def debug_property_fields() -> None:
    """Debug the property fields endpoint to understand the structure."""
    try:
        print("🔍 Debugging Property Fields Structure")
        print("=" * 60)
        
        client = OpenToCloseAPI()
        
        # Test 1: Check what's at /v1/property/fields/
        print("\n📋 Test 1: /v1/property/fields/ endpoint")
        print("-" * 50)
        try:
            fields_response = client.properties.get("/property/fields/")
            print(f"✅ Response type: {type(fields_response)}")
            print(f"Response content: {json.dumps(fields_response, indent=2)}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 2: Try variations of the fields endpoint
        print("\n📋 Test 2: Try different field endpoint variations")
        print("-" * 50)
        
        field_endpoints = [
            "/properties/fields/",
            "/property/field/",
            "/fields/",
            "/property/schema/",
            "/properties/schema/"
        ]
        
        for endpoint in field_endpoints:
            try:
                print(f"\nTrying: {endpoint}")
                response = client.properties.get(endpoint)
                print(f"✅ Success! Type: {type(response)}")
                if isinstance(response, list):
                    print(f"Found {len(response)} items")
                    # Show first item structure
                    if response:
                        print(f"First item keys: {list(response[0].keys())}")
                else:
                    print(f"Response: {response}")
            except Exception as e:
                print(f"❌ Failed: {e}")
        
        # Test 3: Look at existing property field structure for reference
        print("\n📋 Test 3: Examine existing property field structure")
        print("-" * 50)
        try:
            properties = client.properties.list_properties()
            if properties:
                first_property = properties[0]
                field_values = first_property.get('field_values', [])
                print(f"✅ Found {len(field_values)} fields in existing property")
                
                # Look for the required fields in existing property
                required_fields = ['contract_title', 'contract_client_type', 'contract_status']
                print(f"\n🔍 Looking for required fields in existing property:")
                
                for field in field_values:
                    field_key = field.get('key', '')
                    if field_key in required_fields:
                        print(f"\n📝 Found required field: {field_key}")
                        print(f"   ID: {field.get('id')}")
                        print(f"   Label: {field.get('label')}")
                        print(f"   Value: {field.get('value')}")
                        print(f"   Type: {field.get('type')}")
                
                # Show all field keys for reference
                print(f"\n📝 All field keys in existing property:")
                all_keys = [field.get('key') for field in field_values if field.get('key')]
                for i, key in enumerate(sorted(all_keys), 1):
                    print(f"   {i:3d}. {key}")
                    if i >= 20:  # Limit output
                        print(f"   ... and {len(all_keys) - 20} more fields")
                        break
            else:
                print("❌ No existing properties found")
        except Exception as e:
            print(f"❌ Error examining existing property: {e}")
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")


if __name__ == "__main__":
    debug_property_fields()