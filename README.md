# Python Sample app

Barebones for a modern Python projects.

## What is included

- **uv**: package and project manager
- **mypy**: tool for static type-check
- **ruff**: tool for linting and code formatting
- **pytest**: framework for tests + basic test suite
- **Makefile**: set of pre-configured commands for project maintainance and running the app
- **Pydantic-settings**: framework for centralized handling of the app settings (app/config.py)
- **logging**: basic logging
- **github workflow**: (!NOT IMPLEMENTED YET) basic CI/CD pipeline
- **dockerization**: basic Dockerfile and docker-compose

## Config.py and environment variables.

To keep all app settings in one place \<py-app\>/app/config.py module is used.
All settings are structurally gathered in the Settings class. If thw dotenv file exists in the \<py-app\> root directory, variables from it will overwrite default settings.

Example of the .env file you can find in the .env.example file. In general you can overwrite any setting by setting variable in the dotenv file using the following pattern:
```
<settings-subclass-variable-name>_<variable_name>=<value>
```

Example of usage:
```
# app/config.py
...
class AppSettings(BaseModel):
    NAME: str = "FastAPI Sample App"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Sample Python FastApi App"
...


class Settings(BaseSettings):
...
    APP: AppSettings = AppSettings()
...


settings = Settings()

#.env
APP_NAME=py-fastapi-sample-app-dev
APP_VERSION=local
APP_DESCRIPTION="Custom app description"
```

Now you can use the following addressing:
```
from app.config import settings

print(settings.APP.APP_NAME)
print(settings.APP.APP_VERSION)
print(settings.APP.APP_DESCRIPTION)
```
---

## Start the app
```
uv run -p app.main
# or
make run
```

## Testing

All app code could be checked and tested using:
- **Linting** check
    ```
    uv run ruff check -v app/                   # check the code
    uv run ruff check --show-files app/         # list the files for test

    # using make
    make lint
    ```
- **Code style** check
    ```
    uv run ruff format                          # auto-format
    uv run ruff format --check                  # only check styling

    # using make
    make fmt
    make fmt-check
    ```
- **Types consistency** check
    ```
    uv run mypy .                                # check the whole project
    uv run mypy app                              # perform check only for app folder

    # using make
    make type
    make type-app
    ```
- **Unit tests**: a unit tests suite with a coverage report
    ```
    uv run pytest                                 # run unit tests
    uv run coverage run -m pytest                 # run tests and calculate coverage
    uv run coverage report -m                     # show coverage report
    # run a specific test
    uv run python -m pytest tests/test_config.py::test_app_name_from_env -xvs

    # using make
    make test                                     # run unit tests
    make coverage                                 # run tests, calculate and show coverage report
    ```
---

## List of Make commands

To simplify the usage of the Python apps standardized make command added to each project.
```
• check              Quick sanity checks
• ci                 Run the same steps CI does (lint, typecheck, tests with coverage)
• coverage           Tests + HTML coverage
• deps               Install Python deps into local venv using uv
• deps-lock          Export pinned requirements for Docker/CI
• env                Create .env from .env.example if missing
• fmt                Auto-format with ruff
• fmt-check          Check code style with ruff
• help               Show this help
• lint               Lint with ruff
• run                Run the app
• test               Run unit tests
• type-app           Static type-check of the app code with mypy
• type               Static type-check of the whole project with mypy
```
---

## Dockerization

```
# build the image locally
docker compose build

# start the app on a container
docker compose up -d        # start the the container in the background
docker compose up           # start the the container with logs

# view logs
docker compose logs
```
---