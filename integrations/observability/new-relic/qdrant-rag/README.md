# Langtrace to New Relic Integration

This project demonstrates how to use Langtrace with OpenAI and Qdrant to create a Retrieval-Augmented Generation (RAG) system, and send traces to New Relic using OpenTelemetry.

## Prerequisites

- Python 3.x
- A New Relic [account](https://docs.newrelic.com/docs/apis/intro-apis/new-relic-api-keys/) with an API key
- An [OpenAI API](https://platform.openai.com/api-keys) key

## Setup

1. Clone this repository:

   ```
   git clone https://github.com/Scale3-Labs/langtrace-recipes.git
   cd integrations/observability/new-relic/qdrant-rag
   ```

2. Create a `.env` file in the project root with the following content:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. Open the `run.sh` file and replace `YOUR_API_KEY` in the `OTEL_EXPORTER_OTLP_HEADERS` line with your actual New Relic API key.

## Running the Application

1. Make the run script executable:

   ```
   chmod +x run.sh
   ```

2. Run the script:
   ```
   ./run.sh
   ```

This script will:

- Set up the necessary environment variables
- Create and activate a Python virtual environment
- Install required packages
- Install the OpenTelemetry SDK
- Run the application with OpenTelemetry instrumentation

## What the Application Does

The application (`newrelic-langtrace.py`):

1. Initializes a knowledge base with sample documents
2. Demonstrates a RAG system by asking predefined questions
3. Sends traces to New Relic for monitoring

## Viewing Traces in New Relic

After running the application:

1. Log into your New Relic account
2. Navigate to the APM (Application Performance Monitoring) section
3. Look for traces labeled with the service name "langtrace-demo-newrelic"
4. Examine the 'rag' root spans and their child spans to understand the flow and performance of your RAG system

## Troubleshooting

- If you encounter any issues with API keys, make sure they are correctly set in the `.env` file and `run.sh` script.
- Ensure all required packages are listed in `requirements.txt`.
- Check the console output for any error messages during execution.
