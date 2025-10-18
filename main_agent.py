#!/usr/bin/env python3
"""
Main agent that autonomously orchestrates story generation.

The agent has access to two MCP tools:
- generate_plot: Creates a 200-word story plot from themes
- write_chapter: Writes individual chapters to files

The agent autonomously decides how to use these tools to create a complete 3-chapter story.

Usage:
    python main_agent.py "mystery, haunted lighthouse, unreliable narrator"
"""

import sys
import asyncio
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_anthropic import AnthropicAugmentedLLM


async def main():
    # Check if query was provided
    if len(sys.argv) < 2:
        print("Error: Please provide themes as a command line argument")
        print("Usage: python main_agent.py 'mystery, haunted lighthouse, unreliable narrator'")
        sys.exit(1)

    # Get the themes from command line arguments
    themes = " ".join(sys.argv[1:])

    print(f"🎬 BESTSELLER STORY GENERATOR")
    print("=" * 60)
    print(f"Themes: {themes}")
    print("=" * 60)
    print("Agent is orchestrating story generation autonomously...\n")

    # Create MCP application with config file that defines the MCP servers
    app = MCPApp(
        name="main_agent_app",
        settings="mcp_agent.config.yaml"
    )

    # Run the app context
    async with app.run() as running_app:
        # Get the context from the running app
        context = running_app.context

        # Create the main agent with access to both servers
        main_agent = Agent(
            name="story_orchestrator",
            instruction="""You are an autonomous story creation agent. You have access to two tools:

1. generate_plot: Creates a cohesive story plot from themes
2. write_chapter: Writes a chapter to a file

Your task is to create a complete 3-chapter story. You should:
1. First, use generate_plot to create the overall story plot
2. Based on that plot, create a mental outline for 3 chapters
3. Use write_chapter to write each of the chapters sequentially
4. For each chapter, provide the chapter number, the overall plot, a brief outline for that specific chapter, and a summary of previous chapters

Be autonomous - figure out the chapter outlines yourself and orchestrate the entire process.
Keep your responses concise and focus on executing the task.""",
            server_names=["plot-generator", "chapter-writer"],
            context=context
        )

        # Initialize the agent
        await main_agent.initialize()

        try:
            # Attach LLM to the main agent
            llm = await main_agent.attach_llm(AnthropicAugmentedLLM)

            # Give the agent the task and let it orchestrate everything
            task = f"""Create a complete 3-chapter story with these themes: {themes}

Steps you should take:
1. Use the generate_plot tool to create the overall plot
2. Plan out chapters based on that plot
3. Use the write_chapter tool to write each chapter
4. Ensure each chapter builds on the previous ones

Begin now and work through each step autonomously."""

            # Let the agent work autonomously
            result = await llm.generate_str(task)

            print("\n" + "="*60)
            print("✅ STORY GENERATION COMPLETE!")
            print("="*60)
            print(result)
            print("="*60 + "\n")

        finally:
            # Clean up
            await main_agent.close()


if __name__ == "__main__":
    asyncio.run(main())
