# =========================
# Builder stage
# =========================
FROM python:3.13 AS builder

ENV POETRY_VERSION=2.1.3
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
    && pip install poetry==$POETRY_VERSION

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --only main

COPY . .
WORKDIR /app

RUN echo "===== CONTENTS OF /app =====" && ls -a /app
RUN python manage.py collectstatic --noinput


# =========================
# Production stage
# =========================
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN useradd -m -u 1000 appuser

WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

RUN chown -R appuser:appuser /app
USER appuser

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "webtech_lab1.wsgi:application", "--bind", "0.0.0.0:8000"]
