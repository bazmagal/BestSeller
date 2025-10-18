#!/usr/bin/env python3
"""
Main agent that uses the plot generator MCP server.

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

    # Check if API key is set (or it will be loaded from config)
    # if not os.environ.get("ANTHROPIC_API_KEY"):
    #     print("Error: ANTHROPIC_API_KEY environment variable not set")
    #     print("Set it with: export ANTHROPIC_API_KEY='your-api-key-here'")
    #     sys.exit(1)

    # Get the themes from command line arguments
    themes = " ".join(sys.argv[1:])

    print(f"Input themes: {themes}\n")
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

        # Create the main agent with access to the plot generator server
        main_agent = Agent(
            name="main_agent",
            instruction="""You are a creative writing assistant. When asked to generate a plot, use the generate_plot tool and return ONLY the plot text itself, with no additional commentary, analysis, or explanation.""",
            server_names=["plot-generator"],
            context=context
        )

        # Initialize the agent
        await main_agent.initialize()

        try:
            # Attach LLM to the main agent
            llm = await main_agent.attach_llm(AnthropicAugmentedLLM)

            # Use the LLM to call the tool and get the plot
            query = f'Use the generate_plot tool with themes: {themes}. Return only the plot text, nothing else.'

            # Get the response - this will include tool calls
            response = await llm.generate(query)

            # The response is a list of messages - get the final text response
            # Look through the last message for text content
            plot = None
            if isinstance(response, list):
                # Get the last message
                for msg in reversed(response):
                    if hasattr(msg, 'content'):
                        for block in msg.content:
                            if hasattr(block, 'text') and block.text:
                                plot = block.text
                                break
                    if plot:
                        break

            if not plot:
                plot = "Error: Could not extract plot from response"

            # Print just the plot
            print("\n" + "="*60)
            print("GENERATED PLOT:")
            print("="*60)
            print(plot)
            print("="*60 + "\n")

        finally:
            # Clean up
            await main_agent.close()


if __name__ == "__main__":
    asyncio.run(main())
