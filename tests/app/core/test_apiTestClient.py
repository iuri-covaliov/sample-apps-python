"""Tests for the APITestClient functionality."""

import json
from typing import Any
import pytest
from app.core.api import API
from app.core.apiTestClient import APITestClient, APITestResponse


@pytest.fixture
def api() -> API:
    """Create an API instance with test routes."""
    api_instance = API()

    @api_instance.get("/hello")
    def hello_handler(args: dict) -> dict:
        return {"message": "Hello, World!", "args": args}

    @api_instance.post("/echo")
    def echo_handler(args: dict) -> dict:
        return {"received": args, "status": "ok"}

    @api_instance.get("/users")
    def users_handler(args: dict) -> dict:
        # Simulate a users endpoint that returns filtered results
        users = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
            {"id": 3, "name": "Charlie"},
        ]

        # Filter by name if provided
        if "name" in args:
            name_str = str(args["name"]) if args["name"] is not None else ""
            users = [u for u in users if name_str.lower() in str(u["name"]).lower()]

        return {"users": users, "count": len(users)}

    return api_instance


@pytest.fixture
def client(api: API) -> APITestClient:
    """Create an APITestClient instance."""
    return APITestClient(api)


class TestAPITestClient:
    """Test the APITestClient functionality."""

    def test_get_request_no_params(self, client: APITestClient) -> None:
        """Test GET request without parameters."""
        response = client.get("/hello")

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

        data = response.json()
        assert data["message"] == "Hello, World!"
        assert data["args"] == {}

    def test_get_request_with_params(self, client):
        """Test GET request with query parameters."""
        response = client.get("/hello", params={"name": "test", "value": "42"})

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Hello, World!"
        assert data["args"]["name"] == "test"
        assert data["args"]["value"] == "42"

    def test_post_request(self, client):
        """Test POST request with JSON data."""
        test_data = {"name": "test", "data": [1, 2, 3]}
        response = client.post("/echo", json=test_data)

        assert response.status_code == 200
        data = response.json()
        assert data["received"] == test_data
        assert data["status"] == "ok"

    def test_post_request_no_data(self, client):
        """Test POST request without data."""
        response = client.post("/echo")

        assert response.status_code == 200
        data = response.json()
        assert data["received"] == {}
        assert data["status"] == "ok"

    def test_404_response(self, client):
        """Test 404 response for non-existent route."""
        response = client.get("/nonexistent")

        assert response.status_code == 404
        data = response.json()
        assert data["error"] == "not found"

    def test_complex_filtering(self, client):
        """Test more complex endpoint with filtering."""
        # Get all users
        response = client.get("/users")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 3
        assert len(data["users"]) == 3

        # Filter by name
        response = client.get("/users", params={"name": "bob"})
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1
        assert data["users"][0]["name"] == "Bob"

    def test_response_properties(self, client):
        """Test APITestResponse properties and methods."""
        response = client.get("/hello")

        # Test status_code property
        assert response.status_code == 200

        # Test headers property
        assert isinstance(response.headers, dict)
        assert response.headers["content-type"] == "application/json"

        # Test content property (bytes)
        assert isinstance(response.content, bytes)

        # Test text property (string)
        assert isinstance(response.text, str)
        assert "Hello, World!" in response.text

        # Test json() method
        data = response.json()
        assert isinstance(data, dict)
        assert data["message"] == "Hello, World!"

        # Test __repr__ method
        repr_str = repr(response)
        assert "APITestResponse" in repr_str
        assert "200" in repr_str


class TestAPITestResponse:
    """Test the APITestResponse class specifically."""

    def test_response_with_custom_headers(self):
        """Test APITestResponse with custom headers."""
        custom_headers = {"x-custom": "header", "content-type": "application/xml"}
        content = b"<xml>test</xml>"
        response = APITestResponse(201, content, custom_headers)

        assert response.status_code == 201
        assert response.headers == custom_headers
        assert response.content == content
        assert response.text == "<xml>test</xml>"

    def test_response_without_headers(self):
        """Test APITestResponse with None headers (default to empty dict)."""
        response = APITestResponse(204, b"", None)

        assert response.status_code == 204
        assert response.headers == {}
        assert response.content == b""
        assert response.text == ""

    def test_json_parsing_error(self):
        """Test APITestResponse.json() with invalid JSON."""
        response = APITestResponse(200, b"invalid json{", {})

        with pytest.raises(json.JSONDecodeError):
            response.json()

    def test_repr_with_different_status_codes(self):
        """Test __repr__ with various status codes."""
        response_200 = APITestResponse(200, b"{}", {})
        response_404 = APITestResponse(404, b"{}", {})
        response_500 = APITestResponse(500, b"{}", {})

        assert repr(response_200) == "<APITestResponse [200]>"
        assert repr(response_404) == "<APITestResponse [404]>"
        assert repr(response_500) == "<APITestResponse [500]>"


class TestAPITestClientEdgeCases:
    """Test edge cases and error conditions for APITestClient."""

    def test_unsupported_http_method(self):
        """Test _make_request with unsupported HTTP method."""
        api = API()

        @api.get("/test")
        def test_handler(args: Any) -> Any:
            return {"test": True}

        client = APITestClient(api)
        # Test with unsupported method (not GET or POST)
        response = client._make_request("PUT", "/test")

        assert response.status_code == 404
        assert response.json()["error"] == "not found"

    def test_route_handler_exception(self):
        """Test when route handler raises an exception."""
        api = API()

        @api.get("/error")
        def error_handler(args: dict) -> None:
            raise ValueError("Something went wrong")

        client = APITestClient(api)
        response = client.get("/error")

        assert response.status_code == 500
        assert "Something went wrong" in response.json()["error"]

    def test_route_handler_with_none_return(self):
        """Test route handler that returns None."""
        api = API()

        @api.get("/none")
        def none_handler(args: dict) -> None:
            return None

        client = APITestClient(api)
        response = client.get("/none")

        assert response.status_code == 200
        assert response.json() is None

    def test_route_handler_with_complex_data_types(self):
        """Test route handler with complex data structures."""
        api = API()

        @api.post("/complex")
        def complex_handler(args: Any) -> Any:
            return {
                "received": args,
                "complex": {
                    "nested": {"deeply": [1, 2, {"key": "value"}]},
                    "list": [{"a": 1}, {"b": 2}],
                },
            }

        client = APITestClient(api)
        test_data = {
            "nested": {"obj": {"value": 42}},
            "array": [1, 2, 3],
            "boolean": True,
            "null": None,
        }
        response = client.post("/complex", json=test_data)

        assert response.status_code == 200
        result = response.json()
        assert result["received"] == test_data
        assert result["complex"]["nested"]["deeply"][2]["key"] == "value"

    def test_get_with_empty_params(self):
        """Test GET request with empty params dict."""
        api = API()

        @api.get("/empty")
        def empty_handler(args: Any) -> Any:
            return {"args": args}

        client = APITestClient(api)
        response = client.get("/empty", params={})

        assert response.status_code == 200
        assert response.json()["args"] == {}

    def test_post_with_params_and_json(self):
        """Test POST request with both params and JSON data."""
        api = API()

        @api.post("/both")
        def both_handler(args: Any) -> Any:
            return {"json_args": args}

        client = APITestClient(api)
        response = client.post(
            "/both", json={"key": "value"}, params={"ignored": "param"}
        )

        assert response.status_code == 200
        # For POST requests, JSON data takes precedence over params
        assert response.json()["json_args"] == {"key": "value"}

    def test_route_not_in_routing_dict(self):
        """Test accessing route when method not in routing dict."""
        api = API()
        # Don't add any routes, so routing dict is empty

        client = APITestClient(api)
        response = client.get("/anything")

        assert response.status_code == 404
        assert response.json()["error"] == "not found"

    def test_route_handler_json_serialization_error(self):
        """Test when route handler returns non-JSON serializable data."""
        api = API()

        @api.get("/bad-json")
        def bad_json_handler(args: dict) -> dict:
            # Return a function (not JSON serializable)
            return {"func": lambda x: x}

        client = APITestClient(api)
        response = client.get("/bad-json")

        assert response.status_code == 500
        assert "error" in response.json()

    def test_multiple_clients_with_same_api(self):
        """Test multiple client instances with the same API."""
        api = API()

        @api.get("/shared")
        def shared_handler(args: Any) -> Any:
            return {"client": "response"}

        client1 = APITestClient(api)
        client2 = APITestClient(api)

        response1 = client1.get("/shared")
        response2 = client2.get("/shared")

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response1.json() == response2.json()

    def test_client_with_empty_api(self):
        """Test client with API that has no routes."""
        api = API()
        client = APITestClient(api)

        response = client.get("/any-path")
        assert response.status_code == 404

        response = client.post("/any-path")
        assert response.status_code == 404

    def test_custom_http_method_with_route_found(self):
        """Test _make_request with custom HTTP method when route exists."""
        api = API()

        # Manually add a custom HTTP method to the routing
        api.routing["PATCH"] = {}

        @api.get("/test")  # We'll add this to PATCH manually
        def test_handler(args: Any) -> Any:
            return {"method": "PATCH", "args": args}

        # Manually add the route to PATCH method
        api.routing["PATCH"]["/test"] = test_handler

        client = APITestClient(api)
        # Test the custom method - this should hit the 'else: args = {}' line
        response = client._make_request("PATCH", "/test")

        assert response.status_code == 200
        result = response.json()
        assert result["method"] == "PATCH"
        assert result["args"] == {}  # Should be empty dict due to 'else' clause
