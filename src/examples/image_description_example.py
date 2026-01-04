"""
Example: Image Description Message in AutoGen AgentChat

Demonstrates sending an image (via URL) as part of a message to an agent, following the official tutorial:
https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/messages.html
"""
from autogen_agentchat.messages import BaseChatMessage, TextMessage
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from autogen_agentchat.ui import Console
from typing import List

async def run_image_description_example() -> None:
    """Demonstrates sending an image URL in a message to an agent and getting a description.

    Returns:
        None
    """
    # Example image URL (public domain)
    image_url = "https://upload.wikimedia.org/wikipedia/commons/9/99/Black_square.jpg"
    history: List[BaseChatMessage] = [
        TextMessage(source="system", content="You are a helpful assistant that can describe images."),
        TextMessage(
            source="user",
            content= f"Describe this image. {image_url}",
        ),
    ]

    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
    agent = AssistantAgent(
        name="image_agent",
        model_client=model_client,
        system_message="You are a helpful assistant that can describe images.",
        reflect_on_tool_use=False,
        model_client_stream=False,
    )

    # Run the agent with the image message using run_stream and Console
    stream = agent.run_stream(task=history)
    await Console(stream, output_stats=True)
    await model_client.close()
