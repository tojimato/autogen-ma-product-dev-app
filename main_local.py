"""
CLI Entry Point for Product Development Multi-Agent App.

This module provides the command-line interface for running agent examples and pipelines.
It supports dependency injection and clean architecture for testability and extension.

Environment: Uses .env.local for API keys and configuration.
"""
import asyncio

from dotenv import load_dotenv
from src.examples.simple_openai_call import run_simple_openai_example
from src.utils.logging_utils import setup_logging

load_dotenv(".env.local")

async def main() -> None:
    """Main entry point """
    setup_logging()
    await run_simple_openai_example()
    

if __name__ == "__main__":
    asyncio.run(main())







