FROM python:3.11-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir --upgrade pip \
    && pip install -r requirements.txt \
    && pip install -e .

CMD ["python", "-m", "driftmonitor.report.html.report_builder"]
