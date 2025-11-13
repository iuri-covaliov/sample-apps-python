# from http.server import HTTPServer
from unittest.mock import MagicMock, patch

from app.core.apiTestClient import APITestClient
from tests.conftest import AppContext, MOCK_ENV_VARS


class TestCreateApp:
    # ------------ Test Routes ------------
    def test_get_index(self, client: APITestClient) -> None:
        """Test the index route."""
        response = client.get("/")

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

        data = response.json()
        assert data["name"] == MOCK_ENV_VARS["APP_NAME"]
        assert data["description"] == MOCK_ENV_VARS["APP_DESCRIPTION"]
        assert data["version"] == MOCK_ENV_VARS["APP_VERSION"]

    def test_get_health(self, client: APITestClient) -> None:
        """Test the health route."""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

        data = response.json()
        assert data["status"] == "healthy"


class TestCreateServer:
    # ------------ Test Server Creation ------------
    def test_create_server(self, app_context: AppContext) -> None:
        # Mock the HTTPServer completely to avoid any real server creation
        mock_server_instance = MagicMock()
        mock_HTTPServer = MagicMock(return_value=mock_server_instance)

        # Mock create_app to avoid creating a real API
        mock_api = MagicMock()

        # Mock logger to suppress log messages
        mock_logger = MagicMock()

        # Import the module first, then patch HTTPServer and create_app
        import app.main

        with (
            patch.object(app.main, "HTTPServer", mock_HTTPServer),
            patch("app.main.create_app", return_value=mock_api),
        ):
            from app.main import create_server

            # Use the mock logger to suppress logs
            server = create_server(app_context.settings, mock_logger)

            assert server is not None
            # Verify that our mock HTTPServer constructor was called with expected args
            mock_HTTPServer.assert_called_once_with(("0.0.0.0", 5000), mock_api)
            # The server should be our mock instance
            assert server is mock_server_instance


class TestMainFunction:
    # ------------ Test Main Function ------------
    def test_main_initialization(self, app_context: AppContext) -> None:
        """Test that main function initializes settings, logging, etc."""
        mock_create_server = MagicMock()
        mock_server = MagicMock()
        mock_create_server.return_value = mock_server

        with patch("app.main.create_server", mock_create_server):
            from app.main import main

            main()

            mock_create_server.assert_called_once()
            mock_server.serve_forever.assert_called_once()
