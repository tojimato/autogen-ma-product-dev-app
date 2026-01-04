"""
Example: Human-in-the-loop with max_turns using RoundRobinGroupChat.

Demonstrates a feedback loop where the user can provide new tasks after each agent response, with max_turns=1.
"""
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

def input_func(prompt: str) -> str:
    return input(prompt)

async def run_human_in_loop_max_turn_example() -> None:
    """Run a feedback loop with max_turns=1 and user input after each turn."""
    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
    assistant = AssistantAgent("assistant", model_client=model_client)
    team = RoundRobinGroupChat([assistant], max_turns=1)
    task = "Write a 4-line poem about the ocean."
    while True:
        stream = team.run_stream(task=task)
        await Console(stream)
        task = input("Enter your feedback (type 'exit' to leave): ")
        if task.lower().strip() == "exit":
            break
    await model_client.close()

if __name__ == "__main__":
    asyncio.run(run_human_in_loop_max_turn_example())
