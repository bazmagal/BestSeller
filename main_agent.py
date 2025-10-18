#!/usr/bin/env python3
"""
Main agent that uses the continent helper MCP server.

Usage:
    python main_agent.py "Paris is a beautiful city in France"
"""

import sys
import asyncio
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_anthropic import AnthropicAugmentedLLM
from mcp_agent.logging.logger import get_logger

logger = get_logger(__name__)


async def main():
    # Check if query was provided
    if len(sys.argv) < 2:
        print("Error: Please provide a text as a command line argument")
        print("Usage: python main_agent.py 'Your text here'")
        sys.exit(1)

    # Check if API key is set (or it will be loaded from config)
    # if not os.environ.get("ANTHROPIC_API_KEY"):
    #     print("Error: ANTHROPIC_API_KEY environment variable not set")
    #     print("Set it with: export ANTHROPIC_API_KEY='your-api-key-here'")
    #     sys.exit(1)

    # Get the text from command line arguments
    text = " ".join(sys.argv[1:])

    print(f"Input text: {text}\n")
    print("=" * 60)

    # Create MCP application with config file that defines the MCP servers
    app = MCPApp(
        name="main_agent_app",
        settings="mcp_agent.config.yaml"
    )

    # Run the app context
    async with app.run() as running_app:
        # Get the context from the running app
        context = running_app.context

        # Create the main agent with access to the continent helper server
        main_agent = Agent(
            name="main_agent",
            instruction="""You are a helpful assistant. When asked about continents, use the identify_continent tool.""",
            server_names=["continent-helper"],
            context=context
        )

        # Initialize the agent
        await main_agent.initialize()

        try:
            # Attach LLM to the main agent
            llm = await main_agent.attach_llm(AnthropicAugmentedLLM)

            print("\n[Main Agent] Analyzing text using continent helper MCP server...\n")

            # Create a simple query
            query = f'Identify the continent for this text: "{text}"'

            # Use generate_str which handles tool calls and returns final text response
            result = await llm.generate_str(query)

            logger.info(f"Continent: {result}")

        finally:
            # Clean up
            await main_agent.close()


if __name__ == "__main__":
    asyncio.run(main())
