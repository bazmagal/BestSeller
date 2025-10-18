#!/usr/bin/env python3
"""
MCP Server that provides plot generation services for short stories.

This server exposes a tool that generates creative 200-word plots based on provided themes.
"""

import asyncio
import sys
from mcp.server import Server
from mcp.types import Tool, TextContent
from anthropic import Anthropic
import os


# Create the MCP server
app = Server("plot-generator")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="generate_plot",
            description="Generates a creative 200-word plot for a short story based on provided themes. The plot will include a beginning, middle, and end with compelling characters and conflict.",
            inputSchema={
                "type": "object",
                "properties": {
                    "themes": {
                        "type": "string",
                        "description": "Free-form text describing the themes, genres, or elements to include in the plot (e.g., 'mystery, haunted lighthouse, unreliable narrator')"
                    }
                },
                "required": ["themes"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "generate_plot":
            themes = arguments.get("themes", "")

            # Log to stderr to avoid breaking MCP protocol
            print(f"[Plot Generator] Received request for themes: {themes}", file=sys.stderr)

            # Debug: Check if API key is set
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if api_key:
                print(f"[Plot Generator] API key found: {api_key[:10]}...", file=sys.stderr)
            else:
                print(f"[Plot Generator] WARNING: No API key found in environment!", file=sys.stderr)
                print(f"[Plot Generator] Environment vars: {list(os.environ.keys())}", file=sys.stderr)

            # Use Claude to generate the plot
            client = Anthropic(api_key=api_key)

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=400,
                messages=[{
                    "role": "user",
                    "content": f"""Generate a compelling 100-word plot for a short story based on these themes and elements: {themes}

The plot should include:
- An intriguing beginning that sets up the world and characters
- A middle section with rising tension and conflict
- A satisfying conclusion or cliffhanger

Make it creative, engaging, and suitable for a short story format. Aim for exactly 200 words.

Plot:"""
                }]
            )

            plot = message.content[0].text.strip()

            # Log to stderr to avoid breaking MCP protocol
            print(f"[Plot Generator] Generated plot ({len(plot.split())} words)", file=sys.stderr)
            print(plot)
            return [TextContent(
                type="text",
                text=plot
            )]

        raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        print(f"[Plot Generator] ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


async def main():
    """Run the MCP server."""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
