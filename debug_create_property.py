#!/usr/bin/env python3
"""Debug script to test property creation with detailed error information."""

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
    OpenToCloseAPIError
)


def debug_create_property() -> Optional[Dict[str, Any]]:
    """Debug property creation with minimal data and detailed error reporting."""
    try:
        # Initialize the API client
        print("Initializing Open To Close API client...")
        client = OpenToCloseAPI()
        
        # Start with minimal property data
        property_data = {
            "address": "123 Test Street",
            "city": "Test City", 
            "state": "CA",
            "zip": "12345"
        }
        
        print(f"Creating property with minimal data: {json.dumps(property_data, indent=2)}")
        
        # Try to create the property
        created_property = client.properties.create_property(property_data)
        
        print("✅ Property created successfully!")
        print(f"Created property: {json.dumps(created_property, indent=2)}")
        
        return created_property
        
    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        if hasattr(e, 'response_data'):
            print(f"Response data: {e.response_data}")
        return None
        
    except ValidationError as e:
        print(f"❌ Validation error: {e}")
        if hasattr(e, 'response_data'):
            print(f"Response data: {e.response_data}")
        return None
        
    except OpenToCloseAPIError as e:
        print(f"❌ API error: {e}")
        if hasattr(e, 'response_data'):
            print(f"Response data: {e.response_data}")
        if hasattr(e, 'status_code'):
            print(f"Status code: {e.status_code}")
        return None
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"Error type: {type(e)}")
        return None


def test_api_connection() -> bool:
    """Test basic API connection."""
    try:
        print("Testing API connection...")
        client = OpenToCloseAPI()
        
        # Try listing properties (should work)
        properties = client.properties.list_properties()
        print(f"✅ API connection successful - found {len(properties)} properties")
        return True
        
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False


def inspect_api_request() -> None:
    """Inspect what request is being made."""
    try:
        print("\nInspecting API client setup...")
        client = OpenToCloseAPI()
        
        print(f"Base URL: {client.properties.base_url}")
        api_key = client.properties.api_key
        if api_key:
            print(f"API Key (first 20 chars): {api_key[:20]}...")
        else:
            print("API Key: None")
        
        # Check session headers
        print(f"Session headers: {dict(client.properties.session.headers)}")
        
    except Exception as e:
        print(f"Error inspecting API client: {e}")


if __name__ == "__main__":
    print("🔍 Open To Close Property Creation Debug")
    print("=" * 50)
    
    # Test API connection first
    connection_ok = test_api_connection()
    
    if connection_ok:
        # Inspect API setup
        inspect_api_request()
        
        # Try creating property with debug info
        print("\n" + "=" * 50)
        created_property = debug_create_property()
        
        if created_property:
            print("\n✅ Debug test completed successfully!")
        else:
            print("\n❌ Debug test failed")
    else:
        print("❌ Cannot proceed - API connection failed")