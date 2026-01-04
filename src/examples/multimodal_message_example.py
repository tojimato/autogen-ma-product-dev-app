"""
Example: Multi-Modal Message in AutoGen AgentChat

Demonstrates sending a PIL image as part of a multi-modal message to an agent, following the official tutorial and best practices.
"""
from io import BytesIO
import requests
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core import Image as AGImage
from PIL import Image
from autogen_agentchat.ui import Console
from typing import List

async def run_multimodal_message_example() -> None:
    """Demonstrates sending a PIL image in a multi-modal message to an agent and getting a description.

    Returns:
        None
    """
    # Download and prepare the image
    image_url = "https://picsum.photos/300/200"
    pil_image = Image.open(BytesIO(requests.get(image_url).content))
    ag_image = AGImage(pil_image)

    # Create a multi-modal message
    multi_modal_message = MultiModalMessage(
        content=["Can you describe the content of this image?", ag_image],
        source="user"
    )

    # System message for the agent
    system_message = "You are a helpful assistant that can describe images."

    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
    agent = AssistantAgent(
        name="multimodal_agent",
        model_client=model_client,
        system_message=system_message,
        reflect_on_tool_use=False,
        model_client_stream=False,
    )

    # Run the agent with the multi-modal message using run_stream and Console
    stream = agent.run_stream(task=multi_modal_message)
    await Console(stream, output_stats=True)
    await model_client.close()
