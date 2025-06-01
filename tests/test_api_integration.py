from open_to_close.client import OpenToCloseAPI

# Initialize the API client
# The API key will be loaded from the .env file by the client's __init__ method
try:
    client = OpenToCloseAPI()
    print("API client initialized successfully.")

    # Test the "List agents" endpoint
    print("\nTesting GET /v1/agents (List agents)...")
    agents_response = client.agents.list_agents()

    # Check if the response is a list (or a dict with a 'data' key that is a list)
    if isinstance(agents_response, list):
        print(f"Found {len(agents_response)} agents.")
        if agents_response:
            print("First agent data:")
            print(agents_response[0])
    elif (
        isinstance(agents_response, dict)
        and "data" in agents_response
        and isinstance(agents_response["data"], list)
    ):
        print(f"Found {len(agents_response['data'])} agents.")
        if agents_response["data"]:
            print("First agent data:")
            print(agents_response["data"][0])
    else:
        print("Unexpected response format for agents list:")
        print(agents_response)

    print("\nAgent listing test completed.")

    # Test the "List contacts" endpoint
    print("\nTesting GET /v1/contacts (List contacts)...")
    contacts_response = client.contacts.list_contacts()

    if isinstance(contacts_response, list):
        print(f"Found {len(contacts_response)} contacts.")
        if contacts_response:
            print("First contact data:")
            print(contacts_response[0])
    elif (
        isinstance(contacts_response, dict)
        and "data" in contacts_response
        and isinstance(contacts_response["data"], list)
    ):
        print(f"Found {len(contacts_response['data'])} contacts.")
        if contacts_response["data"]:
            print("First contact data:")
            print(contacts_response["data"][0])
    else:
        print("Unexpected response format for contacts list:")
        print(contacts_response)

    print("\nContact listing test completed.")

    # Test the "List properties" endpoint
    print("\nTesting GET /v1/properties (List properties)...")
    properties_response = client.properties.list_properties()

    if isinstance(properties_response, list):
        print(f"Found {len(properties_response)} properties.")
        if properties_response:
            print("First property data:")
            print(properties_response[0])
    elif (
        isinstance(properties_response, dict)
        and "data" in properties_response
        and isinstance(properties_response["data"], list)
    ):
        print(f"Found {len(properties_response['data'])} properties.")
        if properties_response["data"]:
            print("First property data:")
            print(properties_response["data"][0])
    else:
        print("Unexpected response format for properties list:")
        print(properties_response)

    print("\nProperty listing test completed.")

    # Test the "List property contacts" endpoint
    print(
        "\nTesting GET /v1/properties/{property_id}/contacts (List property contacts)..."
    )
    # Get a property ID from the properties list if available
    property_id_for_contacts = None
    if isinstance(properties_response, list) and properties_response:
        property_id_for_contacts = properties_response[0].get("id")
    elif (
        isinstance(properties_response, dict)
        and "data" in properties_response
        and properties_response["data"]
    ):
        property_id_for_contacts = properties_response["data"][0].get("id")
    if property_id_for_contacts:
        property_contacts_response = client.property_contacts.list_property_contacts(
            property_id=property_id_for_contacts
        )
        if isinstance(property_contacts_response, list):
            print(
                f"Found {len(property_contacts_response)} contacts for property {property_id_for_contacts}."
            )
            if property_contacts_response:
                print("First property contact data:")
                print(property_contacts_response[0])
        elif (
            isinstance(property_contacts_response, dict)
            and "data" in property_contacts_response
            and isinstance(property_contacts_response["data"], list)
        ):
            print(
                f"Found {len(property_contacts_response['data'])} contacts for property {property_id_for_contacts}."
            )
            if property_contacts_response["data"]:
                print("First property contact data:")
                print(property_contacts_response["data"][0])
        else:
            print(
                f"Unexpected response format for property contacts list for property {property_id_for_contacts}:"
            )
            print(property_contacts_response)
    else:
        print("Skipping List property contacts test as no property_id was found.")

    print("\nProperty contacts listing test completed.")

    # Test the "List property documents" endpoint
    print(
        "\nTesting GET /v1/properties/{property_id}/documents (List property documents)..."
    )
    property_id_for_documents = property_id_for_contacts  # Use same property ID
    if property_id_for_documents:
        property_documents_response = client.property_documents.list_property_documents(
            property_id=property_id_for_documents
        )
        if isinstance(property_documents_response, list):
            print(
                f"Found {len(property_documents_response)} documents for property {property_id_for_documents}."
            )
            if property_documents_response:
                print("First property document data:")
                print(property_documents_response[0])
        elif (
            isinstance(property_documents_response, dict)
            and "data" in property_documents_response
            and isinstance(property_documents_response["data"], list)
        ):
            print(
                f"Found {len(property_documents_response['data'])} documents for property {property_id_for_documents}."
            )
            if property_documents_response["data"]:
                print("First property document data:")
                print(property_documents_response["data"][0])
        else:
            print(
                f"Unexpected response format for property documents list for property {property_id_for_documents}:"
            )
            print(property_documents_response)
    else:
        print("Skipping List property documents test as no property_id was found.")

    print("\nProperty documents listing test completed.")

    # Test the "List property emails" endpoint
    print("\nTesting GET /v1/properties/{property_id}/emails (List property emails)...")
    property_id_for_emails = property_id_for_contacts  # Use same property ID
    if property_id_for_emails:
        property_emails_response = client.property_emails.list_property_emails(
            property_id=property_id_for_emails
        )
        if isinstance(property_emails_response, list):
            print(
                f"Found {len(property_emails_response)} emails for property {property_id_for_emails}."
            )
            if property_emails_response:
                print("First property email data:")
                print(property_emails_response[0])
        elif (
            isinstance(property_emails_response, dict)
            and "data" in property_emails_response
            and isinstance(property_emails_response["data"], list)
        ):
            print(
                f"Found {len(property_emails_response['data'])} emails for property {property_id_for_emails}."
            )
            if property_emails_response["data"]:
                print("First property email data:")
                print(property_emails_response["data"][0])
        else:
            print(
                f"Unexpected response format for property emails list for property {property_id_for_emails}:"
            )
            print(property_emails_response)
    else:
        print("Skipping List property emails test as no property_id was found.")

    print("\nProperty emails listing test completed.")

    # Test the "List property notes" endpoint
    print("\nTesting GET /v1/properties/{property_id}/notes (List property notes)...")
    property_id_for_notes = property_id_for_contacts  # Use same property ID
    if property_id_for_notes:
        property_notes_response = client.property_notes.list_property_notes(
            property_id=property_id_for_notes
        )
        if isinstance(property_notes_response, list):
            print(
                f"Found {len(property_notes_response)} notes for property {property_id_for_notes}."
            )
            if property_notes_response:
                print("First property note data:")
                print(property_notes_response[0])
        elif (
            isinstance(property_notes_response, dict)
            and "data" in property_notes_response
            and isinstance(property_notes_response["data"], list)
        ):
            print(
                f"Found {len(property_notes_response['data'])} notes for property {property_id_for_notes}."
            )
            if property_notes_response["data"]:
                print("First property note data:")
                print(property_notes_response["data"][0])
        else:
            print(
                f"Unexpected response format for property notes list for property {property_id_for_notes}:"
            )
            print(property_notes_response)
    else:
        print("Skipping List property notes test as no property_id was found.")
    print("\nProperty notes listing test completed.")

    # Test the "List property tasks" endpoint
    print("\nTesting GET /v1/properties/{property_id}/tasks (List property tasks)...")
    property_id_for_tasks = property_id_for_contacts  # Use same property ID
    if property_id_for_tasks:
        property_tasks_response = client.property_tasks.list_property_tasks(
            property_id=property_id_for_tasks
        )
        if isinstance(property_tasks_response, list):
            print(
                f"Found {len(property_tasks_response)} tasks for property {property_id_for_tasks}."
            )
            if property_tasks_response:
                print("First property task data:")
                print(property_tasks_response[0])
        elif (
            isinstance(property_tasks_response, dict)
            and "data" in property_tasks_response
            and isinstance(property_tasks_response["data"], list)
        ):
            print(
                f"Found {len(property_tasks_response['data'])} tasks for property {property_id_for_tasks}."
            )
            if property_tasks_response["data"]:
                print("First property task data:")
                print(property_tasks_response["data"][0])
        else:
            print(
                f"Unexpected response format for property tasks list for property {property_id_for_tasks}:"
            )
            print(property_tasks_response)
    else:
        print("Skipping List property tasks test as no property_id was found.")
    print("\nProperty tasks listing test completed.")

    # Test the "List teams" endpoint
    print("\nTesting GET /v1/teams (List teams)...")
    teams_response = client.teams.list_teams()
    if isinstance(teams_response, list):
        print(f"Found {len(teams_response)} teams.")
        if teams_response:
            print("First team data:")
            print(teams_response[0])
    elif (
        isinstance(teams_response, dict)
        and "data" in teams_response
        and isinstance(teams_response["data"], list)
    ):
        print(f"Found {len(teams_response['data'])} teams.")
        if teams_response["data"]:
            print("First team data:")
            print(teams_response["data"][0])
    else:
        print("Unexpected response format for teams list:")
        print(teams_response)
    print("\nTeams listing test completed.")

    # Test the "List tags" endpoint
    print("\nTesting GET /v1/tags (List tags)...")
    tags_response = client.tags.list_tags()
    if isinstance(tags_response, list):
        print(f"Found {len(tags_response)} tags.")
        if tags_response:
            print("First tag data:")
            print(tags_response[0])
    elif (
        isinstance(tags_response, dict)
        and "data" in tags_response
        and isinstance(tags_response["data"], list)
    ):
        print(f"Found {len(tags_response['data'])} tags.")
        if tags_response["data"]:
            print("First tag data:")
            print(tags_response["data"][0])
    else:
        print("Unexpected response format for tags list:")
        print(tags_response)
    print("\nTags listing test completed.")

    # Test the "List users" endpoint
    print("\nTesting GET /v1/users (List users)...")
    users_response = client.users.list_users()
    if isinstance(users_response, list):
        print(f"Found {len(users_response)} users.")
        if users_response:
            print("First user data:")
            print(users_response[0])
    elif (
        isinstance(users_response, dict)
        and "data" in users_response
        and isinstance(users_response["data"], list)
    ):
        print(f"Found {len(users_response['data'])} users.")
        if users_response["data"]:
            print("First user data:")
            print(users_response["data"][0])
    else:
        print("Unexpected response format for users list:")
        print(users_response)
    print("\nUsers listing test completed.")

except ValueError as e:
    print(f"Error initializing API client: {e}")
except Exception as e:
    print(f"An error occurred during the API test: {e}")
