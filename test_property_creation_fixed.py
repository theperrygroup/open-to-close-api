#!/usr/bin/env python3
"""Test property creation with the corrected trailing slash endpoints."""

import os
import sys
import json
from typing import Dict, Any, Optional

# Add the open_to_close package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from open_to_close import OpenToCloseAPI
from open_to_close.exceptions import (
    AuthenticationError,
    ValidationError,
    OpenToCloseAPIError,
    NotFoundError
)


def test_fixed_endpoints() -> None:
    """Test all property endpoints with the corrected trailing slashes."""
    try:
        print("🔧 Testing Fixed Property Endpoints (with trailing slash)")
        print("=" * 65)
        
        client = OpenToCloseAPI()
        
        # Test 1: List properties with trailing slash
        print("\n📋 Test 1: List Properties (/properties/)")
        print("-" * 50)
        try:
            properties = client.properties.list_properties()
            print(f"✅ List properties successful: Found {len(properties)} properties")
            
            if properties:
                property_id = properties[0].get('id')
                print(f"First property ID: {property_id}")
            else:
                print("No properties found to test retrieve/update operations")
                property_id = None
                
        except Exception as e:
            print(f"❌ List properties failed: {e}")
            property_id = None
        
        # Test 2: Create property with trailing slash
        print("\n🏗️ Test 2: Create Property (/properties/)")
        print("-" * 50)
        
        property_data = {
            "address": "456 Fixed Street",
            "city": "Test City",
            "state": "CA",
            "zip_code": "12345",
            "property_type": "Single Family Home"
        }
        
        try:
            print(f"Attempting to create property with data:")
            print(json.dumps(property_data, indent=2))
            
            created_property = client.properties.create_property(property_data)
            print("🎉 Property creation SUCCESSFUL!")
            print(f"Created property ID: {created_property.get('id')}")
            print(f"Created property data: {json.dumps(created_property, indent=2)}")
            
            # If creation was successful, test retrieve on the new property
            new_property_id = created_property.get('id')
            if new_property_id:
                print(f"\n🔍 Test 3: Retrieve Created Property ({new_property_id})")
                print("-" * 50)
                try:
                    retrieved = client.properties.retrieve_property(new_property_id)
                    print(f"✅ Successfully retrieved created property")
                    print(f"Address: {retrieved.get('address', 'N/A')}")
                except Exception as e:
                    print(f"❌ Error retrieving created property: {e}")
            
        except ValidationError as e:
            print(f"❌ Validation error: {e}")
            if hasattr(e, 'response_data'):
                print(f"Response data: {e.response_data}")
        except OpenToCloseAPIError as e:
            print(f"❌ API error: {e}")
            if hasattr(e, 'response_data'):
                print(f"Response data: {e.response_data}")
            if hasattr(e, 'status_code'):
                print(f"Status code: {e.status_code}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        
        # Test 3: Retrieve existing property (if we have one)
        if property_id:
            print(f"\n🔍 Test 4: Retrieve Existing Property ({property_id})")
            print("-" * 50)
            try:
                property_data = client.properties.retrieve_property(property_id)
                print(f"✅ Successfully retrieved property {property_id}")
                print(f"Property created: {property_data.get('created')}")
                print(f"Field count: {len(property_data.get('field_values', []))}")
            except Exception as e:
                print(f"❌ Error retrieving property {property_id}: {e}")
        
        print("\n" + "=" * 65)
        print("✅ Test completed!")
        
    except Exception as e:
        print(f"❌ Test setup failed: {e}")


if __name__ == "__main__":
    test_fixed_endpoints()