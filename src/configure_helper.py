import logging
import os
import base64
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="A helpful AI agent for Sierra Outfitters")
    parser.add_argument(
        "--observablity",
        "-o",
        action="store_true",
        help="Send traces to Langsmith and print succint logs to terminal"
    )

    return parser.parse_args()


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log")
        ]
    )


def setup_langfuse():
    # importing here to make it easier to run during interview in case interviewer doesnt have these installed
    import nest_asyncio
    import logfire

    # langfuse support for OpenAI agents is a little hacky...
    # https://langfuse.com/docs/integrations/openaiagentssdk/openai-agents
    LANGFUSE_AUTH = base64.b64encode(
        f"{os.environ.get('LANGFUSE_PUBLIC_KEY')}:{os.environ.get('LANGFUSE_SECRET_KEY')}".encode()
    ).decode()
    
    # Configure OpenTelemetry endpoint & headers
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = os.environ.get("LANGFUSE_HOST") + "/api/public/otel"
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"
    
    nest_asyncio.apply()
     
    # Configure logfire instrumentation.
    logfire.configure(service_name='my_agent_service', send_to_logfire=False)
    logfire.instrument_openai_agents()
