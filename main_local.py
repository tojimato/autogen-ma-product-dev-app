"""
CLI Entry Point for Product Development Multi-Agent App.

This module provides the command-line interface for running agent examples and pipelines.
It supports dependency injection and clean architecture for testability and extension.

Environment: Uses .env.local for API keys and configuration.
"""
import asyncio

from dotenv import load_dotenv
from src.examples.simple_openai_call import run_simple_openai_example
from src.examples.message_handling_example import run_message_handling_example
from src.examples.image_description_example import run_image_description_example
from src.examples.multimodal_message_example import run_multimodal_message_example
from src.utils.logging_utils import setup_logging
import logging

load_dotenv(".env.local")
setup_logging()


import argparse

async def main() -> None:
    """Main entry point for CLI examples."""
    parser = argparse.ArgumentParser(description="Product Development Multi-Agent App CLI")
    parser.add_argument(
        "--example",
        choices=["simple", "messages", "image", "multimodal"],
        default="simple",
        help="Which example to run: 'simple' (default), 'messages', 'image', or 'multimodal' (multi-modal message)"
    )
    args = parser.parse_args()

    if args.example == "simple":
        await run_simple_openai_example()
    elif args.example == "messages":
        await run_message_handling_example()
    elif args.example == "image":
        await run_image_description_example()
    elif args.example == "multimodal":
        await run_multimodal_message_example()


if __name__ == "__main__":
    asyncio.run(main())







