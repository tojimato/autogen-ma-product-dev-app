"""
RedisMemory Example - Persistent memory storage using Redis.

This example demonstrates how to use RedisMemory for persistent memory storage.
Note: Requires a running Redis instance (local or Docker).
"""
from logging import WARNING, getLogger
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_core.memory import MemoryContent, MemoryMimeType
from autogen_ext.memory.redis import RedisMemory, RedisMemoryConfig
from autogen_ext.models.openai import OpenAIChatCompletionClient

logger = getLogger()
logger.setLevel(WARNING)


async def get_weather(city: str, units: str = "imperial") -> str:
    """Get weather information for a city."""
    if units == "imperial":
        return f"The weather in {city} is 73 °F and Sunny."
    elif units == "metric":
        return f"The weather in {city} is 23 °C and Sunny."
    else:
        return f"Sorry, I don't know the weather in {city}."


async def run_redis_memory_example() -> None:
    """Run the RedisMemory example."""
    print("\n=== RedisMemory Example ===\n")
    print("Note: This example requires a running Redis instance.")
    print("To run Redis locally: redis-server")
    print("Or via Docker: docker run -d -p 6379:6379 redis:latest\n")
    
    try:
        # Initialize Redis memory
        redis_memory = RedisMemory(
            config=RedisMemoryConfig(
                redis_url="redis://localhost:6379",
                index_name="chat_history",
                prefix="memory",
            )
        )
        
        # Add user preferences to memory
        await redis_memory.add(
            MemoryContent(
                content="The weather should be in metric units",
                mime_type=MemoryMimeType.TEXT,
                metadata={"category": "preferences", "type": "units"},
            )
        )
        await redis_memory.add(
            MemoryContent(
                content="Meal recipe must be vegan",
                mime_type=MemoryMimeType.TEXT,
                metadata={"category": "preferences", "type": "dietary"},
            )
        )
        
        # Create model client
        model_client = OpenAIChatCompletionClient(
            model="gpt-4o",
        )
        
        # Create assistant agent with Redis memory
        assistant_agent = AssistantAgent(
            name="assistant_agent",
            model_client=model_client,
            tools=[get_weather],
            memory=[redis_memory],
        )
        
        # Run the agent with a task
        print("Task: What is the weather in New York?\n")
        stream = assistant_agent.run_stream(task="What is the weather in New York?")
        await Console(stream)
        
        # Clean up
        await model_client.close()
        await redis_memory.close()
        
        print("\n=== RedisMemory Example Complete ===\n")
        
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure Redis is running on localhost:6379")
        print("You can start Redis with: docker run -d -p 6379:6379 redis:latest\n")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_redis_memory_example())
