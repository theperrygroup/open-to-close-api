#!/usr/bin/env python3
"""
Example Background Agent for Open To Close API

This is a simple example showing how to create custom background tasks
using the Open To Close API library in a Docker container.
"""

import os
import time
from datetime import datetime
from typing import Dict

from open_to_close import OpenToCloseAPI
from open_to_close.exceptions import OpenToCloseAPIError


def simple_property_monitor() -> None:
    """Simple example of monitoring properties for changes."""
    print(f"🚀 Starting property monitor at {datetime.now()}")
    
    # Initialize API client
    api_key = os.getenv("OPEN_TO_CLOSE_API_KEY")
    if not api_key:
        print("❌ Error: OPEN_TO_CLOSE_API_KEY environment variable not set")
        return
    
    client = OpenToCloseAPI(api_key=api_key)
    
    try:
        # Get all properties
        print("📊 Fetching properties...")
        properties = client.properties.list_properties()
        print(f"✅ Found {len(properties)} properties")
        
        # Process each property
        for i, prop in enumerate(properties[:5]):  # Limit to first 5 for demo
            property_id = prop.get("id")
            address = prop.get("address", "Unknown address")
            
            print(f"🏠 Processing property {i+1}: {address}")
            
            if property_id:
                # Get property details
                try:
                    notes = client.property_notes.list_property_notes(int(property_id))
                    tasks = client.property_tasks.list_property_tasks(int(property_id))
                    
                    print(f"   📝 Notes: {len(notes)}")
                    print(f"   ✅ Tasks: {len(tasks)}")
                    
                    # Example: Check for overdue tasks
                    # In a real agent, you'd implement more sophisticated logic here
                    
                except Exception as e:
                    print(f"   ⚠️  Error processing property {property_id}: {e}")
            
            # Small delay to be respectful to the API
            time.sleep(0.5)
        
        print("✅ Property monitoring completed successfully")
        
    except OpenToCloseAPIError as e:
        print(f"❌ API Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def simple_contact_summary() -> None:
    """Simple example of generating a contact summary."""
    print(f"👥 Starting contact summary at {datetime.now()}")
    
    api_key = os.getenv("OPEN_TO_CLOSE_API_KEY")
    if not api_key:
        print("❌ Error: OPEN_TO_CLOSE_API_KEY environment variable not set")
        return
    
    client = OpenToCloseAPI(api_key=api_key)
    
    try:
        # Get all contacts
        print("📊 Fetching contacts...")
        contacts = client.contacts.list_contacts()
        print(f"✅ Found {len(contacts)} contacts")
        
        # Simple analysis
        contact_types: Dict[str, int] = {}
        for contact in contacts:
            contact_type = contact.get("contact_type", "Unknown")
            contact_types[contact_type] = contact_types.get(contact_type, 0) + 1
        
        print("📈 Contact breakdown by type:")
        for contact_type, count in contact_types.items():
            print(f"   {contact_type}: {count}")
        
        print("✅ Contact summary completed successfully")
        
    except OpenToCloseAPIError as e:
        print(f"❌ API Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def main() -> None:
    """Main function that runs different example tasks."""
    print("🐳 Open To Close API - Example Background Agent")
    print("=" * 50)
    
    # Run example tasks
    simple_property_monitor()
    print()  # Empty line for readability
    simple_contact_summary()
    
    print("=" * 50)
    print("🎉 Example agent run completed!")
    print()
    print("💡 Next steps:")
    print("   1. Customize this script for your specific needs")
    print("   2. Add error handling and retry logic")
    print("   3. Implement scheduling or continuous monitoring")
    print("   4. Add logging and metrics collection")
    print("   5. Create multiple specialized agents")


if __name__ == "__main__":
    main() 