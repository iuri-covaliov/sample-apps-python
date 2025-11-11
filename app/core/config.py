from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = (
    Path(__file__).resolve().parent.parent.parent
)  # go up from app/ to project root

load_dotenv()


class AppSettings(BaseModel):
    NAME: str = "My Python App"
    DATA_DIR: Path = BASE_DIR / "data"
    DESCRIPTION: str = "Python App Barebones"
    VERSION: str = "0.1.0"


class LoggingSettings(BaseModel):
    LEVEL: str = "INFO"
    FORMAT: str = "[%(levelname)s|%(module)s|line:%(lineno)d] %(asctime)s: %(message)s"
    DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        # This lets ENV_VARS like APP__NAME map into app.name etc.
        env_nested_delimiter="_",
        extra="ignore",  # Ignore unknown env vars
    )

    APP: AppSettings = AppSettings()
    LOGGING: LoggingSettings = LoggingSettings()

    def __init__(self) -> None:
        super().__init__()
        # Ensure app data directories exist
        self.APP.DATA_DIR.mkdir(parents=True, exist_ok=True)
