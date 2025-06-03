#!/usr/bin/env python3
"""Create a property with the required fields from the API schema."""

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


def get_property_fields(client: OpenToCloseAPI) -> Optional[List[Dict[str, Any]]]:
    """Get the property field schema from the API."""
    try:
        print("📋 Getting property field schema from /v1/property/fields/")
        print("-" * 60)
        
        # Note: The API error message mentioned /v1/property/fields/ (singular)
        fields_response = client.properties.get("/property/fields/")
        
        print(f"✅ Successfully retrieved field schema")
        print(f"Response type: {type(fields_response)}")
        
        if isinstance(fields_response, list):
            print(f"Found {len(fields_response)} field definitions")
            
            # Look for the required fields
            required_fields = ['contract_title', 'contract_client_type', 'contract_status']
            print(f"\n🔍 Looking for required fields: {required_fields}")
            
            for field in fields_response:
                field_key = field.get('key', '')
                if field_key in required_fields:
                    print(f"\n📝 Required Field: {field_key}")
                    print(f"   Label: {field.get('label', 'N/A')}")
                    print(f"   Type: {field.get('type', 'N/A')}")
                    print(f"   ID: {field.get('id', 'N/A')}")
                    
                    # If it's a choice field, show the options
                    if field.get('type') == 'choice' and 'choices' in field:
                        print(f"   Choices:")
                        for choice in field.get('choices', [])[:5]:  # Show first 5 choices
                            print(f"     - {choice.get('value', 'N/A')} (ID: {choice.get('id', 'N/A')})")
        
        return fields_response if isinstance(fields_response, list) else None
        
    except Exception as e:
        print(f"❌ Error getting field schema: {e}")
        return None


def create_property_with_required_fields(client: OpenToCloseAPI, fields_schema: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Create a property with the required fields properly structured."""
    try:
        print("\n🏗️ Creating property with required fields")
        print("-" * 60)
        
        # Create a mapping of field keys to field info
        field_map = {field.get('key'): field for field in fields_schema}
        
        # Build the required field values
        field_values = []
        
        # Required field 1: contract_title (text field)
        if 'contract_title' in field_map:
            contract_title_field = field_map['contract_title']
            field_values.append({
                "id": contract_title_field.get('id'),
                "value": "Test Property Creation via API"
            })
        
        # Required field 2: contract_client_type (choice field)
        if 'contract_client_type' in field_map:
            client_type_field = field_map['contract_client_type']
            choices = client_type_field.get('choices', [])
            if choices:
                # Use the first available choice
                first_choice = choices[0]
                field_values.append({
                    "id": client_type_field.get('id'),
                    "value": first_choice.get('value')
                })
        
        # Required field 3: contract_status (choice field)
        if 'contract_status' in field_map:
            status_field = field_map['contract_status']
            choices = status_field.get('choices', [])
            if choices:
                # Use the first available choice
                first_choice = choices[0]
                field_values.append({
                    "id": status_field.get('id'),
                    "value": first_choice.get('value')
                })
        
        # Add some optional property information
        # Property address
        if 'property_address' in field_map:
            address_field = field_map['property_address']
            field_values.append({
                "id": address_field.get('id'),
                "value": "789 API Success Avenue"
            })
        
        # Property city
        if 'property_city' in field_map:
            city_field = field_map['property_city']
            field_values.append({
                "id": city_field.get('id'),
                "value": "Success City"
            })
        
        # Property state
        if 'property_state' in field_map:
            state_field = field_map['property_state']
            field_values.append({
                "id": state_field.get('id'),
                "value": "California"
            })
        
        # Create the property data structure
        property_data = {
            "field_values": field_values
        }
        
        print(f"Property data structure:")
        print(json.dumps(property_data, indent=2))
        
        # Create the property
        created_property = client.properties.create_property(property_data)
        
        print("\n🎉 Property created successfully!")
        print(f"Created property ID: {created_property.get('id')}")
        print(f"Created property: {json.dumps(created_property, indent=2)}")
        
        return created_property
        
    except ValidationError as e:
        print(f"❌ Validation error: {e}")
        if hasattr(e, 'response_data'):
            print(f"Response data: {e.response_data}")
        return None
    except Exception as e:
        print(f"❌ Error creating property: {e}")
        return None


def main() -> None:
    """Main function to demonstrate property creation with correct fields."""
    try:
        print("🏠 Open To Close - Property Creation with Required Fields")
        print("=" * 70)
        
        client = OpenToCloseAPI()
        
        # Step 1: Get the field schema
        fields_schema = get_property_fields(client)
        
        if not fields_schema:
            print("❌ Cannot proceed without field schema")
            return
        
        # Step 2: Create property with required fields
        created_property = create_property_with_required_fields(client, fields_schema)
        
        if created_property:
            # Step 3: Verify by retrieving the created property
            property_id = created_property.get('id')
            if property_id:
                print(f"\n🔍 Verifying created property {property_id}")
                print("-" * 60)
                try:
                    retrieved = client.properties.retrieve_property(property_id)
                    print(f"✅ Successfully verified property creation")
                    print(f"Property ID: {retrieved.get('id')}")
                    print(f"Created: {retrieved.get('created')}")
                    print(f"Field count: {len(retrieved.get('field_values', []))}")
                except Exception as e:
                    print(f"❌ Error verifying property: {e}")
        
        print("\n" + "=" * 70)
        print("✅ Property creation demo completed!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")


if __name__ == "__main__":
    main()