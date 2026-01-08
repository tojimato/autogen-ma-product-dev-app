"""Magentic-One example using `MultimodalWebSurfer`.

This example demonstrates creating a `MultimodalWebSurfer` agent and running it
inside a `MagenticOneGroupChat`. The snippet follows the AutoGen docs and is
meant for safe, local experimentation only.
"""
from __future__ import annotations


async def run_magentic_websurfer() -> None:
    """Run a Magentic-One team with a MultimodalWebSurfer agent."""
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    from autogen_agentchat.teams import MagenticOneGroupChat
    from autogen_agentchat.ui import Console
    from autogen_ext.agents.web_surfer import MultimodalWebSurfer

    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    surfer = MultimodalWebSurfer(
        "WebSurfer",
        model_client=model_client,
    )

    team = MagenticOneGroupChat([surfer], model_client=model_client)
    await Console(team.run_stream(task="What is the UV index in Melbourne today?"), output_stats=True)
    await model_client.close()
