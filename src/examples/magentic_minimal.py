"""Minimal Magentic-One example.

This example shows how to create a simple `MagenticOneGroupChat` with a single
`AssistantAgent` and run it via the console UI. It mirrors the minimal example
from the AutoGen Magentic-One docs.
"""
from __future__ import annotations

from typing import Any


async def run_magentic_minimal() -> None:
    """Run a minimal Magentic-One example using an Assistant agent.

    This function creates an OpenAI model client, an `AssistantAgent`, and a
    `MagenticOneGroupChat`, then streams output to the console.
    """
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.teams import MagenticOneGroupChat
    from autogen_agentchat.ui import Console

    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    assistant = AssistantAgent(
        "Assistant",
        model_client=model_client,
    )

    team = MagenticOneGroupChat([assistant], model_client=model_client)
    await Console(team.run_stream(task="Provide a different proof for Fermat's Last Theorem"), output_stats=True)
    await model_client.close()
