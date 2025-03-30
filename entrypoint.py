from dotenv import load_dotenv
from src.logger_configure import configure_logging
import asyncio
import logging
from src.agent_runner import AgentRunner


def main():
    load_dotenv()
    configure_logging()
    
    logger = logging.getLogger(__name__)
    logger.info("Starting Sierra Outfitters application")
    
    try:
        runner = AgentRunner()
        logger.info("Agent runner initialized, starting interaction loop")
        asyncio.run(runner.run())
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
    finally:
        logger.info("Application shutdown complete")


if __name__ == "__main__":
    main()
