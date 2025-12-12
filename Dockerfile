FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install -r requirements.txt

# Default command
CMD ["python", "-m", "driftmonitor.report.html.report_builder"]
