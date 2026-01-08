"""Magentic-One helper usage example with approval hook.

This example shows how to use the `MagenticOne` helper class and provide an
`approval_func` for code execution approval, mirroring the AutoGen docs.
"""
from __future__ import annotations

from typing import Callable


def approval_func(request) -> object:
    """Simple approval function that prompts the user to approve code execution.

    The signature mirrors the documentation's `ApprovalRequest` -> `ApprovalResponse`.
    For simplicity, the returned object is constructed inline to avoid extra
    dependencies in this example.
    """
    print(f"Code to execute:\n{request.code}")
    user_input = input("Do you approve this code execution? (y/n): ").strip().lower()
    if user_input == "y":
        return type("ApprovalResponse", (), {"approved": True, "reason": "User approved the code execution"})()
    return type("ApprovalResponse", (), {"approved": False, "reason": "User denied the code execution"})()


async def run_magentic_helper() -> None:
    """Run the `MagenticOne` helper with a user approval callback."""
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    from autogen_ext.teams.magentic_one import MagenticOne
    from autogen_agentchat.ui import Console

    client = OpenAIChatCompletionClient(model="gpt-4o-mini")
    m1 = MagenticOne(client=client, approval_func=approval_func)
    task = "Write a Python script to fetch data from an API."
    await Console(m1.run_stream(task=task), output_stats=True)
    await client.close()
