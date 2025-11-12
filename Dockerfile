FROM python:3.12-slim-trixie

ARG MODE=DEV
ARG PORT=5000

ENV MODE=${MODE}
ENV PORT=${PORT}

# add uv and uvx from astral-sh/uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create non-root user early
RUN addgroup --system appgroup && \
    adduser --system --group appuser --home /home/appuser

# Create and set permissions for working directory
RUN mkdir -p /home/appuser/src && \
    chown -R appuser:appgroup /home/appuser

WORKDIR /home/appuser/src

# Switch to non-root user early
USER appuser

# Install app dependencies to .venv (as appuser)
COPY --chown=appuser:appgroup .python-version pyproject.toml ./
RUN \
  if [ "$MODE" = "PROD" ]; \
  then \
    uv sync --no-dev; \
  else \
    uv sync; \
  fi

# Bundle app source
COPY --chown=appuser:appgroup ./app ./app

# Copy tests only in non-production mode  
COPY --chown=appuser:appgroup ./tests ./tests
USER root
RUN if [ "$MODE" = "PROD" ]; then rm -rf ./tests; fi
USER appuser

# Expose the app port
EXPOSE $PORT

CMD [ "uv", "run", "-m", "app.main" ]