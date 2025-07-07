FROM python:3.12-slim-bookworm

ENV POETRY_VERSION=1.8.2 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      curl \
      build-essential \
      libpq-dev \
 && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - \
 && ln -s /root/.local/bin/poetry /usr/local/bin/poetry


WORKDIR /app

COPY pyproject.toml poetry.lock* /app/


RUN poetry install --no-dev --no-root --no-interaction
COPY . /app

RUN poetry install --no-dev --no-interaction
EXPOSE 8181

ENTRYPOINT ["poetry", "run", "python", "-m", "main"]