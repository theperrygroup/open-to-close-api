import os
import requests
from dotenv import load_dotenv
from typing import Optional, Dict, Any

from .agents import AgentsAPI # Import AgentsAPI
from .contacts import ContactsAPI # Import ContactsAPI
# from .contact_roles import ContactRolesAPI # Removed
# from .file_roles import FileRolesAPI # Removed
from .properties import PropertiesAPI # Import PropertiesAPI
from .property_contacts import PropertyContactsAPI # Import PropertyContactsAPI
from .property_documents import PropertyDocumentsAPI # Import PropertyDocumentsAPI
from .property_emails import PropertyEmailsAPI # Import PropertyEmailsAPI
# from .property_fields import PropertyFieldsAPI # Removed
# from .property_field_sections import PropertyFieldSectionsAPI # Removed
# from .property_field_groups import PropertyFieldGroupsAPI # Removed
from .property_notes import PropertyNotesAPI # Import PropertyNotesAPI
from .property_tasks import PropertyTasksAPI # Import PropertyTasksAPI
# from .property_templates import PropertyTemplatesAPI # Removed
from .teams import TeamsAPI # Import TeamsAPI
# from .time_zones import TimeZonesAPI # Removed
from .tags import TagsAPI # Import TagsAPI
from .users import UsersAPI # Import UsersAPI
# from .events import EventsAPI # Removed
# from .transactions import TransactionsAPI # Removed

class OpenToCloseAPI:
    """A client for interacting with the Open To Close API."""

    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.opentoclose.com/v1") -> None:
        """Initializes the OpenToCloseAPI client.

        Args:
            api_key: The API key for authentication. If not provided, it will
                     attempt to load it from the OPEN_TO_CLOSE_API_KEY environment
                     variable.
            base_url: The base URL for the Open To Close API.
        """
        load_dotenv()
        self.api_key = api_key or os.getenv("OPEN_TO_CLOSE_API_KEY")
        if not self.api_key:
            raise ValueError("API key not provided and not found in environment variables.")
        self.base_url = base_url
        self.headers = {
            "Accept": "application/json",
        } # Simplified headers

        # Initialize resource-specific APIs
        self.agents = AgentsAPI(self)
        self.contacts = ContactsAPI(self)
        # self.contact_roles = ContactRolesAPI(self) # Removed
        # self.file_roles = FileRolesAPI(self) # Removed
        self.properties = PropertiesAPI(self)
        self.property_contacts = PropertyContactsAPI(self)
        self.property_documents = PropertyDocumentsAPI(self)
        self.property_emails = PropertyEmailsAPI(self)
        # self.property_fields = PropertyFieldsAPI(self) # Removed
        # self.property_field_sections = PropertyFieldSectionsAPI(self) # Removed
        # self.property_field_groups = PropertyFieldGroupsAPI(self) # Removed
        self.property_notes = PropertyNotesAPI(self)
        self.property_tasks = PropertyTasksAPI(self)
        # self.property_templates = PropertyTemplatesAPI(self) # Removed
        self.teams = TeamsAPI(self)
        # self.time_zones = TimeZonesAPI(self) # Removed
        self.tags = TagsAPI(self)
        self.users = UsersAPI(self)
        # self.events = EventsAPI(self) # Removed
        # self.transactions = TransactionsAPI(self) # Removed

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """Makes a request to the Open To Close API.

        Args:
            method: The HTTP method (GET, POST, PUT, DELETE).
            endpoint: The API endpoint (e.g., "/agents").
            params: Optional dictionary of query parameters.
            json_data: Optional dictionary of JSON data for the request body.

        Returns:
            The requests.Response object.

        Raises:
            requests.exceptions.RequestException: For network or HTTP errors.
        """
        url = f"{self.base_url}{endpoint}"
        
        # Add api_token to params for all requests
        if params is None:
            params = {}
        params["api_token"] = self.api_key

        response = requests.request(
            method, url, headers=self.headers, params=params, json=json_data
        )
        
        if response.status_code >= 400:
            try:
                error_details = response.json() # Try to get JSON error details
                print(f"API Error Details: {error_details}")
            except requests.exceptions.JSONDecodeError:
                print(f"API Error Text: {response.text}") # Fallback to text if not JSON
        
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        return response 