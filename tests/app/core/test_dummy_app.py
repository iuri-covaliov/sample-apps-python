from _pytest.capture import CaptureFixture
from _pytest.logging import LogCaptureFixture

from app.core.appcontext import AppContext
from app.core.dummy_app import DummyApp as App

from tests.conftest import MOCK_ENV_VARS


class TestDummyApp:
    """Test the DummyApp behavior."""

    def test_dummy_app_initialization(self, app_context: AppContext) -> None:
        """Test that DummyApp initializes correctly with given context."""
        app = App(context=app_context)

        assert app.context == app_context

    def test_print_greating(
        self, app_context: AppContext, capsys: CaptureFixture
    ) -> None:
        """Test that the greating message is printed correctly.
        Uses standard pytest fixture to capture stdout."""
        app = App(context=app_context)
        app.print_greating()

        captured = capsys.readouterr()
        assert "Welcome to" in captured.out
        assert MOCK_ENV_VARS["APP_NAME"] in captured.out
        assert MOCK_ENV_VARS["APP_VERSION"] in captured.out
        assert app_context.settings.APP.DESCRIPTION in captured.out

    def test_do_math_logs_operations(
        self, app_context: AppContext, caplog: LogCaptureFixture
    ) -> None:
        """Test that do_math method logs the correct calculations.
        Uses pytest's caplog fixture to capture log messages."""
        app = App(context=app_context)

        app.do_math()

        # Check that the log messages were captured
        assert "Addition: 15" in caplog.text
        assert "Subtraction: 5" in caplog.text
        assert "Multiplication: 50" in caplog.text
        assert "Division: 2.0" in caplog.text

    def test_run_method_starts_loop(self, app_context: AppContext) -> None:
        """Test that the run method starts the infinite loop.
        This test will run the loop in a separate thread and terminate it cleanly.

        This test is just a demo of how to handle infinite loops in tests.
        It doesn't affect coverage metrics.
        """
        import threading
        import time
        from unittest.mock import patch

        app = App(context=app_context)
        stop_event = threading.Event()

        def mock_run() -> None:
            """Mock run method that can be stopped."""
            app.print_greating()
            while not stop_event.is_set():
                time.sleep(0.01)  # Small sleep to prevent busy waiting

        # Patch the run method to use our stoppable version
        with patch.object(app, "run", side_effect=mock_run):
            app_thread = threading.Thread(target=app.run)
            app_thread.start()

            time.sleep(0.1)  # Let the app run for a short time
            assert app_thread.is_alive()

            # Clean shutdown
            stop_event.set()
            app_thread.join(timeout=1.0)  # Wait up to 1 second for clean shutdown

            assert not app_thread.is_alive()

    def test_run_method(self, app_context: AppContext, capsys: CaptureFixture) -> None:
        """Test the run method of the actual implementation.
        This test executes the real run() method and verifies its behavior."""
        import threading
        import time

        app = App(context=app_context)
        run_completed = threading.Event()

        def monitored_run() -> None:
            """Run the app and monitor its execution."""
            try:
                # This will execute the actual run() method lines 46-48
                app.run()
            except KeyboardInterrupt:
                # Expected when we interrupt the process
                run_completed.set()
            except Exception:
                # Any other exception also means we executed the method
                run_completed.set()

        # Start the app in a separate thread
        app_thread = threading.Thread(target=monitored_run, daemon=True)
        app_thread.start()

        # Let it run long enough to execute print_greating() and enter while loop
        time.sleep(0.15)

        # Verify the method is running (thread is alive = while loop is active)
        assert app_thread.is_alive(), "run() method should be executing"

        # Verify print_greating was called (line 46 coverage)
        captured = capsys.readouterr()
        assert "Welcome to" in captured.out, "print_greating() should have been called"

        # Thread cleanup happens automatically (daemon=True)
