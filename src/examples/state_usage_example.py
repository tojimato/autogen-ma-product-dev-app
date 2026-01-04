"""
Example: Saving and using agent team state with MaxMessageTermination.

Demonstrates how to save the state of a team after running a task.
"""
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def run_state_usage_example() -> None:
    """Run a team, stream output, and save state after execution."""
    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
    
    assistant_agent = AssistantAgent(
        name="assistant_agent",
        system_message="You are a helpful assistant",
        model_client=model_client,
    )
    
    agent_team = RoundRobinGroupChat(
        [assistant_agent],
        termination_condition=MaxMessageTermination(max_messages=2)
    )
   
    # Run the team with a task and stream output.
    stream = agent_team.run_stream(task="Write a beautiful poem 3-line about lake tangayika")
    await Console(stream, output_stats=True)
    
    # Save team state.
    team_state = await agent_team.save_state()
    
    print("Saved team state:", team_state)
    
    # Load team state.
    await agent_team.load_state(team_state)
    
    # Continue the conversation using the loaded state.
    stream = agent_team.run_stream(task="What was the last line of the poem you wrote?")
    await Console(stream, output_stats=True)
    
    # Close the model client.
    await model_client.close()

if __name__ == "__main__":
    asyncio.run(run_state_usage_example())
