#!/usr/bin/env python3
"""Detailed debug script to inspect HTTP requests."""

import os
import sys
import json
import requests
from typing import Dict, Any, Optional, Union, List

# Add the open_to_close package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from open_to_close import OpenToCloseAPI
from open_to_close.base_client import BaseClient


class DebugClient(BaseClient):
    """Debug version of BaseClient that logs requests."""
    
    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        files: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request with detailed logging."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        # Add api_token to params for all requests
        if params is None:
            params = {}
        params["api_token"] = self.api_key

        print(f"\n🔍 Making {method} request:")
        print(f"URL: {url}")
        print(f"Params: {params}")
        print(f"Headers: {dict(self.session.headers)}")
        if json_data:
            print(f"JSON Data: {json.dumps(json_data, indent=2)}")

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=json_data,
                data=data,
                files=files,
                params=params,
            )
            
            print(f"\n📡 Response received:")
            print(f"Status Code: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            print(f"Content: {response.text[:500]}...")  # First 500 chars
            
            return self._handle_response(response)

        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {str(e)}")
            raise


def debug_api_requests() -> None:
    """Debug the API requests in detail."""
    try:
        print("🔍 Creating debug client...")
        
        # Create a debug instance
        debug_client = DebugClient()
        
        print(f"Base URL: {debug_client.base_url}")
        api_key = debug_client.api_key
        if api_key:
            print(f"API Key: {api_key[:20]}...")
        else:
            print("API Key: None")
        
        # Test 1: List properties (this works)
        print("\n" + "="*50)
        print("🔍 TEST 1: List Properties (should work)")
        print("="*50)
        
        properties = debug_client.get("/properties")
        print(f"✅ List properties successful: {len(properties) if isinstance(properties, list) else 'Not a list'}")
        
        # Test 2: Create property (this fails)
        print("\n" + "="*50)
        print("🔍 TEST 2: Create Property (currently failing)")
        print("="*50)
        
        property_data = {
            "address": "123 Debug Street",
            "city": "Debug City",
            "state": "CA",
            "zip_code": "12345"
        }
        
        try:
            created_property = debug_client.post("/properties", json_data=property_data)
            print(f"✅ Create property successful: {created_property}")
        except Exception as e:
            print(f"❌ Create property failed: {e}")
            
        # Test 3: Try different variations of the endpoint
        print("\n" + "="*50)
        print("🔍 TEST 3: Try Alternative Endpoints")
        print("="*50)
        
        test_endpoints = [
            ("POST", "/property"),  # singular
            ("POST", "/properties/create"),  # with create suffix
            ("POST", "/v1/properties"),  # with version
        ]
        
        for method, endpoint in test_endpoints:
            try:
                print(f"\nTrying {method} {endpoint}...")
                response = debug_client._request(method, endpoint, json_data=property_data)
                print(f"✅ {endpoint} worked!")
                break
            except Exception as e:
                print(f"❌ {endpoint} failed: {e}")
                
    except Exception as e:
        print(f"❌ Debug failed: {e}")


if __name__ == "__main__":
    print("🔍 Detailed API Debug")
    print("=" * 50)
    debug_api_requests()