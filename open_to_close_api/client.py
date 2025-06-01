from typing import Optional

from .agents import AgentsAPI
from .base_client import DEFAULT_BASE_URL
from .contacts import ContactsAPI
from .properties import PropertiesAPI
from .property_contacts import PropertyContactsAPI
from .property_documents import PropertyDocumentsAPI
from .property_emails import PropertyEmailsAPI
from .property_notes import PropertyNotesAPI
from .property_tasks import PropertyTasksAPI
from .tags import TagsAPI
from .teams import TeamsAPI
from .users import UsersAPI


class OpenToCloseAPI:
    """Main client for Open To Close API.

    This client provides access to all Open To Close API endpoints through
    service-specific clients using a composition pattern with lazy initialization.

    Example:
        ```python
        from open_to_close_api import OpenToCloseAPI

        # Initialize with API key from environment variable
        client = OpenToCloseAPI()

        # Or provide API key directly
        client = OpenToCloseAPI(api_key="your_api_key_here")

        # Use service endpoints
        agents = client.agents.list_agents()
        agent = client.agents.retrieve_agent(1)

        # Create a new contact
        contact = client.contacts.create_contact({
            "name": "John Doe",
            "email": "john@example.com"
        })
        ```
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the client.

        Args:
            api_key: API key for authentication. If not provided, it will
                     attempt to load it from the OPEN_TO_CLOSE_API_KEY environment
                     variable.
            base_url: Base URL for the Open To Close API. Defaults to
                      https://api.opentoclose.com/v1

        Raises:
            AuthenticationError: If API key is not provided and not found in environment
        """
        self._api_key = api_key
        self._base_url = base_url or DEFAULT_BASE_URL

        # Lazy initialization of service clients
        self._agents: Optional[AgentsAPI] = None
        self._contacts: Optional[ContactsAPI] = None
        self._properties: Optional[PropertiesAPI] = None
        self._property_contacts: Optional[PropertyContactsAPI] = None
        self._property_documents: Optional[PropertyDocumentsAPI] = None
        self._property_emails: Optional[PropertyEmailsAPI] = None
        self._property_notes: Optional[PropertyNotesAPI] = None
        self._property_tasks: Optional[PropertyTasksAPI] = None
        self._tags: Optional[TagsAPI] = None
        self._teams: Optional[TeamsAPI] = None
        self._users: Optional[UsersAPI] = None

    @property
    def agents(self) -> AgentsAPI:
        """Access to agents endpoints.

        Returns:
            AgentsAPI instance for managing agents
        """
        if self._agents is None:
            self._agents = AgentsAPI(api_key=self._api_key, base_url=self._base_url)
        return self._agents

    @property
    def contacts(self) -> ContactsAPI:
        """Access to contacts endpoints.

        Returns:
            ContactsAPI instance for managing contacts
        """
        if self._contacts is None:
            self._contacts = ContactsAPI(api_key=self._api_key, base_url=self._base_url)
        return self._contacts

    @property
    def properties(self) -> PropertiesAPI:
        """Access to properties endpoints.

        Returns:
            PropertiesAPI instance for managing properties
        """
        if self._properties is None:
            self._properties = PropertiesAPI(
                api_key=self._api_key, base_url=self._base_url
            )
        return self._properties

    @property
    def property_contacts(self) -> PropertyContactsAPI:
        """Access to property contacts endpoints.

        Returns:
            PropertyContactsAPI instance for managing property contacts
        """
        if self._property_contacts is None:
            self._property_contacts = PropertyContactsAPI(
                api_key=self._api_key, base_url=self._base_url
            )
        return self._property_contacts

    @property
    def property_documents(self) -> PropertyDocumentsAPI:
        """Access to property documents endpoints.

        Returns:
            PropertyDocumentsAPI instance for managing property documents
        """
        if self._property_documents is None:
            self._property_documents = PropertyDocumentsAPI(
                api_key=self._api_key, base_url=self._base_url
            )
        return self._property_documents

    @property
    def property_emails(self) -> PropertyEmailsAPI:
        """Access to property emails endpoints.

        Returns:
            PropertyEmailsAPI instance for managing property emails
        """
        if self._property_emails is None:
            self._property_emails = PropertyEmailsAPI(
                api_key=self._api_key, base_url=self._base_url
            )
        return self._property_emails

    @property
    def property_notes(self) -> PropertyNotesAPI:
        """Access to property notes endpoints.

        Returns:
            PropertyNotesAPI instance for managing property notes
        """
        if self._property_notes is None:
            self._property_notes = PropertyNotesAPI(
                api_key=self._api_key, base_url=self._base_url
            )
        return self._property_notes

    @property
    def property_tasks(self) -> PropertyTasksAPI:
        """Access to property tasks endpoints.

        Returns:
            PropertyTasksAPI instance for managing property tasks
        """
        if self._property_tasks is None:
            self._property_tasks = PropertyTasksAPI(
                api_key=self._api_key, base_url=self._base_url
            )
        return self._property_tasks

    @property
    def tags(self) -> TagsAPI:
        """Access to tags endpoints.

        Returns:
            TagsAPI instance for managing tags
        """
        if self._tags is None:
            self._tags = TagsAPI(api_key=self._api_key, base_url=self._base_url)
        return self._tags

    @property
    def teams(self) -> TeamsAPI:
        """Access to teams endpoints.

        Returns:
            TeamsAPI instance for managing teams
        """
        if self._teams is None:
            self._teams = TeamsAPI(api_key=self._api_key, base_url=self._base_url)
        return self._teams

    @property
    def users(self) -> UsersAPI:
        """Access to users endpoints.

        Returns:
            UsersAPI instance for managing users
        """
        if self._users is None:
            self._users = UsersAPI(api_key=self._api_key, base_url=self._base_url)
        return self._users
