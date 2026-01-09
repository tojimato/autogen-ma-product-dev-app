"""Advanced GraphFlow examples: conditional loop and activation groups.

This module includes the 'Conditional Loop + Filtered Summary' example and
illustrative activation-group scenarios from the AutoGen docs.
"""
from __future__ import annotations

async def run_graphflow_advanced() -> None:
    """Run advanced GraphFlow examples (conditional loop + activation groups)."""
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    from autogen_agentchat.agents import (
        AssistantAgent,
        MessageFilterAgent,
        MessageFilterConfig,
        PerSourceFilter,
    )
    from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
    from autogen_agentchat.conditions import MaxMessageTermination
    from autogen_agentchat.ui import Console

    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    # Conditional loop + filtered summarizer
    generator = AssistantAgent("generator", model_client=model_client, system_message="Generate a list of creative ideas.")
    reviewer = AssistantAgent(
        "reviewer",
        model_client=model_client,
        system_message="Review ideas and provide feedbacks, or just 'APPROVE' for final approval.",
    )
    summarizer_core = AssistantAgent("summary", model_client=model_client, system_message="Summarize the user request and the final feedback.")

    filtered_summarizer = MessageFilterAgent(
        name="summary",
        wrapped_agent=summarizer_core,
        filter=MessageFilterConfig(
            per_source=[
                PerSourceFilter(source="user", position="first", count=1),
                PerSourceFilter(source="reviewer", position="last", count=1),
            ]
        ),
    )

    builder = DiGraphBuilder()
    builder.add_node(generator).add_node(reviewer).add_node(filtered_summarizer)
    builder.add_edge(generator, reviewer)
    # reviewer -> summary when APPROVE; else reviewer -> generator (loop)
    builder.add_edge(reviewer, filtered_summarizer, condition=lambda msg: "APPROVE" in msg.to_model_text())
    builder.add_edge(reviewer, generator, condition=lambda msg: "APPROVE" not in msg.to_model_text())
    builder.set_entry_point(generator)

    termination_condition = MaxMessageTermination(10)

    graph = builder.build()
    flow = GraphFlow(participants=builder.get_participants(), graph=graph, termination_condition=termination_condition)

    await Console(flow.run_stream(task="Brainstorm ways to reduce plastic waste."), output_stats=True)

    # Activation-group examples (illustrative build only)
    # Example 1: A -> B -> C -> B with 'all' activation
    client = model_client
    agent_a = AssistantAgent("A", model_client=client, system_message="Start the process and provide initial input.")
    agent_b = AssistantAgent("B", model_client=client, system_message="Process input from A or feedback from C. Say 'CONTINUE' if it's from A or 'STOP' if it's from C.")
    agent_c = AssistantAgent("C", model_client=client, system_message="Review B's output and provide feedback.")
    agent_e = AssistantAgent("E", model_client=client, system_message="Finalize the process.")

    builder2 = DiGraphBuilder()
    builder2.add_node(agent_a).add_node(agent_b).add_node(agent_c).add_node(agent_e)
    builder2.add_edge(agent_a, agent_b, activation_group="initial")
    builder2.add_edge(agent_b, agent_c)
    builder2.add_edge(agent_c, agent_b, activation_group="feedback")
    builder2.add_edge(agent_b, agent_e, condition=lambda msg: "STOP" in msg.to_model_text())

    graph2 = builder2.build()
    flow2 = GraphFlow(participants=[agent_a, agent_b, agent_c, agent_e], graph=graph2, termination_condition=MaxMessageTermination(10))

    # Example 2 and 3 are similar; building them is straightforward per docs.
    await client.close()
