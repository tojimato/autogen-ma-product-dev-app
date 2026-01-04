"""
CLI Entry Point for Product Development Multi-Agent App.

This module provides the command-line interface for running agent examples and pipelines.
It supports dependency injection and clean architecture for testability and extension.

Environment: Uses .env.local for API keys and configuration.
"""

import argparse
import asyncio
import logging
from dotenv import load_dotenv
from autogen_core import EVENT_LOGGER_NAME
from src.examples.simple_openai_call import run_simple_openai_example

load_dotenv(".env.local")

def setup_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger(EVENT_LOGGER_NAME)
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)

async def main() -> None:
    """Main entry point """
    setup_logging()
    await run_simple_openai_example()
    

if __name__ == "__main__":
    asyncio.run(main())







