from dotenv import load_dotenv
from src.logger_configure import configure_logging
import asyncio
import logging
from src.agent_runner import AgentRunner
import os
import nest_asyncio
import logfire
import base64


def setup_langfuse():
    # langfuse support for OpenAI agents is a little hacky...
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


def main():
    load_dotenv()
    setup_langfuse()
    configure_logging()

    logger = logging.getLogger(__name__)
    logger.info("Starting Sierra Outfitters application")

    try:
        runner = AgentRunner()
        logger.info("Agent runner initialized, starting loop!")
        asyncio.run(runner.run())
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
    finally:
        logger.info("Application shutdown complete")


if __name__ == "__main__":
    main()
