#!/bin/bash

set -euo pipefail

# Step 0: Init ENV variables and Install the OpenTelemetry SDK
export OTEL_SERVICE_NAME=langtrace-demo-newrelic
export OTEL_EXPORTER_OTLP_ENDPOINT=https://otlp.nr-data.net
export OTEL_EXPORTER_OTLP_HEADERS="api-key=YOUR_API_KEY"



python3 -m venv venv
source ./venv/bin/activate

pip install --upgrade pip
pip install -Uq -r requirements.txt


# Step 1: Install the OpenTelemetry SDK
opentelemetry-bootstrap -a install

# Step 2: Run the application

echo "Running the application..."
opentelemetry-instrument python newrelic-langtrace.py