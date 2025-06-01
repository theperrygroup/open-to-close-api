import pytest
from unittest.mock import MagicMock, patch
from open_to_close_api.client import OpenToCloseAPI
from open_to_close_api.property_documents import PropertyDocumentsAPI

@pytest.fixture
def client() -> OpenToCloseAPI:
    """Provides an OpenToCloseAPI client instance for testing."""
    return OpenToCloseAPI(api_key="test_api_key")

@pytest.fixture
def property_documents_api(client: OpenToCloseAPI) -> PropertyDocumentsAPI:
    """Provides a PropertyDocumentsAPI instance for testing."""
    return PropertyDocumentsAPI(client)

def test_list_property_documents_success(property_documents_api: PropertyDocumentsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a list of documents for a property."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1, "file_name": "contract.pdf"}]}
    property_id = 200
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        params = {"category": "legal"}
        result = property_documents_api.list_property_documents(property_id=property_id, params=params)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/documents", params=params)
    assert result == [{"id": 1, "file_name": "contract.pdf"}]

def test_create_property_document_success(property_documents_api: PropertyDocumentsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful creation of a property document."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"data": {"id": 2, "file_name": "inspection.pdf"}}
    property_id = 200
    document_data = {"file_name": "inspection.pdf", "url": "http://example.com/inspection.pdf"} # Simplified
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_documents_api.create_property_document(property_id=property_id, document_data=document_data)
        mock_method.assert_called_once_with("POST", f"/properties/{property_id}/documents", json_data=document_data)
    assert result == {"id": 2, "file_name": "inspection.pdf"}

def test_retrieve_property_document_success(property_documents_api: PropertyDocumentsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful retrieval of a specific property document."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "file_name": "contract.pdf"}}
    property_id = 200
    document_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_documents_api.retrieve_property_document(property_id=property_id, document_id=document_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/documents/{document_id}")
    assert result == {"id": 1, "file_name": "contract.pdf"}

def test_update_property_document_success(property_documents_api: PropertyDocumentsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful update of a property document."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1, "file_name": "contract_v2.pdf"}}
    property_id = 200
    document_id = 1
    update_data = {"file_name": "contract_v2.pdf"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_documents_api.update_property_document(property_id=property_id, document_id=document_id, document_data=update_data)
        mock_method.assert_called_once_with("PUT", f"/properties/{property_id}/documents/{document_id}", json_data=update_data)
    assert result == {"id": 1, "file_name": "contract_v2.pdf"}

def test_delete_property_document_success_204(property_documents_api: PropertyDocumentsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a property document with a 204 response."""
    mock_response = MagicMock()
    mock_response.status_code = 204
    property_id = 200
    document_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_documents_api.delete_property_document(property_id=property_id, document_id=document_id)
        mock_method.assert_called_once_with("DELETE", f"/properties/{property_id}/documents/{document_id}")
    assert result == {}

def test_delete_property_document_success_json_response(property_documents_api: PropertyDocumentsAPI, client: OpenToCloseAPI) -> None:
    """Tests successful deletion of a property document with a JSON response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Property document deleted"}
    property_id = 200
    document_id = 1
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_documents_api.delete_property_document(property_id=property_id, document_id=document_id)
        mock_method.assert_called_once_with("DELETE", f"/properties/{property_id}/documents/{document_id}")
    assert result == {"message": "Property document deleted"}

def test_list_property_documents_empty(property_documents_api: PropertyDocumentsAPI, client: OpenToCloseAPI) -> None:
    """Tests listing property documents when API returns an empty list."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    property_id = 201
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_documents_api.list_property_documents(property_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/documents", params=None)
    assert result == []

def test_list_property_documents_no_data_key(property_documents_api: PropertyDocumentsAPI, client: OpenToCloseAPI) -> None:
    """Tests listing property documents when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    property_id = 202
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_documents_api.list_property_documents(property_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/documents", params=None)
    assert result == []

def test_create_property_document_no_data_key(property_documents_api: PropertyDocumentsAPI, client: OpenToCloseAPI) -> None:
    """Tests creating a property document when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {}
    property_id = 203
    document_data = {"file_name": "untitled.pdf"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_documents_api.create_property_document(property_id, document_data)
        mock_method.assert_called_once_with("POST", f"/properties/{property_id}/documents", json_data=document_data)
    assert result == {}

def test_retrieve_property_document_no_data_key(property_documents_api: PropertyDocumentsAPI, client: OpenToCloseAPI) -> None:
    """Tests retrieving a property document when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    property_id = 204
    document_id = 50
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_documents_api.retrieve_property_document(property_id, document_id)
        mock_method.assert_called_once_with("GET", f"/properties/{property_id}/documents/{document_id}")
    assert result == {}

def test_update_property_document_no_data_key(property_documents_api: PropertyDocumentsAPI, client: OpenToCloseAPI) -> None:
    """Tests updating a property document when API response is missing 'data' key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    property_id = 205
    document_id = 51
    update_data = {"file_name": "final_report.docx"}
    with patch.object(client, '_request', return_value=mock_response) as mock_method:
        result = property_documents_api.update_property_document(property_id, document_id, update_data)
        mock_method.assert_called_once_with("PUT", f"/properties/{property_id}/documents/{document_id}", json_data=update_data)
    assert result == {} 