#!/usr/bin/env python3
"""
Simple Property Creation Examples

This script demonstrates how easy it is to create properties with the
simplified Open To Close API wrapper.
"""

from open_to_close import PropertiesAPI


def main() -> None:
    """Demonstrate simplified property creation."""

    print("🏠 Open To Close - Simplified Property Creation")
    print("=" * 55)

    client = PropertiesAPI()

    # Example 1: Just a title (simplest possible)
    print("\n1. Creating property with just a title:")
    property1 = client.create_property("🏡 Beautiful Family Home")
    print(f"   ✅ Created Property ID: {property1['id']}")

    # Example 2: Buyer property with details
    print("\n2. Creating buyer property with details:")
    property2 = client.create_property(
        {
            "title": "🏰 Luxury Estate with Pool",
            "client_type": "Buyer",
            "status": "Active",
            "purchase_amount": 650000,
        }
    )
    print(f"   ✅ Created Property ID: {property2['id']}")

    # Example 3: Seller property
    print("\n3. Creating seller property:")
    property3 = client.create_property(
        {
            "title": "🏢 Downtown Condo for Sale",
            "client_type": "Seller",
            "status": "Pre-MLS",
            "purchase_amount": 425000,
        }
    )
    print(f"   ✅ Created Property ID: {property3['id']}")

    print(f"\n🎉 Successfully created 3 properties!")
    print(f"📚 See docs/property-creation-guide.md for more examples")


if __name__ == "__main__":
    main()
