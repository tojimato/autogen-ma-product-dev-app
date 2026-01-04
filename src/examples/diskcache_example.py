"""
Example: Using disk cache with OpenAIChatCompletionClient and AutoGen

Demonstrates how to use DiskCacheStore to cache LLM responses for efficiency.
"""
import asyncio
import tempfile
from autogen_core.models import UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.cache import ChatCompletionCache, CHAT_CACHE_VALUE_TYPE
from autogen_ext.cache_store.diskcache import DiskCacheStore
from diskcache import Cache

async def run_diskcache_example() -> None:
    """Run an example with disk cache for LLM responses."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        openai_model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
        cache_store = DiskCacheStore[CHAT_CACHE_VALUE_TYPE](Cache(tmpdirname))
        cache_client = ChatCompletionCache(openai_model_client, cache_store)

        response1 = await cache_client.create([
            UserMessage(content="Hello, how are you?", source="user")
        ])
        print("First response (from OpenAI):", response1)

        response2 = await cache_client.create([
            UserMessage(content="Hello, how are you?", source="user")
        ])
        print("Second response (from cache):", response2)
