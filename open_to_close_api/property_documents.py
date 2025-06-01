"""Property documents client for Open To Close API."""

from typing import Any, Dict, List, Optional

from .base_client import BaseClient


class PropertyDocumentsAPI(BaseClient):
    """Client for property documents API endpoints.
    
    This client provides methods to manage documents associated with specific properties
    in the Open To Close platform.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the property documents client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API
        """
        super().__init__(api_key=api_key, base_url=base_url)

    def list_property_documents(
        self, property_id: int, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of documents for a specific property.

        Args:
            property_id: The ID of the property
            params: Optional dictionary of query parameters for filtering

        Returns:
            A list of dictionaries, where each dictionary represents a property document

        Raises:
            OpenToCloseAPIError: If the API request fails
            NotFoundError: If the property is not found
            ValidationError: If parameters are invalid
            AuthenticationError: If authentication fails

        Example:
            ```python
            # Get all documents for a property
            documents = client.property_documents.list_property_documents(123)

            # Get documents with filtering
            documents = client.property_documents.list_property_documents(
                123, params={"limit": 10}
            )
            ```
        """
        response = self.get(f"/properties/{property_id}/documents", params=params)
        if isinstance(response, list):
            return response
        elif isinstance(response, dict):
            data = response.get("data", [])
            return data if isinstance(data, list) else []
        return []

    def create_property_document(
        self, property_id: int, document_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add a document to a specific property.

        Args:
            property_id: The ID of the property
            document_data: A dictionary containing the document's information to be added

        Returns:
            A dictionary representing the newly added property document

        Raises:
            OpenToCloseAPIError: If the API request fails
            ValidationError: If document data is invalid
            NotFoundError: If the property is not found
            AuthenticationError: If authentication fails

        Example:
            ```python
            document = client.property_documents.create_property_document(123, {
                "name": "Purchase Agreement",
                "file_url": "https://example.com/file.pdf"
            })
            ```
        """
        response = self.post(f"/properties/{property_id}/documents", json_data=document_data)
        if isinstance(response, dict) and response.get("id"):
            return response
        if isinstance(response, dict):
            data = response.get("data", {})
            return data if isinstance(data, dict) else {}
        return {}

    def retrieve_property_document(
        self, property_id: int, document_id: int
    ) -> Dict[str, Any]:
        """Retrieve a specific document for a specific property.

        Args:
            property_id: The ID of the property
            document_id: The ID of the document to retrieve

        Returns:
            A dictionary representing the property document

        Raises:
            NotFoundError: If the property or document is not found
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            document = client.property_documents.retrieve_property_document(123, 456)
            print(f"Document name: {document['name']}")
            ```
        """
        response = self.get(f"/properties/{property_id}/documents/{document_id}")
        if isinstance(response, dict) and response.get("id"):
            return response
        if isinstance(response, dict):
            data = response.get("data", {})
            return data if isinstance(data, dict) else {}
        return {}

    def update_property_document(
        self, property_id: int, document_id: int, document_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a specific document for a specific property.

        Args:
            property_id: The ID of the property
            document_id: The ID of the document to update
            document_data: A dictionary containing the fields to update

        Returns:
            A dictionary representing the updated property document

        Raises:
            NotFoundError: If the property or document is not found
            ValidationError: If document data is invalid
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            updated_document = client.property_documents.update_property_document(
                123, 456, {"name": "Updated Purchase Agreement"}
            )
            ```
        """
        response = self.put(
            f"/properties/{property_id}/documents/{document_id}", json_data=document_data
        )
        if isinstance(response, dict) and response.get("id"):
            return response
        if isinstance(response, dict):
            data = response.get("data", {})
            return data if isinstance(data, dict) else {}
        return {}

    def delete_property_document(
        self, property_id: int, document_id: int
    ) -> Dict[str, Any]:
        """Remove a document from a specific property.

        Args:
            property_id: The ID of the property
            document_id: The ID of the document to remove

        Returns:
            A dictionary containing the API response

        Raises:
            NotFoundError: If the property or document is not found
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            result = client.property_documents.delete_property_document(123, 456)
            ```
        """
        return self.delete(f"/properties/{property_id}/documents/{document_id}")
