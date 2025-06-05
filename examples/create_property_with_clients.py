#!/usr/bin/env python3
"""
Example: Creating a property and linking clients to it.

This example demonstrates the complete workflow for:
1. Creating multiple contacts (clients)
2. Creating a property
3. Linking the contacts to the property
4. Verifying the associations were created
"""

from typing import Any, Dict, List

from open_to_close import OpenToCloseAPI


def create_property_with_clients() -> Dict[str, Any]:
    """Create a property with linked clients and return the results.

    Returns:
        Dictionary containing the created property, contacts, and associations
    """
    # Initialize the API client
    client = OpenToCloseAPI()

    # Step 1: Create contacts
    print("Creating contacts...")
    import time

    timestamp = int(time.time())

    contacts_data = [
        {
            "first_name": "John",
            "last_name": "Smith",
            "email": f"john.smith.{timestamp}@example.com",
            "phone": "+1-555-123-4567",
        },
        {
            "first_name": "Sarah",
            "last_name": "Johnson",
            "email": f"sarah.johnson.{timestamp}@example.com",
            "phone": "+1-555-987-6543",
        },
        {
            "first_name": "Michael",
            "last_name": "Williams",
            "email": f"michael.williams.{timestamp}@example.com",
            "phone": "+1-555-555-1212",
        },
    ]

    created_contacts = []
    for contact_data in contacts_data:
        contact = client.contacts.create_contact(contact_data)
        created_contacts.append(contact)
        print(
            f"✅ Created contact: {contact_data['first_name']} {contact_data['last_name']} (ID: {contact['id']})"
        )

    # Step 2: Create property
    print("\nCreating property...")
    property_data = {
        "title": "Beautiful Family Home - 123 Maple Street",
        "client_type": "Buyer",
        "status": "Active",
        "purchase_amount": 450000,
    }

    property_record = client.properties.create_property(property_data)
    property_id = property_record["id"]
    print(f"✅ Created property: {property_data['title']} (ID: {property_id})")

    # Step 3: Link contacts to property
    print("\nLinking contacts to property...")
    property_contacts = []
    for contact in created_contacts:
        contact_id = contact["id"]
        contact_name = (
            f"{contact.get('first_name', '')} {contact.get('last_name', '')}".strip()
        )

        # Create the property-contact association
        link_data = {"contact_id": contact_id}
        property_contact = client.property_contacts.create_property_contact(
            property_id, link_data
        )
        property_contacts.append(property_contact)

        association_id = property_contact["id"]
        print(
            f"✅ Linked {contact_name} to property (Association ID: {association_id})"
        )

    # Step 4: Verify links were created
    print("\nVerifying contact links...")
    linked_contacts = client.property_contacts.list_property_contacts(property_id)

    expected_contact_ids = {contact["id"] for contact in created_contacts}
    actual_contact_ids = {pc["contact"]["id"] for pc in linked_contacts}

    if expected_contact_ids == actual_contact_ids:
        print(
            f"✅ VERIFICATION PASSED: All {len(expected_contact_ids)} contacts successfully linked!"
        )
    else:
        print(
            f"❌ VERIFICATION FAILED: Expected {expected_contact_ids}, got {actual_contact_ids}"
        )

    return {
        "property": property_record,
        "contacts": created_contacts,
        "property_contacts": property_contacts,
        "verification_passed": expected_contact_ids == actual_contact_ids,
    }


if __name__ == "__main__":
    print("=== Creating Property with Linked Clients ===\n")

    try:
        result = create_property_with_clients()

        print("\n=== SUMMARY ===")
        print(f"Property ID: {result['property']['id']}")
        print(f"Contacts created: {len(result['contacts'])}")
        print(f"Links created: {len(result['property_contacts'])}")
        print(
            f"Verification: {'PASSED' if result['verification_passed'] else 'FAILED'}"
        )

        if result["verification_passed"]:
            print("\n🎉 SUCCESS! Property and client linking completed successfully!")
        else:
            print("\n❌ Some issues occurred during the process.")

    except Exception as e:
        print(f"\n❌ Error: {e}")
