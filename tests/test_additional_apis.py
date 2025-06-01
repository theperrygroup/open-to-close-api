"""Tests for additional API endpoints with low coverage."""

from unittest.mock import Mock, patch

import pytest
import requests

from open_to_close import OpenToCloseAPI


@pytest.fixture
def client() -> OpenToCloseAPI:
    """Create a test client."""
    return OpenToCloseAPI(api_key="test_key")


@pytest.fixture
def mock_response() -> Mock:
    """Create a mock response."""
    response = Mock(spec=requests.Response)
    response.status_code = 200
    response.json.return_value = {"id": 1, "name": "Test"}
    return response


@pytest.fixture
def mock_list_response() -> Mock:
    """Create a mock list response."""
    response = Mock(spec=requests.Response)
    response.status_code = 200
    response.json.return_value = [{"id": 1, "name": "Test Item"}]
    return response


@pytest.fixture
def mock_delete_response() -> Mock:
    """Create a mock delete response."""
    response = Mock(spec=requests.Response)
    response.status_code = 204
    response.json.return_value = {}
    return response


class TestTagsAPI:
    """Test TagsAPI functionality."""

    def test_tags_initialization(self, client: OpenToCloseAPI) -> None:
        """Test that tags API can be initialized."""
        tags = client.tags
        assert tags is not None
        assert hasattr(tags, "list_tags")
        assert hasattr(tags, "create_tag")
        assert hasattr(tags, "retrieve_tag")
        assert hasattr(tags, "update_tag")
        assert hasattr(tags, "delete_tag")

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_tags(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_list_response: Mock
    ) -> None:
        """Test listing tags."""
        mock_request.return_value = mock_list_response

        tags = client.tags.list_tags()

        assert isinstance(tags, list)
        assert len(tags) == 1
        assert tags[0]["id"] == 1
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_tags_with_params(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_list_response: Mock
    ) -> None:
        """Test listing tags with parameters."""
        mock_request.return_value = mock_list_response

        tags = client.tags.list_tags(params={"limit": 50})

        assert isinstance(tags, list)
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_tags_dict_response(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test listing tags with dict response containing data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": [{"id": 1, "name": "Test Tag"}]}
        mock_request.return_value = response

        tags = client.tags.list_tags()

        assert isinstance(tags, list)
        assert len(tags) == 1
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_create_tag(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test creating a tag."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {
            "id": 1,
            "name": "VIP Client",
            "color": "#ff0000",
        }

        tag_data = {"name": "VIP Client", "color": "#ff0000"}
        tag = client.tags.create_tag(tag_data)

        assert isinstance(tag, dict)
        assert tag.get("id") == 1
        assert tag.get("name") == "VIP Client"
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_create_tag_dict_response(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test creating a tag with dict response containing data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": {"id": 1, "name": "Test Tag"}}
        mock_request.return_value = response

        tag_data = {"name": "Test Tag"}
        tag = client.tags.create_tag(tag_data)

        assert isinstance(tag, dict)
        assert tag.get("id") == 1
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_retrieve_tag(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test retrieving a tag."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"id": 123, "name": "VIP Client"}

        tag = client.tags.retrieve_tag(123)

        assert isinstance(tag, dict)
        assert tag.get("id") == 123
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_retrieve_tag_dict_response(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test retrieving a tag with dict response containing data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": {"id": 123, "name": "Test Tag"}}
        mock_request.return_value = response

        tag = client.tags.retrieve_tag(123)

        assert isinstance(tag, dict)
        assert tag.get("id") == 123
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_update_tag(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test updating a tag."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {
            "id": 123,
            "name": "Premium Client",
            "color": "#00ff00",
        }

        update_data = {"name": "Premium Client", "color": "#00ff00"}
        tag = client.tags.update_tag(123, update_data)

        assert isinstance(tag, dict)
        assert tag.get("id") == 123
        assert tag.get("name") == "Premium Client"
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_delete_tag(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_delete_response: Mock
    ) -> None:
        """Test deleting a tag."""
        mock_request.return_value = mock_delete_response

        result = client.tags.delete_tag(123)

        assert isinstance(result, dict)
        mock_request.assert_called_once()


class TestTeamsAPI:
    """Test TeamsAPI functionality."""

    def test_teams_initialization(self, client: OpenToCloseAPI) -> None:
        """Test that teams API can be initialized."""
        teams = client.teams
        assert teams is not None
        assert hasattr(teams, "list_teams")
        assert hasattr(teams, "create_team")
        assert hasattr(teams, "retrieve_team")
        assert hasattr(teams, "update_team")
        assert hasattr(teams, "delete_team")

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_teams(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_list_response: Mock
    ) -> None:
        """Test listing teams."""
        mock_request.return_value = mock_list_response

        teams = client.teams.list_teams()

        assert isinstance(teams, list)
        assert len(teams) == 1
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_teams_with_params(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_list_response: Mock
    ) -> None:
        """Test listing teams with parameters."""
        mock_request.return_value = mock_list_response

        teams = client.teams.list_teams(params={"limit": 50})

        assert isinstance(teams, list)
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_create_team(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test creating a team."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {
            "id": 1,
            "name": "Sales Team",
            "description": "Primary sales team",
        }

        team_data = {"name": "Sales Team", "description": "Primary sales team"}
        team = client.teams.create_team(team_data)

        assert isinstance(team, dict)
        assert team.get("id") == 1
        assert team.get("name") == "Sales Team"
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_retrieve_team(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test retrieving a team."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"id": 123, "name": "Sales Team"}

        team = client.teams.retrieve_team(123)

        assert isinstance(team, dict)
        assert team.get("id") == 123
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_update_team(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test updating a team."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {
            "id": 123,
            "name": "Marketing Team",
            "description": "Updated team",
        }

        update_data = {"name": "Marketing Team", "description": "Updated team"}
        team = client.teams.update_team(123, update_data)

        assert isinstance(team, dict)
        assert team.get("id") == 123
        assert team.get("name") == "Marketing Team"
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_delete_team(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_delete_response: Mock
    ) -> None:
        """Test deleting a team."""
        mock_request.return_value = mock_delete_response

        result = client.teams.delete_team(123)

        assert isinstance(result, dict)
        mock_request.assert_called_once()


class TestUsersAPI:
    """Test UsersAPI functionality."""

    def test_users_initialization(self, client: OpenToCloseAPI) -> None:
        """Test that users API can be initialized."""
        users = client.users
        assert users is not None
        assert hasattr(users, "list_users")
        assert hasattr(users, "create_user")
        assert hasattr(users, "retrieve_user")
        assert hasattr(users, "update_user")
        assert hasattr(users, "delete_user")

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_users(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_list_response: Mock
    ) -> None:
        """Test listing users."""
        mock_request.return_value = mock_list_response

        users = client.users.list_users()

        assert isinstance(users, list)
        assert len(users) == 1
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_users_with_params(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_list_response: Mock
    ) -> None:
        """Test listing users with parameters."""
        mock_request.return_value = mock_list_response

        users = client.users.list_users(params={"limit": 25, "active": True})

        assert isinstance(users, list)
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_create_user(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test creating a user."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {
            "id": 1,
            "name": "John User",
            "email": "john@example.com",
            "role": "agent",
        }

        user_data = {
            "name": "John User",
            "email": "john@example.com",
            "role": "agent",
            "password": "secure_password",
        }
        user = client.users.create_user(user_data)

        assert isinstance(user, dict)
        assert user.get("id") == 1
        assert user.get("email") == "john@example.com"
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_retrieve_user(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test retrieving a user."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {
            "id": 123,
            "name": "John User",
            "email": "john@example.com",
        }

        user = client.users.retrieve_user(123)

        assert isinstance(user, dict)
        assert user.get("id") == 123
        assert user.get("email") == "john@example.com"
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_update_user(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test updating a user."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {
            "id": 123,
            "name": "Jane User",
            "role": "admin",
        }

        update_data = {"name": "Jane User", "role": "admin"}
        user = client.users.update_user(123, update_data)

        assert isinstance(user, dict)
        assert user.get("id") == 123
        assert user.get("name") == "Jane User"
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_delete_user(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_delete_response: Mock
    ) -> None:
        """Test deleting a user."""
        mock_request.return_value = mock_delete_response

        result = client.users.delete_user(123)

        assert isinstance(result, dict)
        mock_request.assert_called_once()


class TestPropertyEmailsAPI:
    """Test PropertyEmailsAPI functionality."""

    def test_property_emails_initialization(self, client: OpenToCloseAPI) -> None:
        """Test that property emails API can be initialized."""
        property_emails = client.property_emails
        assert property_emails is not None
        assert hasattr(property_emails, "list_property_emails")
        assert hasattr(property_emails, "create_property_email")
        assert hasattr(property_emails, "retrieve_property_email")
        assert hasattr(property_emails, "update_property_email")
        assert hasattr(property_emails, "delete_property_email")

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_property_emails(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_list_response: Mock
    ) -> None:
        """Test listing property emails."""
        mock_request.return_value = mock_list_response

        emails = client.property_emails.list_property_emails(1)

        assert isinstance(emails, list)
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_property_emails_with_params(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_list_response: Mock
    ) -> None:
        """Test listing property emails with parameters."""
        mock_request.return_value = mock_list_response

        emails = client.property_emails.list_property_emails(1, params={"limit": 10})

        assert isinstance(emails, list)
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_property_emails_dict_response(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test listing property emails with dict response containing data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": [{"id": 1, "subject": "Test Email"}]}
        mock_request.return_value = response

        emails = client.property_emails.list_property_emails(1)

        assert isinstance(emails, list)
        assert len(emails) == 1
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_property_emails_dict_response_no_data(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test listing property emails with dict response but no data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": "not a list"}
        mock_request.return_value = response

        emails = client.property_emails.list_property_emails(1)

        assert isinstance(emails, list)
        assert len(emails) == 0
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_property_emails_unexpected_response(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test listing property emails with unexpected response format."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = "unexpected string response"
        mock_request.return_value = response

        emails = client.property_emails.list_property_emails(1)

        assert isinstance(emails, list)
        assert len(emails) == 0
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_create_property_email(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test creating a property email."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {
            "id": 1,
            "subject": "Property Update",
            "body": "Email content",
            "property_id": 1,
        }

        email_data = {
            "subject": "Property Update",
            "body": "Email content",
            "to": "client@example.com",
        }
        email = client.property_emails.create_property_email(1, email_data)

        assert isinstance(email, dict)
        assert email.get("id") == 1
        assert email.get("subject") == "Property Update"
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_create_property_email_dict_response(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test creating a property email with dict response containing data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": {"id": 1, "subject": "Test Email"}}
        mock_request.return_value = response

        email_data = {"subject": "Test Email"}
        email = client.property_emails.create_property_email(1, email_data)

        assert isinstance(email, dict)
        assert email.get("id") == 1
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_create_property_email_dict_response_no_data(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test creating a property email with dict response but no valid data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": "not a dict"}
        mock_request.return_value = response

        email_data = {"subject": "Test Email"}
        email = client.property_emails.create_property_email(1, email_data)

        assert isinstance(email, dict)
        assert len(email) == 0
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_create_property_email_unexpected_response(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test creating a property email with unexpected response format."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = "unexpected string response"
        mock_request.return_value = response

        email_data = {"subject": "Test Email"}
        email = client.property_emails.create_property_email(1, email_data)

        assert isinstance(email, dict)
        assert len(email) == 0
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_retrieve_property_email(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test retrieving a property email."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"id": 123, "subject": "Property Update"}

        email = client.property_emails.retrieve_property_email(1, 123)

        assert isinstance(email, dict)
        assert email.get("id") == 123
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_retrieve_property_email_dict_response(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test retrieving a property email with dict response containing data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": {"id": 123, "subject": "Test Email"}}
        mock_request.return_value = response

        email = client.property_emails.retrieve_property_email(1, 123)

        assert isinstance(email, dict)
        assert email.get("id") == 123
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_update_property_email(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test updating a property email."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"id": 123, "subject": "Updated Subject"}

        update_data = {"subject": "Updated Subject"}
        email = client.property_emails.update_property_email(1, 123, update_data)

        assert isinstance(email, dict)
        assert email.get("id") == 123
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_update_property_email_dict_response(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test updating a property email with dict response containing data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": {"id": 123, "subject": "Updated Email"}}
        mock_request.return_value = response

        update_data = {"subject": "Updated Email"}
        email = client.property_emails.update_property_email(1, 123, update_data)

        assert isinstance(email, dict)
        assert email.get("id") == 123
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_delete_property_email(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_delete_response: Mock
    ) -> None:
        """Test deleting a property email."""
        mock_request.return_value = mock_delete_response

        result = client.property_emails.delete_property_email(1, 123)

        assert isinstance(result, dict)
        mock_request.assert_called_once()


class TestPropertyNotesAPI:
    """Test PropertyNotesAPI functionality."""

    def test_property_notes_initialization(self, client: OpenToCloseAPI) -> None:
        """Test that property notes API can be initialized."""
        property_notes = client.property_notes
        assert property_notes is not None
        assert hasattr(property_notes, "list_property_notes")
        assert hasattr(property_notes, "create_property_note")
        assert hasattr(property_notes, "retrieve_property_note")
        assert hasattr(property_notes, "update_property_note")
        assert hasattr(property_notes, "delete_property_note")

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_property_notes(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_list_response: Mock
    ) -> None:
        """Test listing property notes."""
        mock_request.return_value = mock_list_response

        notes = client.property_notes.list_property_notes(1)

        assert isinstance(notes, list)
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_property_notes_dict_response(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test listing property notes with dict response containing data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": [{"id": 1, "title": "Test Note"}]}
        mock_request.return_value = response

        notes = client.property_notes.list_property_notes(1)

        assert isinstance(notes, list)
        assert len(notes) == 1
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_property_notes_dict_response_no_data(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test listing property notes with dict response but no data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": "not a list"}
        mock_request.return_value = response

        notes = client.property_notes.list_property_notes(1)

        assert isinstance(notes, list)
        assert len(notes) == 0
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_create_property_note(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test creating a property note."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {
            "id": 1,
            "title": "Important Note",
            "content": "Note content",
            "property_id": 1,
        }

        note_data = {"title": "Important Note", "content": "Note content"}
        note = client.property_notes.create_property_note(1, note_data)

        assert isinstance(note, dict)
        assert note.get("id") == 1
        assert note.get("title") == "Important Note"
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_create_property_note_dict_response(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test creating a property note with dict response containing data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": {"id": 1, "title": "Test Note"}}
        mock_request.return_value = response

        note_data = {"title": "Test Note"}
        note = client.property_notes.create_property_note(1, note_data)

        assert isinstance(note, dict)
        assert note.get("id") == 1
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_create_property_note_dict_response_no_data(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test creating a property note with dict response but no valid data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": "not a dict"}
        mock_request.return_value = response

        note_data = {"title": "Test Note"}
        note = client.property_notes.create_property_note(1, note_data)

        assert isinstance(note, dict)
        assert len(note) == 0
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_retrieve_property_note(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test retrieving a property note."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"id": 123, "title": "Important Note"}

        note = client.property_notes.retrieve_property_note(1, 123)

        assert isinstance(note, dict)
        assert note.get("id") == 123
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_retrieve_property_note_dict_response(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test retrieving a property note with dict response containing data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": {"id": 123, "title": "Test Note"}}
        mock_request.return_value = response

        note = client.property_notes.retrieve_property_note(1, 123)

        assert isinstance(note, dict)
        assert note.get("id") == 123
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_update_property_note(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test updating a property note."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"id": 123, "title": "Updated Note"}

        update_data = {"title": "Updated Note"}
        note = client.property_notes.update_property_note(1, 123, update_data)

        assert isinstance(note, dict)
        assert note.get("id") == 123
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_update_property_note_dict_response(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test updating a property note with dict response containing data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": {"id": 123, "title": "Updated Note"}}
        mock_request.return_value = response

        update_data = {"title": "Updated Note"}
        note = client.property_notes.update_property_note(1, 123, update_data)

        assert isinstance(note, dict)
        assert note.get("id") == 123
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_delete_property_note(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_delete_response: Mock
    ) -> None:
        """Test deleting a property note."""
        mock_request.return_value = mock_delete_response

        result = client.property_notes.delete_property_note(1, 123)

        assert isinstance(result, dict)
        mock_request.assert_called_once()


class TestPropertyDocumentsAPI:
    """Test PropertyDocumentsAPI functionality."""

    def test_property_documents_initialization(self, client: OpenToCloseAPI) -> None:
        """Test that property documents API can be initialized."""
        property_documents = client.property_documents
        assert property_documents is not None
        assert hasattr(property_documents, "list_property_documents")
        assert hasattr(property_documents, "create_property_document")
        assert hasattr(property_documents, "retrieve_property_document")
        assert hasattr(property_documents, "update_property_document")
        assert hasattr(property_documents, "delete_property_document")

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_property_documents(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_list_response: Mock
    ) -> None:
        """Test listing property documents."""
        mock_request.return_value = mock_list_response

        documents = client.property_documents.list_property_documents(1)

        assert isinstance(documents, list)
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_property_documents_dict_response(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test listing property documents with dict response containing data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": [{"id": 1, "title": "Test Document"}]}
        mock_request.return_value = response

        documents = client.property_documents.list_property_documents(1)

        assert isinstance(documents, list)
        assert len(documents) == 1
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_property_documents_dict_response_no_data(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test listing property documents with dict response but no data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": "not a list"}
        mock_request.return_value = response

        documents = client.property_documents.list_property_documents(1)

        assert isinstance(documents, list)
        assert len(documents) == 0
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_create_property_document(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test creating a property document."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {
            "id": 1,
            "title": "Contract Document",
            "filename": "contract.pdf",
            "property_id": 1,
        }

        document_data = {
            "title": "Contract Document",
            "filename": "contract.pdf",
            "file_url": "http://example.com/contract.pdf",
        }
        document = client.property_documents.create_property_document(1, document_data)

        assert isinstance(document, dict)
        assert document.get("id") == 1
        assert document.get("title") == "Contract Document"
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_create_property_document_dict_response(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test creating a property document with dict response containing data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": {"id": 1, "title": "Test Document"}}
        mock_request.return_value = response

        document_data = {"title": "Test Document"}
        document = client.property_documents.create_property_document(1, document_data)

        assert isinstance(document, dict)
        assert document.get("id") == 1
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_create_property_document_dict_response_no_data(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test creating a property document with dict response but no valid data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": "not a dict"}
        mock_request.return_value = response

        document_data = {"title": "Test Document"}
        document = client.property_documents.create_property_document(1, document_data)

        assert isinstance(document, dict)
        assert len(document) == 0
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_retrieve_property_document(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test retrieving a property document."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"id": 123, "title": "Contract Document"}

        document = client.property_documents.retrieve_property_document(1, 123)

        assert isinstance(document, dict)
        assert document.get("id") == 123
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_retrieve_property_document_dict_response(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test retrieving a property document with dict response containing data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": {"id": 123, "title": "Test Document"}}
        mock_request.return_value = response

        document = client.property_documents.retrieve_property_document(1, 123)

        assert isinstance(document, dict)
        assert document.get("id") == 123
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_update_property_document(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test updating a property document."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"id": 123, "title": "Updated Document"}

        update_data = {"title": "Updated Document"}
        document = client.property_documents.update_property_document(
            1, 123, update_data
        )

        assert isinstance(document, dict)
        assert document.get("id") == 123
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_update_property_document_dict_response(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test updating a property document with dict response containing data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": {"id": 123, "title": "Updated Document"}}
        mock_request.return_value = response

        update_data = {"title": "Updated Document"}
        document = client.property_documents.update_property_document(
            1, 123, update_data
        )

        assert isinstance(document, dict)
        assert document.get("id") == 123
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_delete_property_document(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_delete_response: Mock
    ) -> None:
        """Test deleting a property document."""
        mock_request.return_value = mock_delete_response

        result = client.property_documents.delete_property_document(1, 123)

        assert isinstance(result, dict)
        mock_request.assert_called_once()


class TestPropertyTasksAPI:
    """Test PropertyTasksAPI functionality."""

    def test_property_tasks_initialization(self, client: OpenToCloseAPI) -> None:
        """Test that property tasks API can be initialized."""
        property_tasks = client.property_tasks
        assert property_tasks is not None
        assert hasattr(property_tasks, "list_property_tasks")
        assert hasattr(property_tasks, "create_property_task")
        assert hasattr(property_tasks, "retrieve_property_task")
        assert hasattr(property_tasks, "update_property_task")
        assert hasattr(property_tasks, "delete_property_task")

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_property_tasks(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_list_response: Mock
    ) -> None:
        """Test listing property tasks."""
        mock_request.return_value = mock_list_response

        tasks = client.property_tasks.list_property_tasks(1)

        assert isinstance(tasks, list)
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_property_tasks_dict_response(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test listing property tasks with dict response containing data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": [{"id": 1, "title": "Test Task"}]}
        mock_request.return_value = response

        tasks = client.property_tasks.list_property_tasks(1)

        assert isinstance(tasks, list)
        assert len(tasks) == 1
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_property_tasks_dict_response_no_data(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test listing property tasks with dict response but no data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": "not a list"}
        mock_request.return_value = response

        tasks = client.property_tasks.list_property_tasks(1)

        assert isinstance(tasks, list)
        assert len(tasks) == 0
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_create_property_task(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test creating a property task."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {
            "id": 1,
            "title": "Follow up with client",
            "description": "Task description",
            "property_id": 1,
            "status": "pending",
        }

        task_data = {
            "title": "Follow up with client",
            "description": "Task description",
            "due_date": "2024-01-15",
        }
        task = client.property_tasks.create_property_task(1, task_data)

        assert isinstance(task, dict)
        assert task.get("id") == 1
        assert task.get("title") == "Follow up with client"
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_create_property_task_dict_response(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test creating a property task with dict response containing data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": {"id": 1, "title": "Test Task"}}
        mock_request.return_value = response

        task_data = {"title": "Test Task"}
        task = client.property_tasks.create_property_task(1, task_data)

        assert isinstance(task, dict)
        assert task.get("id") == 1
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_create_property_task_dict_response_no_data(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test creating a property task with dict response but no valid data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": "not a dict"}
        mock_request.return_value = response

        task_data = {"title": "Test Task"}
        task = client.property_tasks.create_property_task(1, task_data)

        assert isinstance(task, dict)
        assert len(task) == 0
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_retrieve_property_task(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test retrieving a property task."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"id": 123, "title": "Follow up with client"}

        task = client.property_tasks.retrieve_property_task(1, 123)

        assert isinstance(task, dict)
        assert task.get("id") == 123
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_retrieve_property_task_dict_response(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test retrieving a property task with dict response containing data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": {"id": 123, "title": "Test Task"}}
        mock_request.return_value = response

        task = client.property_tasks.retrieve_property_task(1, 123)

        assert isinstance(task, dict)
        assert task.get("id") == 123
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_update_property_task(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test updating a property task."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {
            "id": 123,
            "title": "Updated Task",
            "status": "completed",
        }

        update_data = {"title": "Updated Task", "status": "completed"}
        task = client.property_tasks.update_property_task(1, 123, update_data)

        assert isinstance(task, dict)
        assert task.get("id") == 123
        assert task.get("status") == "completed"
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_update_property_task_dict_response(
        self, mock_request: Mock, client: OpenToCloseAPI
    ) -> None:
        """Test updating a property task with dict response containing data."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"data": {"id": 123, "title": "Updated Task"}}
        mock_request.return_value = response

        update_data = {"title": "Updated Task"}
        task = client.property_tasks.update_property_task(1, 123, update_data)

        assert isinstance(task, dict)
        assert task.get("id") == 123
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_delete_property_task(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_delete_response: Mock
    ) -> None:
        """Test deleting a property task."""
        mock_request.return_value = mock_delete_response

        result = client.property_tasks.delete_property_task(1, 123)

        assert isinstance(result, dict)
        mock_request.assert_called_once()
