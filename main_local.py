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
from src.examples.refund_flight_swarm_example import run_team_stream as run_refund_flight_example
from src.examples.stock_research_swarm_example import run_team_stream as run_stock_research_example
from src.examples.magentic_minimal import run_magentic_minimal
from src.examples.magentic_websurfer import run_magentic_websurfer
from src.examples.magentic_helper import run_magentic_helper
from src.examples.graphflow_sequential import run_graphflow_sequential
from src.examples.graphflow_parallel import run_graphflow_parallel
from src.examples.graphflow_filtering import run_graphflow_filtering
from src.examples.graphflow_advanced import run_graphflow_advanced

load_dotenv(".env.local")
setup_logging()


import argparse

async def main() -> None:
    """Main entry point for CLI examples."""
    parser = argparse.ArgumentParser(description="Product Development Multi-Agent App CLI")
    parser.add_argument(
        "--example",
        choices=[
            "simple",
            "messages",
            "image",
            "multimodal",
            "tool",
            "diskcache",
            "redis",
            "structured_output",
            "round_robin_team",
            "human_in_loop",
            "human_in_loop_max_turn",
            "state_usage",
            "selector_groupchat",
            "refund_flight",
            "stock_research",
            "magentic_minimal",
            "magentic_websurfer",
            "magentic_helper",
            "graph_sequential",
            "graph_parallel",
            "graph_filtering",
            "graph_advanced",
        ],
        default="simple",
        help=(
            "Which example to run: 'simple' (default), 'messages', 'image', 'multimodal', 'tool', 'diskcache', 'redis', 'structured_output', 'round_robin_team', 'human_in_loop', 'human_in_loop_max_turn', 'state_usage', 'selector_groupchat', 'refund_flight', 'stock_research', 'magentic_minimal', 'magentic_websurfer', 'magentic_helper'"
        ),
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
    elif args.example == "refund_flight":
        await run_refund_flight_example()
    elif args.example == "stock_research":
        await run_stock_research_example()
    elif args.example == "magentic_minimal":
        await run_magentic_minimal()
    elif args.example == "magentic_websurfer":
        await run_magentic_websurfer()
    elif args.example == "magentic_helper":
        await run_magentic_helper()
    elif args.example == "graph_sequential":
        await run_graphflow_sequential()
    elif args.example == "graph_parallel":
        await run_graphflow_parallel()
    elif args.example == "graph_filtering":
        await run_graphflow_filtering()
    elif args.example == "graph_advanced":
        await run_graphflow_advanced()


if __name__ == "__main__":
    asyncio.run(main())







