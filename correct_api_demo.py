#!/usr/bin/env python3
"""Demo using the actual Open To Close API endpoints from Postman collection."""

import os
import sys
import json
import requests
from typing import Dict, Any, Optional, List

# Add the open_to_close package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from open_to_close.base_client import BaseClient


class ActualOpenToCloseAPI(BaseClient):
    """API client using the actual endpoints from the Postman collection."""
    
    def get_agents(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get all agents."""
        response = self.get("/agents", params=params)
        return self._process_list_response(response)
    
    def get_users(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get all users."""
        response = self.get("/users", params=params)
        return self._process_list_response(response)
    
    def get_tags(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get all tags."""
        response = self.get("/tags", params=params)
        return self._process_list_response(response)
    
    def get_timezones(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get all timezones."""
        response = self.get("/timezones", params=params)
        return self._process_list_response(response)


def demo_actual_endpoints() -> None:
    """Demo the actual working endpoints from the Postman collection."""
    try:
        print("🌐 Open To Close API - Actual Working Endpoints")
        print("=" * 60)
        
        client = ActualOpenToCloseAPI()
        
        # Test Agents endpoint
        print("\n👥 Testing /v1/agents endpoint:")
        print("-" * 40)
        try:
            agents = client.get_agents()
            print(f"✅ Found {len(agents)} agents")
            
            for i, agent in enumerate(agents[:3], 1):  # Show first 3
                print(f"\nAgent {i}:")
                print(f"  ID: {agent.get('id')}")
                print(f"  Name: {agent.get('first_name', '')} {agent.get('last_name', '')}")
                print(f"  Email: {agent.get('email', 'N/A')}")
                
        except Exception as e:
            print(f"❌ Agents endpoint failed: {e}")
        
        # Test Users endpoint
        print("\n👤 Testing /v1/users endpoint:")
        print("-" * 40)
        try:
            users = client.get_users()
            print(f"✅ Found {len(users)} users")
            
            for i, user in enumerate(users[:3], 1):  # Show first 3
                print(f"\nUser {i}:")
                print(f"  ID: {user.get('id')}")
                print(f"  Name: {user.get('name', user.get('first_name', '') + ' ' + user.get('last_name', ''))}")
                print(f"  Email: {user.get('email', 'N/A')}")
                
        except Exception as e:
            print(f"❌ Users endpoint failed: {e}")
        
        # Test Tags endpoint
        print("\n🏷️ Testing /v1/tags endpoint:")
        print("-" * 40)
        try:
            tags = client.get_tags()
            print(f"✅ Found {len(tags)} tags")
            
            for i, tag in enumerate(tags[:5], 1):  # Show first 5
                print(f"\nTag {i}:")
                print(f"  ID: {tag.get('id')}")
                print(f"  Title: {tag.get('title', 'N/A')}")
                print(f"  Category: {tag.get('category', 'N/A')}")
                print(f"  Color: {tag.get('color', 'N/A')}")
                
        except Exception as e:
            print(f"❌ Tags endpoint failed: {e}")
        
        # Test Timezones endpoint
        print("\n🌍 Testing /v1/timezones endpoint:")
        print("-" * 40)
        try:
            timezones = client.get_timezones()
            print(f"✅ Found {len(timezones)} timezones")
            
            for i, tz in enumerate(timezones[:5], 1):  # Show first 5
                print(f"\nTimezone {i}:")
                print(f"  ID: {tz.get('id')}")
                print(f"  Country Code: {tz.get('country_code', 'N/A')}")
                print(f"  Zone: {tz.get('country_zone', 'N/A')}")
                print(f"  Abbreviation: {tz.get('zone_abbreviation', 'N/A')}")
                
        except Exception as e:
            print(f"❌ Timezones endpoint failed: {e}")
        
        print("\n" + "=" * 60)
        print("✅ Demo completed!")
        print("\n📝 Summary of working endpoints:")
        print("   - GET /v1/agents")
        print("   - GET /v1/users") 
        print("   - GET /v1/tags")
        print("   - GET /v1/timezones")
        
        print("\n❌ Note about properties:")
        print("   The /v1/properties endpoint is NOT in the Postman collection")
        print("   This explains why property creation was failing with 405 errors")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")


def test_property_endpoint_directly() -> None:
    """Test if the property endpoint exists at all."""
    try:
        print("\n🔍 Direct test of /v1/properties endpoint:")
        print("-" * 50)
        
        client = ActualOpenToCloseAPI()
        
        # Try GET to see if properties endpoint exists
        try:
            response = client.get("/properties")
            print("✅ /v1/properties GET works - endpoint exists!")
            print(f"Response type: {type(response)}")
            if isinstance(response, list):
                print(f"Found {len(response)} properties")
            else:
                print(f"Response: {response}")
        except Exception as e:
            print(f"❌ /v1/properties GET failed: {e}")
            print("This confirms the endpoint might not exist in the current API")
            
    except Exception as e:
        print(f"❌ Direct test failed: {e}")


if __name__ == "__main__":
    # Test the actual working endpoints
    demo_actual_endpoints()
    
    # Test if properties endpoint exists at all
    test_property_endpoint_directly()