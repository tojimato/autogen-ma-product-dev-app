"""
Example: Structured output with Pydantic model using AssistantAgent

Demonstrates how to enforce structured LLM output using a Pydantic model and output_content_type.
"""
import asyncio
from typing import Literal
from pydantic import BaseModel
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import StructuredMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.ui import Console

class AgentResponse(BaseModel):
    thoughts: str
    response: Literal["happy", "sad", "neutral"]

async def run_structured_output_example() -> None:
    """Run an agent that returns structured output using a Pydantic model."""
    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
    agent = AssistantAgent(
        name="assistant",
        model_client=model_client,
        system_message="Categorize the input as happy, sad, or neutral following the JSON format.",
        output_content_type=AgentResponse,
    )
    result = await Console(agent.run_stream(task="I am happy."), output_stats=True)
    assert result.messages, "No messages returned."
    assert isinstance(result.messages[-1], StructuredMessage)
    assert isinstance(result.messages[-1].content, AgentResponse)
    print("Thought: ", result.messages[-1].content.thoughts)
    print("Response: ", result.messages[-1].content.response)
    await model_client.close()

if __name__ == "__main__":
    asyncio.run(run_structured_output_example())
