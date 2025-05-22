from typing import Dict, Any, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .client import OpenToCloseAPI

class PropertiesAPI:
    """Handles API requests for Property related endpoints."""

    def __init__(self, client: 'OpenToCloseAPI'):
        """Initializes the PropertiesAPI with a client instance.

        Args:
            client: The OpenToCloseAPI client instance.
        """
        self._client = client

    def list_properties(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Retrieves a list of properties.

        Args:
            params: Optional dictionary of query parameters.

        Returns:
            A list of dictionaries, where each dictionary represents a property.
        """
        response = self._client._request("GET", "/properties", params=params)
        json_response = response.json()
        if isinstance(json_response, list):
            return json_response
        elif isinstance(json_response, dict):
            return json_response.get("data", [])
        return [] # Should not happen with a consistent API, but a safe default

    def create_property(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new property.

        Args:
            property_data: A dictionary containing the property's information.

        Returns:
            A dictionary representing the newly created property.
        """
        response = self._client._request("POST", "/properties", json_data=property_data)
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get('id'): return json_response
        return json_response.get("data", {})

    def retrieve_property(self, property_id: int) -> Dict[str, Any]:
        """Retrieves a specific property by its ID.

        Args:
            property_id: The ID of the property to retrieve.

        Returns:
            A dictionary representing the property.
        """
        response = self._client._request("GET", f"/properties/{property_id}")
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get('id'): return json_response
        return json_response.get("data", {})

    def update_property(self, property_id: int, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Updates an existing property.

        Args:
            property_id: The ID of the property to update.
            property_data: A dictionary containing the fields to update.

        Returns:
            A dictionary representing the updated property.
        """
        response = self._client._request("PUT", f"/properties/{property_id}", json_data=property_data)
        json_response = response.json()
        if isinstance(json_response, dict) and json_response.get('id'): return json_response
        return json_response.get("data", {})

    def delete_property(self, property_id: int) -> Dict[str, Any]:
        """Deletes a property by its ID.

        Args:
            property_id: The ID of the property to delete.
        
        Returns:
            A dictionary containing the API response.
        """
        response = self._client._request("DELETE", f"/properties/{property_id}")
        if response.status_code == 204:
            return {}
        return response.json() 