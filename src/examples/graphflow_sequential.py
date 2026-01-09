"""GraphFlow sequential example.

This example mirrors the 'Sequential Flow' example from the AutoGen GraphFlow
docs: a writer drafts a paragraph and a reviewer provides feedback. Run via
`run_graphflow_sequential()`.
"""
from __future__ import annotations

async def run_graphflow_sequential() -> None:
    """Run the simple sequential GraphFlow example.

    Creates a writer and reviewer agent, builds a DiGraph with an edge from
    writer -> reviewer, and streams execution to the console.
    """
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
    from autogen_agentchat.ui import Console

    client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    writer = AssistantAgent("writer", model_client=client, system_message="Draft a short paragraph on climate change.")
    reviewer = AssistantAgent("reviewer", model_client=client, system_message="Review the draft and suggest improvements.")

    builder = DiGraphBuilder()
    builder.add_node(writer).add_node(reviewer)
    builder.add_edge(writer, reviewer)

    graph = builder.build()

    flow = GraphFlow([writer, reviewer], graph=graph)

    await Console(flow.run_stream(task="Write a short paragraph about climate change."), output_stats=True)
    await client.close()
