FROM python:3.10.14-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Essensial to work with pytorch and opencv
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gettext \
    wkhtmltopdf

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
ARG USER=appuser
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/app" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    ${USER}

FROM base as build
# Poetry dependency group.
# Used differentiate image build environments.
ARG ENV
# Install poetry
RUN set -ex \
    && POETRY_VERSION="1.8.3" \
    && pip install --no-cache-dir "poetry==$POETRY_VERSION"
# Create venv to isolate project dependencies
RUN python -m venv /venv
ENV VIRTUAL_ENV="/venv"

# Move bin to venv and remove wkhtmltox installer
RUN mv /usr/bin/wkhtmltopdf /venv/bin/
RUN mv /usr/bin/wkhtmltoimage /venv/bin/
# Install project python packages:
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-interaction --no-ansi

FROM base as runtime
# Change workdir ownership
RUN chown ${USER}:${USER} /app
# Copy builded project python packages
COPY --from=build /venv /venv
# Add new venv to system path
ENV PATH="/venv/bin:$PATH"
# Copy application code to the container
# (make sure to have a .dockerignore file)
ADD src .
# Change to a non-root user
USER ${USER}:${USER}
# Uvicorn port
EXPOSE 8000
# Start Uvicorn
CMD ["python", "run.py"]
