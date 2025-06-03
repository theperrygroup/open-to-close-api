#!/usr/bin/env python3
"""Test script to create a property using the Open To Close API."""

import os
import sys
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add the open_to_close package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from open_to_close import OpenToCloseAPI
from open_to_close.exceptions import (
    AuthenticationError,
    ValidationError,
    OpenToCloseAPIError
)


def create_test_property() -> Optional[Dict[str, Any]]:
    """Create a test property using the Open To Close API."""
    try:
        # Initialize the API client (will use API key from .env file)
        print("Initializing Open To Close API client...")
        client = OpenToCloseAPI()
        
        # Property data to create
        property_data = {
            "address": "123 Main Street",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94102",
            "property_type": "Single Family Home",
            "bedrooms": 3,
            "bathrooms": 2,
            "square_feet": 1500,
            "lot_size": 0.25,
            "price": 850000,
            "status": "active",
            "description": "Beautiful 3-bedroom home in prime SF location",
            "year_built": 1950,
            "listing_date": datetime.now().isoformat()
        }
        
        print(f"Creating property with data: {property_data}")
        
        # Create the property
        created_property = client.properties.create_property(property_data)
        
        print("✅ Property created successfully!")
        print(f"Property ID: {created_property.get('id')}")
        print(f"Address: {created_property.get('address')}")
        print(f"Full response: {created_property}")
        
        return created_property
        
    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("Please check your API key in the .env file")
        return None
        
    except ValidationError as e:
        print(f"❌ Validation error: {e}")
        print("Please check the property data format")
        return None
        
    except OpenToCloseAPIError as e:
        print(f"❌ API error: {e}")
        return None
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None


def list_properties() -> List[Dict[str, Any]]:
    """List existing properties to verify our creation."""
    try:
        print("\nListing existing properties...")
        client = OpenToCloseAPI()
        
        properties = client.properties.list_properties()
        
        print(f"Found {len(properties)} properties:")
        for prop in properties[:5]:  # Show first 5 properties
            print(f"  - ID: {prop.get('id')}, Address: {prop.get('address')}")
            
        return properties
        
    except Exception as e:
        print(f"❌ Error listing properties: {e}")
        return []


if __name__ == "__main__":
    print("🏠 Open To Close Property Creation Test")
    print("=" * 50)
    
    # First, try to list existing properties
    existing_properties = list_properties()
    
    # Then create a new property
    print("\n" + "=" * 50)
    created_property = create_test_property()
    
    if created_property:
        print("\n" + "=" * 50)
        print("✅ Test completed successfully!")
        
        # Optionally, try to retrieve the created property
        try:
            property_id = created_property.get('id')
            if property_id:
                print(f"\nRetrieving created property (ID: {property_id})...")
                client = OpenToCloseAPI()
                retrieved_property = client.properties.retrieve_property(property_id)
                print(f"Retrieved property: {retrieved_property.get('address')}")
        except Exception as e:
            print(f"Note: Could not retrieve created property: {e}")
    else:
        print("\n❌ Test failed - property creation unsuccessful")