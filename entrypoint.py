from dotenv import load_dotenv
from src.logger_configure import configure_logging
import asyncio
from src.agent_runner import AgentRunner


def main():
    load_dotenv()
    configure_logging()

    runner = AgentRunner()
    asyncio.run(runner.run())


if __name__ == "__main__":
    main()
