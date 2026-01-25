"""
Mem0Memory Example - Integration with Mem0.ai's memory system.

This example demonstrates how to use Mem0Memory for advanced memory capabilities
with both cloud-based and local backends.
"""
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_core.memory import MemoryContent, MemoryMimeType
from autogen_ext.memory.mem0 import Mem0Memory
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def get_weather(city: str, units: str = "imperial") -> str:
    """Get weather information for a city."""
    if units == "imperial":
        return f"The weather in {city} is 73 °F and Sunny."
    elif units == "metric":
        return f"The weather in {city} is 23 °C and Sunny."
    else:
        return f"Sorry, I don't know the weather in {city}."


async def run_mem0_memory_example() -> None:
    """Run the Mem0Memory example."""
    print("\n=== Mem0Memory Example ===\n")
    print("Note: This example requires Mem0 API key (for cloud) or local setup.")
    print("For cloud: Set MEM0_API_KEY environment variable")
    print("For local: Use is_cloud=False with appropriate config\n")
    
    try:
        # Initialize Mem0 cloud memory (requires API key)
        # For local deployment, use is_cloud=False with appropriate config
        mem0_memory = Mem0Memory(
            is_cloud=True,
            limit=5,  # Maximum number of memories to retrieve
        )
        
        # Add user preferences to memory
        await mem0_memory.add(
            MemoryContent(
                content="The weather should be in metric units",
                mime_type=MemoryMimeType.TEXT,
                metadata={"category": "preferences", "type": "units"},
            )
        )
        await mem0_memory.add(
            MemoryContent(
                content="Meal recipe must be vegan",
                mime_type=MemoryMimeType.TEXT,
                metadata={"category": "preferences", "type": "dietary"},
            )
        )
        
        # Create assistant with mem0 memory
        assistant_agent = AssistantAgent(
            name="assistant_agent",
            model_client=OpenAIChatCompletionClient(
                model="gpt-4o-2024-08-06",
            ),
            tools=[get_weather],
            memory=[mem0_memory],
        )
        
        # Ask about the weather
        print("Task: What are my dietary preferences?\n")
        stream = assistant_agent.run_stream(task="What are my dietary preferences?")
        await Console(stream)
        
        # Serialize the memory configuration
        print("\n--- Memory Configuration ---")
        config_json = mem0_memory.dump_component().model_dump_json()
        print(f"Memory config JSON: {config_json[:100]}...")
        
        print("\n=== Mem0Memory Example Complete ===\n")
        print("\nMem0Memory is particularly useful for:")
        print("- Long-running agent deployments that need persistent memory")
        print("- Applications requiring enhanced privacy controls")
        print("- Teams wanting unified memory management across agents")
        print("- Use cases needing advanced memory filtering and analytics\n")
        
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure you have set up Mem0 correctly:")
        print("- For cloud: Set MEM0_API_KEY environment variable")
        print("- For local: Configure local Mem0 instance\n")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_mem0_memory_example())
