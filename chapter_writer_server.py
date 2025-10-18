#!/usr/bin/env python3
"""
MCP Server that writes story chapters to files.

This server exposes a tool that generates chapter content and saves it to a file.
"""

import asyncio
import sys
import os
from mcp.server import Server
from mcp.types import Tool, TextContent
from anthropic import Anthropic


# Create the MCP server
app = Server("chapter-writer")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="write_chapter",
            description="Generates a story chapter based on the plot and chapter outline, then writes it to a file. Returns the filename where the chapter was saved.",
            inputSchema={
                "type": "object",
                "properties": {
                    "chapter_number": {
                        "type": "integer",
                        "description": "The chapter number (e.g., 1, 2, 3)"
                    },
                    "overall_plot": {
                        "type": "string",
                        "description": "The overall plot/summary of the entire story"
                    },
                    "chapter_outline": {
                        "type": "string",
                        "description": "Brief outline or description of what should happen in this chapter"
                    },
                    "previous_chapters_summary": {
                        "type": "string",
                        "description": "Summary of what happened in previous chapters (empty for chapter 1)"
                    }
                },
                "required": ["chapter_number", "overall_plot", "chapter_outline"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "write_chapter":
            chapter_number = arguments.get("chapter_number", 1)
            overall_plot = arguments.get("overall_plot", "")
            chapter_outline = arguments.get("chapter_outline", "")
            previous_chapters = arguments.get("previous_chapters_summary", "")

            # Log to stderr to avoid breaking MCP protocol
            print(f"[Chapter Writer] Writing chapter {chapter_number}", file=sys.stderr)

            # Check if API key is set
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                print(f"[Chapter Writer] WARNING: No API key found!", file=sys.stderr)
                return [TextContent(
                    type="text",
                    text="Error: ANTHROPIC_API_KEY not set"
                )]

            # Use Claude to generate the chapter
            client = Anthropic(api_key=api_key)

            prompt = f"""You are writing Chapter {chapter_number} of a short story.

OVERALL PLOT:
{overall_plot}

PREVIOUS CHAPTERS SUMMARY:
{previous_chapters if previous_chapters else "This is the first chapter."}

CHAPTER {chapter_number} OUTLINE:
{chapter_outline}

Write a compelling, detailed chapter (approximately 500-800 words) that:
- Follows the overall plot and chapter outline
- Maintains continuity with previous chapters
- Includes vivid descriptions, dialogue, and character development
- Ends with a hook or transition to the next chapter (unless it's the final chapter)

Write the chapter now:"""

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            chapter_content = message.content[0].text.strip()

            # Create chapters directory if it doesn't exist
            chapters_dir = "chapters"
            os.makedirs(chapters_dir, exist_ok=True)

            # Write chapter to file
            filename = f"{chapters_dir}/chapter_{chapter_number}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"CHAPTER {chapter_number}\n")
                f.write("=" * 60 + "\n\n")
                f.write(chapter_content)
                f.write("\n")

            word_count = len(chapter_content.split())
            print(f"[Chapter Writer] Chapter {chapter_number} written to {filename} ({word_count} words)", file=sys.stderr)

            return [TextContent(
                type="text",
                text=f"Chapter {chapter_number} successfully written to {filename} ({word_count} words)"
            )]

        raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        print(f"[Chapter Writer] ERROR: {e}", file=sys.stderr)
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
