from dotenv import load_dotenv
import asyncio
import logging

from src.agent_runner import AgentRunner
from src.configure_helper import configure_logging, setup_langfuse, parse_args


def setup_environment():
    load_dotenv()
    args = parse_args()
    if args.observablity:
        setup_langfuse()
    configure_logging()


def main():
    setup_environment()

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
