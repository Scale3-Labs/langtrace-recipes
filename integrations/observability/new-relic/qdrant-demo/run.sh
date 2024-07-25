#!/bin/bash

set -euo pipefail

# Step 0: Init ENV variables and Install the OpenTelemetry SDK
export OTEL_SERVICE_NAME=qdrant-demo
export OTEL_RESOURCE_ATTRIBUTES=service.instance.id=123
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
export OTEL_EXPORTER_OTLP_ENDPOINT=https://otlp.nr-data.net
export OTEL_EXPORTER_OTLP_HEADERS=api-key=a7c8ff2457d19e80915d798ecce12a6dFFFFNRAL
export OTEL_ATTRIBUTE_VALUE_LENGTH_LIMIT=4095
export OTEL_EXPORTER_OTLP_COMPRESSION=gzip
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf 
export OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE=delta
export OTEL_PYTHON_DISABLED_INSTRUMENTATIONS=aws-lambda
python3 -m venv venv
source ./venv/bin/activate

pip install --upgrade pip

# How to get the requirements.txt file?
# 1. Follow https://opentelemetry.io/docs/languages/python/getting-started/
# 2. Run `pip freeze > requirements.txt` in the same directory as your app.py file
pip install -Uq -r requirements.txt
pip install langtrace-python-sdk --upgrade

# Step 1: Install the OpenTelemetry SDK
opentelemetry-bootstrap -a install

# Step 2: Run the application

echo "Running the application..."
opentelemetry-instrument python qdrant-demo.py
