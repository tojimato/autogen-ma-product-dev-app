"""
Example: Using a custom tool with AutoGen AgentChat

This demonstrates how to define an async tool function and use it in an AssistantAgent.
"""

import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent

async def web_search(query: str) -> str:
    """Find information on the web.
    Args:
        query (str): The search query.
    Returns:
        str: Search result summary.
    """
    # Simulate async web search (replace with real API in production)
    await asyncio.sleep(0.1)
    return "AutoGen is a programming framework for building multi-agent applications."

async def run_tool_example() -> None:
    """Run an agent with a custom tool."""
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
    )
    agent = AssistantAgent(
        name="assistant",
        description="General assistant that uses web_search tool.",
        model_client=model_client,
        tools=[web_search],
        system_message="Use tools to solve tasks.",
    )
    # Example task for the agent
    result = await agent.run(task="What is AutoGen?")
    print("Agent result:", result)
