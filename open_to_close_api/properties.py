"""Properties client for Open To Close API."""

from typing import Any, Dict, List, Optional

from .base_client import BaseClient


class PropertiesAPI(BaseClient):
    """Client for properties API endpoints.

    This client provides methods to manage properties in the Open To Close platform.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the properties client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API
        """
        super().__init__(api_key=api_key, base_url=base_url)

    def list_properties(
        self, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of properties.

        Args:
            params: Optional dictionary of query parameters for filtering

        Returns:
            A list of dictionaries, where each dictionary represents a property

        Raises:
            OpenToCloseAPIError: If the API request fails
            ValidationError: If parameters are invalid
            AuthenticationError: If authentication fails

        Example:
            ```python
            # Get all properties
            properties = client.properties.list_properties()

            # Get properties with custom parameters
            properties = client.properties.list_properties(params={"limit": 50})
            ```
        """
        response = self.get("/properties", params=params)
        return self._process_list_response(response)

    def create_property(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new property.

        Args:
            property_data: A dictionary containing the property's information

        Returns:
            A dictionary representing the newly created property

        Raises:
            OpenToCloseAPIError: If the API request fails
            ValidationError: If property data is invalid
            AuthenticationError: If authentication fails

        Example:
            ```python
            property = client.properties.create_property({
                "address": "123 Main St",
                "city": "Anytown",
                "state": "CA",
                "zip": "12345"
            })
            ```
        """
        response = self.post("/properties", json_data=property_data)
        return self._process_response_data(response)

    def retrieve_property(self, property_id: int) -> Dict[str, Any]:
        """Retrieve a specific property by its ID.

        Args:
            property_id: The ID of the property to retrieve

        Returns:
            A dictionary representing the property

        Raises:
            NotFoundError: If the property is not found
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            property = client.properties.retrieve_property(123)
            print(f"Property address: {property['address']}")
            ```
        """
        response = self.get(f"/properties/{property_id}")
        return self._process_response_data(response)

    def update_property(
        self, property_id: int, property_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing property.

        Args:
            property_id: The ID of the property to update
            property_data: A dictionary containing the fields to update

        Returns:
            A dictionary representing the updated property

        Raises:
            NotFoundError: If the property is not found
            ValidationError: If property data is invalid
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            updated_property = client.properties.update_property(123, {
                "status": "sold",
                "sale_price": 350000
            })
            ```
        """
        response = self.put(f"/properties/{property_id}", json_data=property_data)
        return self._process_response_data(response)

    def delete_property(self, property_id: int) -> Dict[str, Any]:
        """Delete a property by its ID.

        Args:
            property_id: The ID of the property to delete

        Returns:
            A dictionary containing the API response

        Raises:
            NotFoundError: If the property is not found
            OpenToCloseAPIError: If the API request fails
            AuthenticationError: If authentication fails

        Example:
            ```python
            result = client.properties.delete_property(123)
            ```
        """
        return self.delete(f"/properties/{property_id}")
