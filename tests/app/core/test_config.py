from unittest.mock import MagicMock, patch

from app.core.appcontext import AppContext
from tests.conftest import MOCK_ENV_VARS


class TestSettings:
    def test_settings_init(self) -> None:
        mock_mkdir = MagicMock()
        with patch("app.core.config.Path.mkdir", mock_mkdir):
            from app.core.config import Settings

            _settings = Settings()
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

    def test_settings_take_env_vars_for_test_env(
        self,
        app_context: AppContext,
    ) -> None:
        with patch("app.core.config.Path.mkdir", MagicMock()):
            from app.core.config import Settings

            settings = Settings()

            assert settings.APP.NAME == MOCK_ENV_VARS["APP_NAME"]
            assert settings.APP.VERSION == MOCK_ENV_VARS["APP_VERSION"]
