"""
Example: Message Handling in AutoGen AgentChat

Demonstrates advanced message construction, BaseChatMessage usage, and message history for agents.
Based on: https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/messages.html
"""
from autogen_agentchat.messages import BaseChatMessage, TextMessage
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from autogen_agentchat.ui import Console
from typing import List

async def run_message_handling_example() -> None:
    """Demonstrates message construction and history in AutoGen AgentChat.

    Returns:
        None
    """
    # Construct a message history manually
    history: List[BaseChatMessage] = [
        TextMessage(source="system", content="You are a helpful assistant."),
        TextMessage(source="user", content="What is the capital of France?"),
    ]

    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
    agent = AssistantAgent(
        name="message_agent",
        model_client=model_client,
        system_message="You are a helpful assistant.",
        reflect_on_tool_use=False,
        model_client_stream=False,
    )

    # Run the agent with a message history using run_stream and Console
    stream = agent.run_stream(task=history)
    await Console(stream, output_stats=True)
    await model_client.close()
