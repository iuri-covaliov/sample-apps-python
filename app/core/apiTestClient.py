"""TestClient for HTTP API testing - similar to FastAPI's TestClient.

Allows testing HTTP endpoints without making real network requests.
"""

import json
from typing import Any, Dict, Optional

from app.core.api import API


class APITestResponse:
    """Mock HTTP response object."""

    def __init__(
        self, status_code: int, content: bytes, headers: Optional[Dict[str, str]] = None
    ):
        self.status_code = status_code
        self.content = content
        self.headers = headers or {}

    def json(self) -> Any:
        """Parse response content as JSON."""
        return json.loads(self.content.decode())

    @property
    def text(self) -> str:
        """Return response content as text."""
        return self.content.decode()

    def __repr__(self) -> str:
        return f"<APITestResponse [{self.status_code}]>"


class APITestClient:
    """Test client for making requests to the API without a real server."""

    def __init__(self, api: API):
        """Initialize test client with an API instance."""
        self.api = api

    def get(
        self, path: str, params: Optional[Dict[str, Any]] = None
    ) -> APITestResponse:
        """Make a GET request."""
        return self._make_request("GET", path, params=params)

    def post(
        self,
        path: str,
        json: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> APITestResponse:
        """Make a POST request."""
        return self._make_request("POST", path, params=params, json_data=json)

    def _make_request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Any] = None,
    ) -> APITestResponse:
        """Make a mock HTTP request to the API."""
        try:
            # Check if route exists
            if method in self.api.routing and path in self.api.routing[method]:
                # Get the route function
                route_func = self.api.routing[method][path]

                # Prepare arguments based on method
                if method == "GET":
                    # Use query parameters as args
                    args = params if params is not None else {}
                elif method == "POST":
                    # Use JSON data as args
                    args = json_data if json_data is not None else {}
                else:
                    args = {}

                # Call the route function
                result = route_func(args)

                # Create success response
                response_body = json.dumps(result, indent=4).encode()
                headers = {"content-type": "application/json"}
                return APITestResponse(200, response_body, headers)
            else:
                # 404 response
                error_response = {"error": "not found"}
                response_body = json.dumps(error_response, indent=4).encode()
                headers = {"content-type": "application/json"}
                return APITestResponse(404, response_body, headers)

        except Exception as e:
            # 500 response for errors
            error_response = {"error": str(e)}
            response_body = json.dumps(error_response, indent=4).encode()
            headers = {"content-type": "application/json"}
            return APITestResponse(500, response_body, headers)
