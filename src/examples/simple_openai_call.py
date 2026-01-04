"""
Example: Simple OpenAI call using Autogen AgentChat v0.7.5.

Demonstrates a minimal AssistantAgent interaction with OpenAIChatCompletionClient.
"""
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.ui import Console

async def run_simple_openai_example() -> None:
    """Runs a minimal OpenAI agent call using Autogen AgentChat.

    Returns:
        None
    """
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini"       
    )

    agent = AssistantAgent(
        name="simple_agent",
        model_client=model_client,
        system_message="You are a helpful assistant.",
        reflect_on_tool_use=False,
        model_client_stream=False,
    )

    stream = agent.run_stream(task="Hello, what can you do?")
    await Console(stream)
    await model_client.close()