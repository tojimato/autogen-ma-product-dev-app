"""
Stock Research Swarm example.

Implements the Stock Research example from the AutoGen Swarm docs using a
`Swarm` of four agents: planner, financial_analyst, news_analyst, and writer.

Run:

    python -m src.examples.stock_research_swarm_example

"""
from __future__ import annotations

import asyncio
from typing import Any, Dict, List

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import Swarm
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def get_stock_data(symbol: str) -> Dict[str, Any]:
    """Mock async tool returning stock metrics for a symbol.

    Args:
        symbol: Stock ticker symbol.

    Returns:
        A dict with mock financial metrics.
    """
    await asyncio.sleep(0.05)
    return {"price": 180.25, "volume": 1_000_000, "pe_ratio": 65.4, "market_cap": "700B"}


async def get_news(query: str) -> List[Dict[str, str]]:
    """Mock async tool returning recent news items for a query.

    Args:
        query: Query string for news.

    Returns:
        A list of news dicts with `title`, `date`, and `summary`.
    """
    await asyncio.sleep(0.05)
    return [
        {"title": "Company X expands production", "date": "2024-03-20", "summary": "Production increases."},
        {"title": "Company X reports new product", "date": "2024-03-19", "summary": "New product announced."},
    ]


async def run_team_stream() -> None:
    """Builds the Swarm team and runs the stock research task, streaming to console."""
    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    planner = AssistantAgent(
        name="planner",
        model_client=model_client,
        handoffs=["financial_analyst", "news_analyst", "writer"],
        system_message=(
            "You are a research planning coordinator. Coordinate market research by "
            "delegating to specialized agents: Financial Analyst, News Analyst, and Writer. "
            "Always send your plan first, then handoff to an appropriate agent. Use TERMINATE when research is complete."
        ),
    )

    financial_analyst = AssistantAgent(
        name="financial_analyst",
        model_client=model_client,
        handoffs=["planner"],
        tools=[get_stock_data],
        system_message=(
            "You are a financial analyst. Analyze stock market data using the get_stock_data tool. "
            "Provide insights on financial metrics and handoff back to planner when done."
        ),
    )

    news_analyst = AssistantAgent(
        name="news_analyst",
        model_client=model_client,
        handoffs=["planner"],
        tools=[get_news],
        system_message=(
            "You are a news analyst. Gather and analyze relevant news using the get_news tool. "
            "Summarize key market insights and handoff back to planner when done."
        ),
    )

    writer = AssistantAgent(
        name="writer",
        model_client=model_client,
        handoffs=["planner"],
        system_message=(
            "You are a financial report writer. Compile research findings into clear, concise reports. "
            "Hand off back to planner when the report is complete."
        ),
    )

    termination = TextMentionTermination("TERMINATE")

    research_team = Swarm([planner, financial_analyst, news_analyst, writer], termination_condition=termination)

    task = "Conduct market research for TSLA stock"

    await research_team.reset()
    await Console(research_team.run_stream(task=task), output_stats=True)

    await model_client.close()


if __name__ == "__main__":
    asyncio.run(run_team_stream())
