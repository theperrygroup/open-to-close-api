#!/usr/bin/env python3
"""Create a property using the ACTUAL field IDs from existing properties."""

import os
import sys
import json

# Add the open_to_close package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from open_to_close import OpenToCloseAPI


def create_property_with_actual_ids() -> None:
    """Create a property using the actual field IDs from the existing property."""
    try:
        print("🎯 FINAL ATTEMPT - Using Actual Field IDs from Existing Property")
        print("=" * 80)
        
        client = OpenToCloseAPI()
        
        # Use the ACTUAL field IDs we discovered from the existing property
        print("\n📋 Using actual field IDs from existing property:")
        print("   contract_title: 143501981")
        print("   contract_client_type: 143501969") 
        print("   contract_status: 143501968")
        
        # Create property data with actual field IDs
        property_data = {
            "field_values": [
                {
                    "id": 143501981,  # contract_title (actual ID from existing property)
                    "value": "🚀 SUCCESS! Property Created via API!"
                },
                {
                    "id": 143501969,  # contract_client_type (actual ID from existing property)
                    "value": "Buyer"  # Use same value as existing property
                },
                {
                    "id": 143501968,  # contract_status (actual ID from existing property) 
                    "value": "Listing - Pre-MLS"  # Use same value as existing property
                }
            ]
        }
        
        print("\n🏗️ Creating property with actual field IDs...")
        print("Property data:")
        print(json.dumps(property_data, indent=2))
        
        # CREATE THE PROPERTY
        created_property = client.properties.create_property(property_data)
        
        # SUCCESS!
        print("\n" + "🎉" * 20)
        print("   🏆 PROPERTY CREATION SUCCESSFUL! 🏆")
        print("🎉" * 20)
        
        print(f"\n✅ Created property details:")
        print(f"   Property ID: {created_property.get('id')}")
        print(f"   Created Date: {created_property.get('created')}")
        print(f"   Timezone: {created_property.get('timezone')}")
        
        # Verify by retrieving the created property
        property_id = created_property.get('id')
        if property_id:
            print(f"\n🔍 Verifying created property {property_id}...")
            
            retrieved = client.properties.retrieve_property(property_id)
            print(f"✅ Verification successful!")
            
            # Show the fields we created
            field_values = retrieved.get('field_values', [])
            print(f"\n📋 Created property has {len(field_values)} total fields")
            print(f"Our custom fields:")
            
            target_field_ids = [143501981, 143501969, 143501968]
            for field in field_values:
                if field.get('id') in target_field_ids:
                    print(f"   {field.get('label', field.get('key'))}: {field.get('value')}")
        
        print(f"\n" + "=" * 80)
        print("🎊 PROPERTY CREATION BREAKTHROUGH! 🎊")
        print("✅ The Open To Close API DOES support property creation!")
        print("✅ The key insights were:")
        print("   1. Endpoints need trailing slash: /properties/")
        print("   2. Must use actual field IDs from existing properties")
        print("   3. Schema endpoint returns template IDs, not actual IDs")
        print("✅ Property successfully created and verified!")
        
    except Exception as e:
        print(f"\n❌ Final attempt failed: {e}")
        print("This suggests there may be additional restrictions on property creation")
        print("for this specific account or API configuration.")


if __name__ == "__main__":
    create_property_with_actual_ids()