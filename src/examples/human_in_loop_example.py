"""
Example: Human-in-the-loop with UserProxyAgent and AssistantAgent in a round robin team.

Demonstrates a basic interactive workflow where a user can approve or provide input.
"""
import asyncio
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def run_human_in_loop_example() -> None:
    """Run a round robin team with a human-in-the-loop via UserProxyAgent."""
    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
    
    assistant = AssistantAgent("assistant", model_client=model_client)
    user_proxy = UserProxyAgent("user_proxy", input_func=input)
    
    termination = TextMentionTermination("APPROVE")
    
    team = RoundRobinGroupChat([assistant, user_proxy], termination_condition=termination)
    
    stream = team.run_stream(task="Write a 4-line poem about the ocean.")
    
    await Console(stream, output_stats=True)
    await model_client.close()

if __name__ == "__main__":
    asyncio.run(run_human_in_loop_example())
