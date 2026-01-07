"""
Customer support Swarm example (flights refund) — mirrors the Autogen docs' Customer Support example.

This example implements two agents in a `Swarm`:
- `travel_agent`: evaluates user requests and delegates refund tasks.
- `flights_refunder`: requests flight reference numbers and calls `refund_flight`.

When an agent needs information from the user, it hands off to the special target
`"user"`. The example demonstrates the human-in-the-loop pattern where the program
prompts the local user for input and resumes the swarm with a `HandoffMessage`.

Run:

    python -m src.examples.refund_flight_swarm_example

"""
from __future__ import annotations

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import HandoffTermination, TextMentionTermination
from autogen_agentchat.messages import HandoffMessage
from autogen_agentchat.teams import Swarm
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


def refund_flight(flight_id: str) -> str:
    """Mock refund tool.

    In the real world this would call a payments/refunds API.
    """
    return f"Flight {flight_id} refunded"


async def run_team_stream() -> None:
    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    travel_agent = AssistantAgent(
        name="travel_agent",
        model_client=model_client,
        handoffs=["flights_refunder", "user"],
        system_message=(
            "You are a travel agent. The flights_refunder is in charge of refunding flights. "
            "If you need information from the user, you must first send your message, then "
            "handoff to the user. Use TERMINATE when the travel planning is complete."
        ),
    )

    flights_refunder = AssistantAgent(
        name="flights_refunder",
        model_client=model_client,
        handoffs=["travel_agent", "user"],
        tools=[refund_flight],
        system_message=(
            "You are an agent specialized in refunding flights. You only need flight reference "
            "numbers to refund a flight. Use the refund_flight tool when provided with a flight id. "
            "If you need information from the user, send your message then handoff to the user. "
            "When the transaction is complete, handoff to the travel_agent to finalize."
        ),
    )

    termination = HandoffTermination(target="user") | TextMentionTermination("TERMINATE")

    team = Swarm([travel_agent, flights_refunder], termination_condition=termination)

    task = "I need to refund my flight."

    await team.reset()

    # First run: stream messages until termination or a handoff-to-user occurs.
    task_result = await Console(team.run_stream(task=task), output_stats=True)

    # If the last message is a handoff to the user, prompt and resume.
    last_message = task_result.messages[-1]
    while isinstance(last_message, HandoffMessage) and last_message.target == "user":
        user_message = input("User: ")
        task_result = await Console(
            team.run_stream(task=HandoffMessage(source="user", target=last_message.source, content=user_message))
        )
        last_message = task_result.messages[-1]

    await model_client.close()
