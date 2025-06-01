"""Tests for property-related API endpoints."""

import pytest
from unittest.mock import Mock, patch
import requests

from open_to_close_api import OpenToCloseAPI
from open_to_close_api.exceptions import NotFoundError, ValidationError


@pytest.fixture
def client():
    """Create a test client."""
    return OpenToCloseAPI(api_key="test_key")


@pytest.fixture
def mock_response():
    """Create a mock response."""
    response = Mock(spec=requests.Response)
    response.status_code = 200
    response.json.return_value = {"id": 1, "name": "Test"}
    return response


class TestPropertyContactsAPI:
    """Test PropertyContactsAPI functionality."""

    def test_property_contacts_initialization(self, client):
        """Test that property contacts API can be initialized."""
        property_contacts = client.property_contacts
        assert property_contacts is not None
        assert hasattr(property_contacts, 'list_property_contacts')

    @patch('open_to_close_api.base_client.requests.Session.request')
    def test_list_property_contacts(self, mock_request, client, mock_response):
        """Test listing property contacts."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = [{"id": 1, "role": "buyer"}]
        
        contacts = client.property_contacts.list_property_contacts(123)
        
        assert isinstance(contacts, list)
        mock_request.assert_called_once()

    @patch('open_to_close_api.base_client.requests.Session.request')
    def test_create_property_contact(self, mock_request, client, mock_response):
        """Test creating a property contact."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"id": 1, "contact_id": 456, "role": "buyer"}
        
        contact_data = {"contact_id": 456, "role": "buyer"}
        contact = client.property_contacts.create_property_contact(123, contact_data)
        
        assert isinstance(contact, dict)
        assert contact.get("id") == 1
        mock_request.assert_called_once()

    @patch('open_to_close_api.base_client.requests.Session.request')
    def test_retrieve_property_contact(self, mock_request, client, mock_response):
        """Test retrieving a property contact."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"id": 1, "contact_id": 456, "role": "buyer"}
        
        contact = client.property_contacts.retrieve_property_contact(123, 456)
        
        assert isinstance(contact, dict)
        assert contact.get("id") == 1
        mock_request.assert_called_once()

    @patch('open_to_close_api.base_client.requests.Session.request')
    def test_update_property_contact(self, mock_request, client, mock_response):
        """Test updating a property contact."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"id": 1, "contact_id": 456, "role": "seller"}
        
        update_data = {"role": "seller"}
        contact = client.property_contacts.update_property_contact(123, 456, update_data)
        
        assert isinstance(contact, dict)
        assert contact.get("id") == 1
        mock_request.assert_called_once()

    @patch('open_to_close_api.base_client.requests.Session.request')
    def test_delete_property_contact(self, mock_request, client, mock_response):
        """Test deleting a property contact."""
        mock_request.return_value = mock_response
        mock_response.status_code = 204
        mock_response.json.return_value = {}
        
        result = client.property_contacts.delete_property_contact(123, 456)
        
        assert isinstance(result, dict)
        mock_request.assert_called_once()


class TestPropertyDocumentsAPI:
    """Test PropertyDocumentsAPI functionality."""

    def test_property_documents_initialization(self, client):
        """Test that property documents API can be initialized."""
        property_documents = client.property_documents
        assert property_documents is not None
        assert hasattr(property_documents, 'list_property_documents')

    @patch('open_to_close_api.base_client.requests.Session.request')
    def test_list_property_documents(self, mock_request, client, mock_response):
        """Test listing property documents."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = [{"id": 1, "name": "Contract"}]
        
        documents = client.property_documents.list_property_documents(123)
        
        assert isinstance(documents, list)
        mock_request.assert_called_once()

    @patch('open_to_close_api.base_client.requests.Session.request')
    def test_create_property_document(self, mock_request, client, mock_response):
        """Test creating a property document."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"id": 1, "name": "Purchase Agreement"}
        
        document_data = {"name": "Purchase Agreement", "file_url": "https://example.com/file.pdf"}
        document = client.property_documents.create_property_document(123, document_data)
        
        assert isinstance(document, dict)
        assert document.get("id") == 1
        mock_request.assert_called_once()


class TestPropertyEmailsAPI:
    """Test PropertyEmailsAPI functionality."""

    def test_property_emails_initialization(self, client):
        """Test that property emails API can be initialized."""
        property_emails = client.property_emails
        assert property_emails is not None
        assert hasattr(property_emails, 'list_property_emails')

    @patch('open_to_close_api.base_client.requests.Session.request')
    def test_list_property_emails(self, mock_request, client, mock_response):
        """Test listing property emails."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = [{"id": 1, "subject": "Property Update"}]
        
        emails = client.property_emails.list_property_emails(123)
        
        assert isinstance(emails, list)
        mock_request.assert_called_once()


class TestPropertyNotesAPI:
    """Test PropertyNotesAPI functionality."""

    def test_property_notes_initialization(self, client):
        """Test that property notes API can be initialized."""
        property_notes = client.property_notes
        assert property_notes is not None
        assert hasattr(property_notes, 'list_property_notes')

    @patch('open_to_close_api.base_client.requests.Session.request')
    def test_list_property_notes(self, mock_request, client, mock_response):
        """Test listing property notes."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = [{"id": 1, "content": "Inspection completed"}]
        
        notes = client.property_notes.list_property_notes(123)
        
        assert isinstance(notes, list)
        mock_request.assert_called_once()


class TestPropertyTasksAPI:
    """Test PropertyTasksAPI functionality."""

    def test_property_tasks_initialization(self, client):
        """Test that property tasks API can be initialized."""
        property_tasks = client.property_tasks
        assert property_tasks is not None
        assert hasattr(property_tasks, 'list_property_tasks')

    @patch('open_to_close_api.base_client.requests.Session.request')
    def test_list_property_tasks(self, mock_request, client, mock_response):
        """Test listing property tasks."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = [{"id": 1, "title": "Schedule inspection"}]
        
        tasks = client.property_tasks.list_property_tasks(123)
        
        assert isinstance(tasks, list)
        mock_request.assert_called_once()

    @patch('open_to_close_api.base_client.requests.Session.request')
    def test_create_property_task(self, mock_request, client, mock_response):
        """Test creating a property task."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"id": 1, "title": "Schedule inspection"}
        
        task_data = {
            "title": "Schedule inspection", 
            "description": "Arrange property inspection with buyer.",
            "due_date": "2024-01-15"
        }
        task = client.property_tasks.create_property_task(123, task_data)
        
        assert isinstance(task, dict)
        assert task.get("id") == 1
        mock_request.assert_called_once()


class TestPropertyAPIIntegration:
    """Integration tests for property APIs."""

    def test_all_property_apis_accessible(self, client):
        """Test that all property APIs are accessible without errors."""
        # This test would have failed before our fix
        assert client.property_contacts is not None
        assert client.property_documents is not None
        assert client.property_emails is not None
        assert client.property_notes is not None
        assert client.property_tasks is not None

    def test_property_apis_inherit_from_base_client(self, client):
        """Test that all property APIs inherit from BaseClient."""
        from open_to_close_api.base_client import BaseClient
        
        assert isinstance(client.property_contacts, BaseClient)
        assert isinstance(client.property_documents, BaseClient)
        assert isinstance(client.property_emails, BaseClient)
        assert isinstance(client.property_notes, BaseClient)
        assert isinstance(client.property_tasks, BaseClient) 