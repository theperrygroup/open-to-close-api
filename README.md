# Open To Close API Python Client

This is a Python client library for interacting with the Open To Close API. It provides an easy-to-use interface for the various API endpoints.

## Organization

- **Organization**: The Perry Group
- **Author**: John Perry
- **Email**: john@theperry.group

## Installation

```bash
pip install open-to-close-api
```

## Usage

First, ensure you have your Open To Close API key. You can set it as an environment variable `OPEN_TO_CLOSE_API_KEY` or pass it directly when initializing the client.

```python
from open_to_close_api.client import OpenToCloseAPI

# Initialize the client (loads API key from .env or environment variable by default)
client = OpenToCloseAPI()

# Or, provide the API key directly
# client = OpenToCloseAPI(api_key="YOUR_API_KEY")

# Example: List contacts
try:
    contacts = client.contacts.list_contacts()
    for contact in contacts:
        print(contact.get('first_name'), contact.get('last_name'))
except Exception as e:
    print(f"An error occurred: {e}")
```

## Available API Modules

The client provides access to the following API resources through dedicated helper classes:

*   `client.agents`
*   `client.contacts`
*   `client.properties`
*   `client.property_contacts`
*   `client.property_documents`
*   `client.property_emails`
*   `client.property_notes`
*   `client.property_tasks`
*   `client.teams`
*   `client.tags`
*   `client.users`

Each of these modules provides methods for `list`, `create`, `retrieve`, `update`, and `delete` operations where applicable and available through the API.

## Development

To set up for development:

1.  Clone the repository.
2.  Create a virtual environment: `python -m venv .venv`
3.  Activate the virtual environment: `source .venv/bin/activate` (or `\.venv\Scripts\activate` on Windows)
4.  Install dependencies: `pip install -r requirements.txt`
5.  Create a `.env` file in the root directory and add your API key:
    `OPEN_TO_CLOSE_API_KEY=your_actual_api_key_here`

## Testing

A basic test script `test_api.py` is included to verify connectivity and basic list operations for available endpoints.

```bash
python test_api.py
```

## Contributing

(Contribution guidelines to be added)

## License

(License information to be added, e.g., MIT License) 