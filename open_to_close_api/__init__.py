"""Open To Close API Python Client."""

from .client import OpenToCloseAPI
from .exceptions import (
    AuthenticationError,
    NetworkError,
    NotFoundError,
    OpenToCloseAPIError,
    RateLimitError,
    ServerError,
    ValidationError,
)

# Import service clients
from .agents import AgentsAPI
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

__version__ = "1.0.0"
__all__ = [
    "OpenToCloseAPI",
    # Service Clients
    "AgentsAPI",
    "ContactsAPI",
    "PropertiesAPI",
    "PropertyContactsAPI",
    "PropertyDocumentsAPI",
    "PropertyEmailsAPI",
    "PropertyNotesAPI",
    "PropertyTasksAPI",
    "TagsAPI",
    "TeamsAPI",
    "UsersAPI",
    # Exceptions
    "OpenToCloseAPIError",
    "AuthenticationError",
    "ValidationError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "NetworkError",
] 