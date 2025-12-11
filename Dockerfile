# DriftMonitor Dockerfile (lightweight)

FROM python:3.11-slim

# Install system deps (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy full project
COPY . /app

# Default environment variable (optional)
ENV PYTHONUNBUFFERED=1

# Default command runs report builder (you can override)
CMD ["python", "-m", "driftmonitor.report.html.report_builder"]
