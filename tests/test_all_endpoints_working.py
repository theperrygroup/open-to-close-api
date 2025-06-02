#!/usr/bin/env python3
"""Test all endpoints systematically with the fixed base URL routing."""

import os

from dotenv import load_dotenv

from open_to_close import OpenToCloseAPI

load_dotenv()


def test_all_endpoints_comprehensive() -> None:
    """Test all endpoints with the fixed URL patterns."""
    try:
        client = OpenToCloseAPI()
        print("✅ Client initialized with fixed base URL routing")

        results = {}

        # Test all core endpoints
        endpoints_tests = [
            {
                "name": "Contacts",
                "client": client.contacts,
                "create_method": "create_contact",
                "data": {
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john.doe@example.com",
                    "phone": "555-123-4567",
                },
            },
            {
                "name": "Properties",
                "client": client.properties,
                "create_method": "create_property",
                "data": {
                    "title": "Beautiful Home",
                    "address": "123 Main Street",
                    "city": "Anytown",
                    "state": "UT",
                    "zip": "12345",
                },
            },
            {
                "name": "Agents",
                "client": client.agents,
                "create_method": "create_agent",
                "data": {
                    "first_name": "Jane",
                    "last_name": "Agent",
                    "email": "jane.agent@example.com",
                    "phone": "555-987-6543",
                },
            },
            {
                "name": "Teams",
                "client": client.teams,
                "create_method": "create_team",
                "data": {
                    "name": "Sales Team",
                    "description": "Main sales team",
                    "type": "sales",
                },
            },
            {
                "name": "Users",
                "client": client.users,
                "create_method": "create_user",
                "data": {
                    "first_name": "Bob",
                    "last_name": "User",
                    "email": "bob.user@example.com",
                    "role": "agent",
                },
            },
            {
                "name": "Tags",
                "client": client.tags,
                "create_method": "create_tag",
                "data": {
                    "name": "Hot Lead",
                    "color": "#FF0000",
                    "description": "High priority prospect",
                },
            },
        ]

        print("\n" + "=" * 80)
        print("🧪 COMPREHENSIVE ENDPOINT TESTING")
        print("=" * 80)

        for test in endpoints_tests:
            print(f"\n📋 Testing {test['name']}...")
            print(f"   Data: {test['data']}")

            try:
                # Get the create method and call it
                create_method = getattr(test["client"], test["create_method"])
                result = create_method(test["data"])

                print(f"   ✅ {test['name']} CREATE: SUCCESS!")
                if result and isinstance(result, dict) and result.get("id"):
                    print(f"   🎉 Created with ID: {result['id']}")
                    results[test["name"]] = {"success": True, "id": result.get("id")}
                else:
                    print(f"   📄 Response: {result}")
                    results[test["name"]] = {"success": True, "response": result}

            except Exception as e:
                print(f"   ❌ {test['name']} CREATE FAILED: {e}")
                results[test["name"]] = {"success": False, "error": str(e)}

        # Summary
        print(f"\n{'='*80}")
        print("📊 FINAL RESULTS SUMMARY")
        print("=" * 80)

        successful = []
        failed = []

        for endpoint, result in results.items():
            if result["success"]:
                successful.append(endpoint)
                status = "✅ SUCCESS"
                if result.get("id"):
                    status += f" (ID: {result['id']})"
            else:
                failed.append(endpoint)
                status = f"❌ FAILED: {result['error'][:50]}..."

            print(f"{endpoint:12} CREATE: {status}")

        print(f"\n🎯 ENDPOINT STATUS:")
        print(f"   ✅ Working: {len(successful)}/6 endpoints")
        print(f"   ❌ Failed:  {len(failed)}/6 endpoints")

        if successful:
            print(f"   🚀 Success List: {', '.join(successful)}")
        if failed:
            print(f"   🔧 Need Work: {', '.join(failed)}")

        # Calculate success rate
        success_rate = (len(successful) / len(endpoints_tests)) * 100
        print(f"\n🏆 SUCCESS RATE: {success_rate:.1f}%")

        if success_rate >= 80:
            print("🎉 EXCELLENT! Most endpoints are working!")
        elif success_rate >= 50:
            print("👍 GOOD! Majority of endpoints working!")
        else:
            print("🔧 NEEDS WORK: More endpoints need fixing")

    except Exception as e:
        print(f"❌ Test setup failed: {e}")


if __name__ == "__main__":
    test_all_endpoints_comprehensive()
