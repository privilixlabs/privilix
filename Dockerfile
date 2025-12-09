FROM python:3.12-alpine AS base
ENV PYTHONDONTWRITEBYTECODE = 1 \
PYTHONUNBUFFERED = 1
WORKDIR /app

FROM base AS builder
ENV PIP_NO_CACHE_DIR = off \
POETRY_NO_INTERACTION = 1 \
POETRY_HOME = "/usr/local"
COPY pyproject.toml poetry.lock ./
RUN apk add --no-cache build-base && \
pip install poetry && \
poetry install --no-interaction --no-root
COPY . .
RUN poetry install --no-interaction

FROM base AS final
ENV PATH = "/app/.venv/bin:$PATH"
COPY --from = builder /app /app
CMD ["poetry", "run", "python", "main.py"]