import os
from pathlib import Path

from dotenv import load_dotenv

from tests.conftest import MOCK_ENV_VARS, AppContext


class TestEnv:
    def test_env_vars_loaded_from_test_env(self, app_context: AppContext) -> None:
        BASE_DIR = Path(__file__).resolve().parent.parent
        load_dotenv(dotenv_path=BASE_DIR / ".env")

        assert os.environ.get("APP_NAME") == MOCK_ENV_VARS["APP_NAME"]
        assert os.environ.get("APP_VERSION") == MOCK_ENV_VARS["APP_VERSION"]
