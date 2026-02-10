# Build stage to run container isolated tests
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS tester

WORKDIR /app

# Avoid writing to pycache
ENV PYTHONDONTWRITEBYTECODE 1
# Output logs immediately
ENV PYTHONUNBUFFERED 1

# Only install uv dependencies here for better docker layer caching
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

# Copy the project files over
COPY TwitchChannelPointsMiner ./TwitchChannelPointsMiner
COPY tests ./tests
COPY pyproject.toml uv.lock ./

# Now install the project dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Run pytest
ENTRYPOINT ["uv", "run", "pytest"]


# Separate build stage to avoid distributing build dependencies
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Disable python download, the image has it
ENV UV_PYTHON_DOWNLOADS 0
# Copy all packages
ENV UV_LINK_MODE copy
# Don't include dev dependencies (pytest, etc...)
ENV UV_NO_DEV 1

WORKDIR /app

# Only install uv dependencies here for better docker layer caching
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Copy the project files over
COPY TwitchChannelPointsMiner ./TwitchChannelPointsMiner
COPY assets ./assets
COPY pyproject.toml uv.lock ./

# Now tnstall the project dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked


# Final build stage that runs the actual miner
FROM python:3.12-slim-bookworm AS miner

WORKDIR /usr/src/app

# Setup nonroot user for better security
RUN groupadd --system --gid 997 nonroot \
    && useradd --system --gid 997 --create-home nonroot

# Copy over built project files
COPY --from=builder --chown=nonroot:nonroot /app .
# Copy LICENCE
COPY --chown=nonroot:nonroot LICENSE .

ENV PATH="/usr/src/app/.venv/bin:$PATH"

USER nonroot

ENTRYPOINT ["python", "run.py"]
