"""Minimal tests for API class to achieve coverage."""

import json
from unittest.mock import Mock, patch

from app.core.api import API, ApiRequestHandler


class TestAPIMinimal:
    """Minimal tests to achieve 90% coverage."""

    def test_api_initialization(self) -> None:
        """Test API instance creation."""
        api = API()
        assert "GET" in api.routing
        assert "POST" in api.routing

    def test_decorators(self) -> None:
        """Test both decorators."""
        api = API()

        @api.get("/get_route")
        def get_handler(args):
            return {"get": True}

        @api.post("/post_route")
        def post_handler(args):
            return {"post": True}

        assert "/get_route" in api.routing["GET"]
        assert "/post_route" in api.routing["POST"]

    @patch("app.core.api.ApiRequestHandler")
    def test_api_call_method(self, mock_handler_class) -> None:
        """Test the API.__call__ method (lines 82-85)."""
        api = API()
        mock_request = Mock()
        mock_address = ("127.0.0.1", 8080)
        mock_ref = Mock()
        mock_instance = Mock()
        mock_handler_class.return_value = mock_instance

        result = api(mock_request, mock_address, mock_ref)

        mock_handler_class.assert_called_once_with(
            mock_request, mock_address, mock_ref, api_ref=api
        )
        assert result is mock_instance

    def test_call_api_success(self) -> None:
        """Test call_api method success path (covers lines 15-20)."""
        api = API()

        @api.get("/test")
        def test_handler(args):
            return {"result": "success", "args": args}

        # Create handler bypassing __init__
        handler = object.__new__(ApiRequestHandler)
        handler.api = api
        handler.send_response = Mock()
        handler.end_headers = Mock()
        handler.wfile = Mock()

        handler.call_api("GET", "/test", {"input": "data"})

        handler.send_response.assert_called_with(200)
        handler.end_headers.assert_called_once()
        expected = json.dumps(
            {"result": "success", "args": {"input": "data"}}, indent=4
        ).encode()
        handler.wfile.write.assert_called_with(expected)

    def test_call_api_not_found(self) -> None:
        """Test call_api 404 path (covers lines 26-28)."""
        api = API()

        handler = object.__new__(ApiRequestHandler)
        handler.api = api
        handler.send_response = Mock()
        handler.end_headers = Mock()
        handler.wfile = Mock()

        handler.call_api("GET", "/missing", {})

        handler.send_response.assert_called_with(404, "Not Found")
        expected = json.dumps({"error": "not found"}, indent=4).encode()
        handler.wfile.write.assert_called_with(expected)

    def test_call_api_exception(self) -> None:
        """Test call_api exception path (covers lines 21-25)."""
        api = API()

        @api.get("/error")
        def error_handler(args):
            raise RuntimeError("Something broke")

        handler = object.__new__(ApiRequestHandler)
        handler.api = api
        handler.send_response = Mock()
        handler.end_headers = Mock()
        handler.wfile = Mock()

        handler.call_api("GET", "/error", {})

        handler.send_response.assert_called_with(500, "Server Error")
        expected = json.dumps({"error": ("Something broke",)}, indent=4).encode()
        handler.wfile.write.assert_called_with(expected)
