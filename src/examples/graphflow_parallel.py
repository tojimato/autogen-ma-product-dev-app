"""GraphFlow parallel fan-out + join example.

This example follows the AutoGen docs: a writer produces a draft, two editors
edit in parallel, then a final reviewer consolidates edits.
"""
from __future__ import annotations

async def run_graphflow_parallel() -> None:
    """Run the parallel fan-out and join GraphFlow example."""
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
    from autogen_agentchat.ui import Console

    client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    writer = AssistantAgent("writer", model_client=client, system_message="Draft a short paragraph on climate change.")
    editor1 = AssistantAgent("editor1", model_client=client, system_message="Edit the paragraph for grammar.")
    editor2 = AssistantAgent("editor2", model_client=client, system_message="Edit the paragraph for style.")
    final_reviewer = AssistantAgent(
        "final_reviewer",
        model_client=client,
        system_message="Consolidate the grammar and style edits into a final version.",
    )

    builder = DiGraphBuilder()
    builder.add_node(writer).add_node(editor1).add_node(editor2).add_node(final_reviewer)

    builder.add_edge(writer, editor1)
    builder.add_edge(writer, editor2)
    builder.add_edge(editor1, final_reviewer)
    builder.add_edge(editor2, final_reviewer)

    graph = builder.build()

    flow = GraphFlow(participants=builder.get_participants(), graph=graph)

    await Console(flow.run_stream(task="Write a short paragraph about climate change."), output_stats=True)
    await client.close()
