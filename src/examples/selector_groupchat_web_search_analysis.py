"""
SelectorGroupChat example: Web-search + Data Analyst flow.

This example mirrors the Autogen SelectorGroupChat demo using three agents:
- Planner: frames the task
- WebSearch: performs (mock) web lookups
- DataAnalyst: computes simple metrics

It uses `SelectorGroupChat` to let a model choose the next speaker. The demo
also shows a `selector_func` example (commented) for deterministic selection.

Run (ensure your environment has OpenAI creds in .env.local or env vars):

    python -m src.examples.selector_groupchat_web_search_analysis

Note: Keep `MaxMessageTermination` to a small value for quick smoke runs.
"""
from __future__ import annotations

import asyncio
from typing import List

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def search_web(query: str) -> List[str]:
    """Mock async web search tool.

    Args:
        query: The search query string.

    Returns:
        A list of short search result strings.
    """
    await asyncio.sleep(0.1)
    return [f"Result A for '{query}'", f"Result B for '{query}'"]


async def compute_percentage_change(values: List[float]) -> float:
    """Mock async computation tool: compute percentage change between first and last.

    Args:
        values: Numeric series with at least two values.

    Returns:
        Percentage change from first to last value.
    """
    await asyncio.sleep(0.05)
    if len(values) < 2:
        return 0.0
    start, end = values[0], values[-1]
    try:
        return ((end - start) / abs(start)) * 100.0 if start != 0 else float("inf")
    except Exception:
        return 0.0


async def main() -> None:
    """Constructs a SelectorGroupChat with three agents and runs a short task.

    This example uses `OpenAIChatCompletionClient` for speaker selection; provide
    your API key via environment or .env.local as appropriate for this repo.
    """
    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    planner = AssistantAgent(
        name="Planner",
        model_client=model_client,
        description="Frames the user's request and suggests subtasks.",
        system_message="You are the Planner. Break down high-level tasks into targeted requests for other agents.",
    )

    web_search = AssistantAgent(
        name="WebSearch",
        model_client=model_client,
        description="Performs web lookups and returns short summaries.",
        tools=[search_web],
        system_message="You are a Web Search agent. Use the provided tool to fetch short results.",
    )

    data_analyst = AssistantAgent(
        name="DataAnalyst",
        model_client=model_client,
        description="Analyzes numeric data and reports simple statistics.",
        tools=[compute_percentage_change],
        system_message="You are a Data Analyst. When given numeric lists, compute percentage changes and short insights.",
    )

    # Optional deterministic selector_func example (commented):
    # async def selector_func(messages):
    #     # If first message, pick Planner; otherwise let model decide
    #     if not messages:
    #         return "Planner"
    #     return None

    termination = MaxMessageTermination(10) | TextMentionTermination("TERMINATE")

    selector_prompt = (
        "You are the selector. Given the roles:\n{roles}\nCandidates: {participants}\n\n{history}\n\n"
        "Pick exactly one agent name from {participants} to speak next and only return the name."
    )

    team = SelectorGroupChat(
        participants=[planner, web_search, data_analyst],
        model_client=model_client,
        termination_condition=termination,
        selector_prompt=selector_prompt,
        allow_repeated_speaker=False,
    )

    task = (
        "Investigate recent price movement for ACME widget and report a short summary."
    )

    await team.reset()
    # Stream the run to console so selection decisions and messages are visible.
    await Console(team.run_stream(task=task), output_stats=True)

    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
