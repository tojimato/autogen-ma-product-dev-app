"""GraphFlow example demonstrating message filtering.

Builds a flow where `researcher` -> `analyst` -> `presenter`, but wraps agents
with `MessageFilterAgent` and `MessageFilterConfig` to limit messages seen by
each agent, per the AutoGen docs.
"""
from __future__ import annotations

async def run_graphflow_filtering() -> None:
    """Run the GraphFlow example with MessageFilterAgent wrappers."""
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    from autogen_agentchat.agents import AssistantAgent, MessageFilterAgent, MessageFilterConfig, PerSourceFilter
    from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
    from autogen_agentchat.ui import Console

    client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    researcher = AssistantAgent(
        "researcher", model_client=client, system_message="Summarize key facts about climate change."
    )
    analyst = AssistantAgent("analyst", model_client=client, system_message="Review the summary and suggest improvements.")
    presenter = AssistantAgent(
        "presenter", model_client=client, system_message="Prepare a presentation slide based on the final summary."
    )

    filtered_analyst = MessageFilterAgent(
        name="analyst",
        wrapped_agent=analyst,
        filter=MessageFilterConfig(per_source=[PerSourceFilter(source="researcher", position="last", count=1)]),
    )

    filtered_presenter = MessageFilterAgent(
        name="presenter",
        wrapped_agent=presenter,
        filter=MessageFilterConfig(per_source=[PerSourceFilter(source="analyst", position="last", count=1)]),
    )

    builder = DiGraphBuilder()
    builder.add_node(researcher).add_node(filtered_analyst).add_node(filtered_presenter)
    builder.add_edge(researcher, filtered_analyst).add_edge(filtered_analyst, filtered_presenter)

    flow = GraphFlow(participants=builder.get_participants(), graph=builder.build())

    await Console(flow.run_stream(task="Summarize key facts about climate change."), output_stats=True)
    await client.close()
