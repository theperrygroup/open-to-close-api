from typing import Dict, Any, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .client import OpenToCloseAPI

class PropertyDocumentsAPI:
    """Handles API requests for Property Document related endpoints."""

    def __init__(self, client: 'OpenToCloseAPI'):
        """Initializes the PropertyDocumentsAPI with a client instance.

        Args:
            client: The OpenToCloseAPI client instance.
        """
        self._client = client

    def list_property_documents(self, property_id: int, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Retrieves a list of documents for a specific property.

        Args:
            property_id: The ID of the property.
            params: Optional dictionary of query parameters.

        Returns:
            A list of dictionaries, where each dictionary represents a property document.
        """
        response = self._client._request("GET", f"/properties/{property_id}/documents", params=params)
        json_response = response.json()
        if isinstance(json_response, list):
            return json_response
        elif isinstance(json_response, dict):
            return json_response.get("data", [])
        return []

    def create_property_document(self, property_id: int, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Adds a document to a specific property.

        Args:
            property_id: The ID of the property.
            document_data: A dictionary containing the document's information to be added.

        Returns:
            A dictionary representing the newly added property document.
        """
        response = self._client._request("POST", f"/properties/{property_id}/documents", json_data=document_data)
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get('id'): return json_response
        return json_response.get("data", {})

    def retrieve_property_document(self, property_id: int, document_id: int) -> Dict[str, Any]:
        """Retrieves a specific document for a specific property.

        Args:
            property_id: The ID of the property.
            document_id: The ID of the document to retrieve.

        Returns:
            A dictionary representing the property document.
        """
        response = self._client._request("GET", f"/properties/{property_id}/documents/{document_id}")
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get('id'): return json_response
        return json_response.get("data", {})

    def update_property_document(self, property_id: int, document_id: int, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Updates a specific document for a specific property.

        Args:
            property_id: The ID of the property.
            document_id: The ID of the document to update.
            document_data: A dictionary containing the fields to update.

        Returns:
            A dictionary representing the updated property document.
        """
        response = self._client._request("PUT", f"/properties/{property_id}/documents/{document_id}", json_data=document_data)
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get('id'): return json_response
        return json_response.get("data", {})

    def delete_property_document(self, property_id: int, document_id: int) -> Dict[str, Any]:
        """Removes a document from a specific property.

        Args:
            property_id: The ID of the property.
            document_id: The ID of the document to remove.
        
        Returns:
            A dictionary containing the API response.
        """
        response = self._client._request("DELETE", f"/properties/{property_id}/documents/{document_id}")
        if response.status_code == 204:
            return {}
        return response.json() 