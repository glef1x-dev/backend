FROM python:3.11-slim-buster as python-base

LABEL MAINTAINER="Glib Garanin <glebgar567@gmail.com>"

# TODO fix uid and guid transportation
ARG UID=1000
ARG GUID=1000
ARG POETRY_VERSION=1.2.2

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    POETRY_VERSION=$POETRY_VERSION


ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder-base
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
    apt-get update && apt-get install --no-install-recommends -y \
        curl \
        build-essential

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://install.python-poetry.org | python -

WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --only main --no-root


# ---- Dev ----
FROM python-base as development

COPY scripts/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

WORKDIR $PYSETUP_PATH
RUN --mount=type=cache,target="$POETRY_HOME/cache" \
    --mount=type=cache,target="$POETRY_HOME/artifacts" \
    poetry install

WORKDIR /app
COPY . .

EXPOSE 8080
CMD ["/bin/sh", "-c", "/docker-entrypoint.sh"]

# ---- Production ----
FROM python-base as production
# RUN groupadd -g $GUID -r glibgaranin && useradd --uid $UID -r -g glibgaranin glibgaranin

COPY --from=builder-base $VENV_PATH $VENV_PATH

COPY scripts/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# USER glibgaranin
WORKDIR /app
COPY . .

EXPOSE 8000
CMD ["/bin/sh", "-c", "/docker-entrypoint.sh"]
