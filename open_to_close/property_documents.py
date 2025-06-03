"""Property documents client for Open To Close API."""

import logging
from typing import Any, Dict, List, Optional

from .base_client import BaseClient
from .exceptions import ValidationError

logger = logging.getLogger(__name__)


class PropertyDocumentsAPI(BaseClient):
    """Client for property documents API endpoints.

    This client provides methods to manage documents associated with specific properties
    in the Open To Close platform. All methods include comprehensive input validation
    and error handling.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the property documents client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API

        Raises:
            AuthenticationError: If API key is missing or invalid
            ConfigurationError: If configuration is invalid
        """
        super().__init__(api_key=api_key, base_url=base_url)
        logger.debug("Initialized PropertyDocumentsAPI client")

    def _validate_property_document_data(
        self, document_data: Dict[str, Any], operation: str
    ) -> None:
        """Validate property document data before sending to API.

        Args:
            document_data: Property document data to validate
            operation: Operation type for error context (create/update)

        Raises:
            ValidationError: If property document data is invalid
        """
        if not isinstance(document_data, dict):
            raise ValidationError(
                f"Property document data for {operation} must be a dictionary, got {type(document_data).__name__}"
            )

        if not document_data:
            raise ValidationError(
                f"Property document data for {operation} cannot be empty"
            )

        # Validate required fields for create operations
        if operation == "create":
            required_fields = ["name"]
            missing_fields = [
                field for field in required_fields if field not in document_data
            ]
            if missing_fields:
                raise ValidationError(
                    f"Property document data for {operation} missing required fields: {', '.join(missing_fields)}"
                )

        # Validate name if provided
        if "name" in document_data:
            name = document_data["name"]
            if not isinstance(name, str) or len(name.strip()) == 0:
                raise ValidationError(f"name must be a non-empty string, got: {name}")

        # Validate type if provided
        if "type" in document_data:
            doc_type = document_data["type"]
            if not isinstance(doc_type, str) or len(doc_type.strip()) == 0:
                raise ValidationError(
                    f"type must be a non-empty string, got: {doc_type}"
                )

        # Validate URL if provided
        if "url" in document_data:
            url = document_data["url"]
            if not isinstance(url, str) or len(url.strip()) == 0:
                raise ValidationError(f"url must be a non-empty string, got: {url}")
            # Basic URL validation
            if not url.startswith(("http://", "https://")):
                raise ValidationError(f"url must be a valid HTTP/HTTPS URL, got: {url}")

        # Validate file_size if provided
        if "file_size" in document_data:
            file_size = document_data["file_size"]
            try:
                file_size_int = int(file_size)
                if file_size_int < 0:
                    raise ValidationError(
                        f"file_size must be non-negative, got {file_size_int}"
                    )
            except (ValueError, TypeError):
                raise ValidationError(
                    f"file_size must be an integer, got {type(file_size).__name__}: {file_size}"
                )

        # Validate description if provided
        if "description" in document_data:
            description = document_data["description"]
            if not isinstance(description, str):
                raise ValidationError(
                    f"description must be a string, got {type(description).__name__}: {description}"
                )

        logger.debug(f"Property document data validated for {operation} operation")

    def _validate_list_params(self, params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate and normalize parameters for list operations.

        Args:
            params: Parameters to validate

        Returns:
            Validated and normalized parameters

        Raises:
            ValidationError: If parameters are invalid
        """
        if params is None:
            return {}

        if not isinstance(params, dict):
            raise ValidationError(
                f"List parameters must be a dictionary, got {type(params).__name__}"
            )

        validated_params = params.copy()

        # Validate limit parameter
        if "limit" in validated_params:
            limit = validated_params["limit"]
            try:
                limit_int = int(limit)
                if limit_int <= 0:
                    raise ValidationError(
                        f"Limit must be a positive integer, got {limit_int}"
                    )
                if limit_int > 1000:  # Reasonable upper bound
                    logger.warning(
                        f"Large limit value: {limit_int}. Consider using pagination."
                    )
                validated_params["limit"] = limit_int
            except (ValueError, TypeError):
                raise ValidationError(
                    f"Limit must be an integer, got {type(limit).__name__}: {limit}"
                )

        # Validate offset parameter
        if "offset" in validated_params:
            offset = validated_params["offset"]
            try:
                offset_int = int(offset)
                if offset_int < 0:
                    raise ValidationError(
                        f"Offset must be non-negative, got {offset_int}"
                    )
                validated_params["offset"] = offset_int
            except (ValueError, TypeError):
                raise ValidationError(
                    f"Offset must be an integer, got {type(offset).__name__}: {offset}"
                )

        # Validate type filter if provided
        if "type" in validated_params:
            doc_type = validated_params["type"]
            if not isinstance(doc_type, str) or len(doc_type.strip()) == 0:
                raise ValidationError(
                    f"Type filter must be a non-empty string, got: {doc_type}"
                )

        logger.debug("List parameters validated", extra={"params": validated_params})
        return validated_params

    def list_property_documents(
        self, property_id: int, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of documents for a specific property with validation and error handling.

        Args:
            property_id: The ID of the property (must be a positive integer)
            params: Optional dictionary of query parameters for filtering.
                   Supported parameters may include:
                   - limit: Maximum number of property documents to return
                   - offset: Number of property documents to skip
                   - type: Filter by document type (e.g., 'contract', 'invoice')

        Returns:
            A list of dictionaries, where each dictionary represents a property document

        Raises:
            ValidationError: If property_id or parameters are invalid
            NotFoundError: If the property is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            # Get all documents for a property
            documents = client.property_documents.list_property_documents(123)

            # Get documents with filtering
            documents = client.property_documents.list_property_documents(
                123, params={"type": "contract", "limit": 10}
            )
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            validated_params = self._validate_list_params(params)

            logger.info(
                f"Listing documents for property {validated_property_id}",
                extra={"params": validated_params},
            )
            response = self.get(
                f"/properties/{validated_property_id}/documents",
                params=validated_params,
            )
            result = self._process_list_response(
                response, f"/properties/{validated_property_id}/documents"
            )

            logger.info(
                f"Successfully retrieved {len(result)} documents for property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to list documents for property {property_id}: {str(e)}",
                extra={"params": params},
            )
            raise

    def create_property_document(
        self, property_id: int, document_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add a document to a specific property with comprehensive validation.

        Args:
            property_id: The ID of the property (must be a positive integer)
            document_data: A dictionary containing the document's information.
                          Must include name as a required field.
                          Common fields include:
                          - name: Document name (required)
                          - type: Document type (e.g., 'contract', 'invoice', 'inspection')
                          - url: Document URL
                          - description: Document description
                          - file_size: File size in bytes

        Returns:
            A dictionary representing the newly added property document

        Raises:
            ValidationError: If property_id or document_data is invalid
            NotFoundError: If the property is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            document = client.property_documents.create_property_document(123, {
                "name": "Purchase Agreement",
                "type": "contract",
                "url": "https://example.com/document.pdf",
                "description": "Main purchase agreement document"
            })
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            self._validate_property_document_data(document_data, "create")

            logger.info(
                f"Creating document for property {validated_property_id}",
                extra={"document_name": document_data.get("name", "unknown")},
            )
            response = self.post(
                f"/properties/{validated_property_id}/documents",
                json_data=document_data,
            )
            result = self._process_response_data(
                response, f"/properties/{validated_property_id}/documents"
            )

            logger.info(
                f"Successfully created document for property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to create document for property {property_id}: {str(e)}",
                extra={
                    "document_data_keys": (
                        list(document_data.keys())
                        if isinstance(document_data, dict)
                        else "invalid"
                    )
                },
            )
            raise

    def retrieve_property_document(
        self, property_id: int, document_id: int
    ) -> Dict[str, Any]:
        """Retrieve a specific document for a specific property with validation.

        Args:
            property_id: The ID of the property (must be a positive integer)
            document_id: The ID of the document to retrieve (must be a positive integer)

        Returns:
            A dictionary representing the property document

        Raises:
            ValidationError: If property_id or document_id is invalid
            NotFoundError: If the property or document is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            document = client.property_documents.retrieve_property_document(123, 456)
            print(f"Document name: {document.get('name', 'N/A')}")
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            validated_document_id = self._validate_resource_id(document_id, "document")

            logger.info(
                f"Retrieving document {validated_document_id} for property {validated_property_id}"
            )
            response = self.get(
                f"/properties/{validated_property_id}/documents/{validated_document_id}"
            )
            result = self._process_response_data(
                response,
                f"/properties/{validated_property_id}/documents/{validated_document_id}",
            )

            logger.info(
                f"Successfully retrieved document {validated_document_id} for property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to retrieve document {document_id} for property {property_id}: {str(e)}"
            )
            raise

    def update_property_document(
        self, property_id: int, document_id: int, document_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a specific document for a specific property with validation.

        Args:
            property_id: The ID of the property (must be a positive integer)
            document_id: The ID of the document to update (must be a positive integer)
            document_data: A dictionary containing the fields to update.
                          Fields can include:
                          - name: Document name
                          - type: Document type
                          - url: Document URL
                          - description: Document description

        Returns:
            A dictionary representing the updated property document

        Raises:
            ValidationError: If property_id, document_id, or document_data is invalid
            NotFoundError: If the property or document is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            updated_document = client.property_documents.update_property_document(
                123, 456, {"name": "Updated Purchase Agreement", "type": "contract"}
            )
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            validated_document_id = self._validate_resource_id(document_id, "document")
            self._validate_property_document_data(document_data, "update")

            logger.info(
                f"Updating document {validated_document_id} for property {validated_property_id}",
                extra={"update_fields": list(document_data.keys())},
            )
            response = self.put(
                f"/properties/{validated_property_id}/documents/{validated_document_id}",
                json_data=document_data,
            )
            result = self._process_response_data(
                response,
                f"/properties/{validated_property_id}/documents/{validated_document_id}",
            )

            logger.info(
                f"Successfully updated document {validated_document_id} for property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to update document {document_id} for property {property_id}: {str(e)}",
                extra={
                    "document_data_keys": (
                        list(document_data.keys())
                        if isinstance(document_data, dict)
                        else "invalid"
                    )
                },
            )
            raise

    def delete_property_document(
        self, property_id: int, document_id: int
    ) -> Dict[str, Any]:
        """Remove a document from a specific property with validation.

        Args:
            property_id: The ID of the property (must be a positive integer)
            document_id: The ID of the document to remove (must be a positive integer)

        Returns:
            A dictionary containing the API response (typically empty for successful deletions)

        Raises:
            ValidationError: If property_id or document_id is invalid
            NotFoundError: If the property or document is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            result = client.property_documents.delete_property_document(123, 456)
            print("Document removed from property successfully")
            ```
        """
        try:
            validated_property_id = self._validate_resource_id(property_id, "property")
            validated_document_id = self._validate_resource_id(document_id, "document")

            logger.info(
                f"Removing document {validated_document_id} from property {validated_property_id}"
            )
            result = self.delete(
                f"/properties/{validated_property_id}/documents/{validated_document_id}"
            )

            logger.info(
                f"Successfully removed document {validated_document_id} from property {validated_property_id}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to remove document {document_id} from property {property_id}: {str(e)}"
            )
            raise
