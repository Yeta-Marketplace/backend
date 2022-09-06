# =========== Requirements Stage ===================
FROM python:3.9 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./app/pyproject.toml ./app/poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# =============== Main Stage =======================
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

WORKDIR /app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app
ENV PYTHONPATH=/app
