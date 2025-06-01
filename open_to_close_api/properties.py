"""Properties client for Open To Close API."""

from typing import Any, Dict, List, Optional

from .base_client import BaseClient


class PropertiesAPI(BaseClient):
    """Client for properties API endpoints."""

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the properties client."""
        super().__init__(api_key=api_key, base_url=base_url)

    def list_properties(
        self, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of properties."""
        response = self.get("/properties", params=params)
        if isinstance(response, list):
            return response
        elif isinstance(response, dict):
            return response.get("data", [])
        return []

    def create_property(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new property."""
        response = self.post("/properties", json_data=property_data)
        if isinstance(response, dict) and response.get("id"):
            return response
        return response.get("data", {}) if isinstance(response, dict) else {}

    def retrieve_property(self, property_id: int) -> Dict[str, Any]:
        """Retrieve a specific property by ID."""
        response = self.get(f"/properties/{property_id}")
        if isinstance(response, dict) and response.get("id"):
            return response
        return response.get("data", {}) if isinstance(response, dict) else {}

    def update_property(
        self, property_id: int, property_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing property."""
        response = self.put(f"/properties/{property_id}", json_data=property_data)
        if isinstance(response, dict) and response.get("id"):
            return response
        return response.get("data", {}) if isinstance(response, dict) else {}

    def delete_property(self, property_id: int) -> Dict[str, Any]:
        """Delete a property by ID."""
        return self.delete(f"/properties/{property_id}")
