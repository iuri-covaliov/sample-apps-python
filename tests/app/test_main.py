from unittest.mock import MagicMock, patch

from app.core.appcontext import AppContext
# from app.main import main


class TestCreateApp:
    """Test the create_app function behavior."""

    def test_create_app_returns_app_instance(self, app_context: AppContext) -> None:
        """Test that create_app returns an App instance with correct context."""
        # Import here to avoid circular imports during testing
        from app.main import create_app
        from app.core.dummy_app import DummyApp as App

        app = create_app()

        assert app is not None
        assert isinstance(app, App)


class TestMain:
    """Test the main function behavior."""

    @patch("app.main.create_app")
    def test_main_function_calls_and_logging(
        self,
        mock_create_app: MagicMock,
        app_context: AppContext,
    ) -> None:
        """Test that main function calls create_app, do_math, run and logs correctly."""
        from app.main import main
        from app.core.dummy_app import DummyApp

        # Create a mock app instance with the required methods
        mock_app = MagicMock(spec=DummyApp)
        mock_app.context = app_context
        mock_app.context.logger = app_context.logger

        # Mock create_app to return our mock app
        mock_create_app.return_value = mock_app

        # Call main function
        main()

        # Assert create_app was called once
        mock_create_app.assert_called_once()

        # Assert do_math was called on the app
        mock_app.do_math.assert_called_once()

        # Assert run was called on the app
        mock_app.run.assert_called_once()
