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
from src.examples.tool_usage_example import run_tool_example
from src.examples.diskcache_example import run_diskcache_example
from src.examples.redis_cache_example import run_redis_cache_example
from src.examples.structured_output_example import run_structured_output_example
from src.examples.round_robin_team_example import run_round_robin_team_example
from src.examples.human_in_loop_example import run_human_in_loop_example
from src.examples.human_in_loop_max_turn_example import run_human_in_loop_max_turn_example
from src.examples.state_usage_example import run_state_usage_example
from src.utils.logging_utils import setup_logging
from src.examples.selector_groupchat_web_search_analysis import main as run_selector_groupchat_example

load_dotenv(".env.local")
setup_logging()


import argparse

async def main() -> None:
    """Main entry point for CLI examples."""
    parser = argparse.ArgumentParser(description="Product Development Multi-Agent App CLI")
    parser.add_argument(
        "--example",
        choices=["simple", "messages", "image", "multimodal", "tool", "diskcache", "redis", "structured_output", "round_robin_team", "human_in_loop", "human_in_loop_max_turn", "state_usage", "selector_groupchat"],
        default="simple",
        help=(
            "Which example to run: 'simple' (default), 'messages', 'image', 'multimodal', 'tool', 'diskcache', 'redis', 'structured_output', 'round_robin_team', 'human_in_loop', 'human_in_loop_max_turn', or 'state_usage' (state usage example)"
        )
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
    elif args.example == "tool":
        await run_tool_example()
    elif args.example == "diskcache":
        await run_diskcache_example()
    elif args.example == "redis":
        await run_redis_cache_example()
    elif args.example == "structured_output":
        await run_structured_output_example()
    elif args.example == "round_robin_team":
        await run_round_robin_team_example()
    elif args.example == "human_in_loop":
        await run_human_in_loop_example()
    elif args.example == "human_in_loop_max_turn":
        await run_human_in_loop_max_turn_example()
    elif args.example == "state_usage":
        await run_state_usage_example()
    elif args.example == "selector_groupchat":
        await run_selector_groupchat_example()


if __name__ == "__main__":
    asyncio.run(main())







