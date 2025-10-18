#!/usr/bin/env python3
"""
MCP Server that provides continent identification services.

This server exposes a tool that can identify which continent is mentioned in text.
"""

import asyncio
import sys
from mcp.server import Server
from mcp.types import Tool, TextContent
from anthropic import Anthropic
import os


# Create the MCP server
app = Server("continent-helper")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="identify_continent",
            description="Identifies which continent is mentioned in the given text. Returns the continent name(s).",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to analyze for continent identification"
                    }
                },
                "required": ["text"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "identify_continent":
            text = arguments.get("text", "")

            # Log to stderr to avoid breaking MCP protocol
            print(f"[Continent Helper] Received request for text: {text}", file=sys.stderr)

            # Debug: Check if API key is set
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if api_key:
                print(f"[Continent Helper] API key found: {api_key[:10]}...", file=sys.stderr)
            else:
                print(f"[Continent Helper] WARNING: No API key found in environment!", file=sys.stderr)
                print(f"[Continent Helper] Environment vars: {list(os.environ.keys())}", file=sys.stderr)

            # Use Claude to identify the continent
            client = Anthropic(api_key=api_key)

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=50,
                messages=[{
                    "role": "user",
                    "content": f"""Analyze this text and identify the continent mentioned. Respond with ONLY the continent name: Europe, Asia, Africa, North America, South America, Australia, or Antarctica.

Text: {text}

Continent:"""
                }]
            )

            continent = message.content[0].text.strip()

            # Log to stderr to avoid breaking MCP protocol
            print(f"[Continent Helper] Identified: {continent}", file=sys.stderr)

            return [TextContent(
                type="text",
                text=continent
            )]

        raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        print(f"[Continent Helper] ERROR: {e}", file=sys.stderr)
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
