# Use official Python image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml poetry.lock* /app/

# Install Poetry
RUN pip install --upgrade pip && pip install poetry

# Install dependencies
RUN poetry install --no-root --no-interaction --no-ansi

# Copy rest of project
COPY . /app

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
