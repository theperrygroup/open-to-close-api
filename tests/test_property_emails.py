import pytest
from unittest.mock import MagicMock, patch
from open_to_close_api.client import OpenToCloseAPI
from open_to_close_api.property_emails import PropertyEmailsAPI

@pytest.fixture
def client() -> OpenToCloseAPI:
    """Provides an OpenToCloseAPI client instance for testing."""
    return OpenToCloseAPI(api_key="test_api_key")

@pytest.fixture
def property_emails_api(client: OpenToCloseAPI) -> PropertyEmailsAPI:
    """Provides a PropertyEmailsAPI instance for testing."""
    return PropertyEmailsAPI(client)

def test_list_property_emails_success(property_emails_api: PropertyEmailsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a list of emails for a property."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1, "subject": "Welcome Email"}]}
    property_id = 300
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        params = {"folder": "sent"}
        result = property_emails_api.list_property_emails(property_id=property_id, params=params)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/emails", params=params)
    assert result == [{"id": 1, "subject": "Welcome Email"}]

def test_create_property_email_success(property_emails_api: PropertyEmailsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful creation of a property email."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"data": {"id": 2, "subject": "Follow-up"}}
    property_id = 300
    email_data = {"subject": "Follow-up", "body": "Just checking in."}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_emails_api.create_property_email(property_id=property_id, email_data=email_data)
        mock_method.assert_called_once_with("POST", f"/properties/{property_id}/emails", json_data=email_data)
    assert result == {"id": 2, "subject": "Follow-up"}

def test_retrieve_property_email_success(property_emails_api: PropertyEmailsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a specific property email."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "subject": "Welcome Email"}}
    property_id = 300
    email_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_emails_api.retrieve_property_email(property_id=property_id, email_id=email_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/emails/{email_id}")
    assert result == {"id": 1, "subject": "Welcome Email"}

def test_update_property_email_success(property_emails_api: PropertyEmailsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful update of a property email."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "subject": "Updated Welcome Email"}}
    property_id = 300
    email_id = 1
    update_data = {"subject": "Updated Welcome Email"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_emails_api.update_property_email(property_id=property_id, email_id=email_id, email_data=update_data)
        mock_method.assert_called_once_with("PUT", f"/properties/{property_id}/emails/{email_id}", json_data=update_data)
    assert result == {"id": 1, "subject": "Updated Welcome Email"}

def test_delete_property_email_success_204(property_emails_api: PropertyEmailsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a property email with a 204 response."""
    mock_response = MagicMock()
    mock_response.status_code = 204
    property_id = 300
    email_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_emails_api.delete_property_email(property_id=property_id, email_id=email_id)
        mock_method.assert_called_once_with("DELETE", f"/properties/{property_id}/emails/{email_id}")
    assert result == {}

def test_delete_property_email_success_json_response(property_emails_api: PropertyEmailsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a property email with a JSON response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Property email deleted"}
    property_id = 300
    email_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_emails_api.delete_property_email(property_id=property_id, email_id=email_id)
        mock_method.assert_called_once_with("DELETE", f"/properties/{property_id}/emails/{email_id}")
    assert result == {"message": "Property email deleted"}

def test_list_property_emails_empty(property_emails_api: PropertyEmailsAPI, client: OpenToCloseAPI) -> None:
    """Tests listing property emails when API returns an empty list."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    property_id = 301
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_emails_api.list_property_emails(property_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/emails", params=None)
    assert result == []

def test_list_property_emails_no_data_key(property_emails_api: PropertyEmailsAPI, client: OpenToCloseAPI) -> None:
    """Tests listing property emails when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    property_id = 302
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_emails_api.list_property_emails(property_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/emails", params=None)
    assert result == []

def test_create_property_email_no_data_key(property_emails_api: PropertyEmailsAPI, client: OpenToCloseAPI) -> None:
    """Tests creating a property email when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {}
    property_id = 303
    email_data = {"subject": "Test Subject"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_emails_api.create_property_email(property_id, email_data)
        mock_method.assert_called_once_with("POST", f"/properties/{property_id}/emails", json_data=email_data)
    assert result == {}

def test_retrieve_property_email_no_data_key(property_emails_api: PropertyEmailsAPI, client: OpenToCloseAPI) -> None:
    """Tests retrieving a property email when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    property_id = 304
    email_id = 50
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_emails_api.retrieve_property_email(property_id, email_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/emails/{email_id}")
    assert result == {}

def test_update_property_email_no_data_key(property_emails_api: PropertyEmailsAPI, client: OpenToCloseAPI) -> None:
    """Tests updating a property email when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    property_id = 305
    email_id = 51
    update_data = {"subject": "Final Update"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_emails_api.update_property_email(property_id, email_id, update_data)
        mock_method.assert_called_once_with("PUT", f"/properties/{property_id}/emails/{email_id}", json_data=update_data)
    assert result == {} 