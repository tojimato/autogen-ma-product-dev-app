"""
ListMemory Example - Simple list-based memory implementation.

This example demonstrates how to use ListMemory to maintain a memory bank
of user preferences and provide consistent context for agent responses.
"""
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_core.memory import ListMemory, MemoryContent, MemoryMimeType
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def get_weather(city: str, units: str = "imperial") -> str:
    """Get weather information for a city."""
    if units == "imperial":
        return f"The weather in {city} is 73 °F and Sunny."
    elif units == "metric":
        return f"The weather in {city} is 23 °C and Sunny."
    else:
        return f"Sorry, I don't know the weather in {city}."


async def run_listmemory_example() -> None:
    """Run the ListMemory example."""
    print("\n=== ListMemory Example ===\n")
    
    # Initialize user memory
    user_memory = ListMemory()
    
    # Add user preferences to memory
    await user_memory.add(
        MemoryContent(
            content="The weather should be in metric units",
            mime_type=MemoryMimeType.TEXT
        )
    )
    await user_memory.add(
        MemoryContent(
            content="Meal recipe must be vegan",
            mime_type=MemoryMimeType.TEXT
        )
    )
    
    # Create assistant agent with memory
    assistant_agent = AssistantAgent(
        name="assistant_agent",
        model_client=OpenAIChatCompletionClient(
            model="gpt-4o-2024-08-06",
        ),
        tools=[get_weather],
        memory=[user_memory],
    )
    
    # Run the agent with a task
    print("Task 1: What is the weather in New York?\n")
    stream = assistant_agent.run_stream(task="What is the weather in New York?")
    await Console(stream)
    
    # Inspect the model context
    print("\n--- Model Context ---")
    messages = await assistant_agent._model_context.get_messages()
    for msg in messages:
        print(f"{type(msg).__name__}: {msg}")
    
    # Ask another question to test memory retrieval
    print("\n\nTask 2: Write brief meal recipe with broth\n")
    stream = assistant_agent.run_stream(task="Write brief meal recipe with broth")
    await Console(stream)
    
    print("\n=== ListMemory Example Complete ===\n")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_listmemory_example())
