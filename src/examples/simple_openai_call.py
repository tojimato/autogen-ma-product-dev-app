"""
Example: Simple OpenAI call using Autogen AgentChat v0.7.5.

Demonstrates a minimal AssistantAgent interaction with OpenAIChatCompletionClient.
"""
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def run_simple_openai_example() -> None:
    """Runs a minimal OpenAI agent call using Autogen AgentChat.

    Returns:
        None
    """
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o",
        # api_key="YOUR_API_KEY",  # Use .env.local for secrets
    )

    agent = AssistantAgent(
        name="simple_agent",
        model_client=model_client,
        system_message="You are a helpful assistant.",
        reflect_on_tool_use=False,
        model_client_stream=False,
    )

    response = await agent.run(task="Hello, what can you do?")
    print("SimpleAgent response:", response)
    await model_client.close()
