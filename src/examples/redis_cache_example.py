"""
Example: Using Redis cache with OpenAIChatCompletionClient and AutoGen

Demonstrates how to use RedisStore to cache LLM responses for efficiency.
"""
import asyncio
from autogen_core.models import UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.cache import ChatCompletionCache, CHAT_CACHE_VALUE_TYPE
from autogen_ext.cache_store.redis import RedisStore
import redis

async def run_redis_cache_example() -> None:
    """Run an example with Redis cache for LLM responses."""
    openai_model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
    redis_instance = redis.Redis()
    cache_store = RedisStore[CHAT_CACHE_VALUE_TYPE](redis_instance)
    cache_client = ChatCompletionCache(openai_model_client, cache_store)

    response1 = await cache_client.create([
        UserMessage(content="Hello, how are you?", source="user")
    ])
    print("First response (from OpenAI):", response1)

    response2 = await cache_client.create([
        UserMessage(content="Hello, how are you?", source="user")
    ])
    print("Second response (from cache):", response2)

if __name__ == "__main__":
    asyncio.run(run_redis_cache_example())
