"""
Example: RoundRobinGroupChat with primary and critic agents, and termination on approval.

Demonstrates a multi-agent workflow with a feedback loop and termination condition.
"""
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import ExternalTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.base import TaskResult

async def run_round_robin_team_example() -> None:
    """Run a team of agents in a round-robin workflow with feedback and approval termination."""
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",     
    )
    primary_agent = AssistantAgent(
        name="primary",
        model_client=model_client,
        system_message="You are a helpful AI assistant.",
    )
    critic_agent = AssistantAgent(
        name="critic",
        model_client=model_client,
        system_message="Provide constructive feedback. Respond with 'APPROVE' when your feedbacks are addressed.",
    )
    text_termination = TextMentionTermination("APPROVE")
   
    team = RoundRobinGroupChat([primary_agent, critic_agent], termination_condition=text_termination)
    
    task = "Draft a short product description for a new AI-powered notebook."
    
    # Start the team conversation
    await team.reset()  # Reset the team for a new task.   
    await Console(team.run_stream(task=task), output_stats=True)  # Stream the messages to the console.

            
if __name__ == "__main__":
    asyncio.run(run_round_robin_team_example())
