#!/usr/bin/env python3
"""
Main agent that orchestrates story generation using plot generator and chapter writer MCP servers.

This agent will:
1. Generate an overall plot based on themes
2. Create outlines for 5 chapters
3. Generate each chapter and save to files

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
    print(f"Themes: {themes}\n")

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
            name="main_agent",
            instruction="""You are a story orchestrator. Your job is to:
1. Generate an overall plot using the generate_plot tool
2. Create a 5-chapter outline based on that plot
3. Write each chapter using the write_chapter tool
Return only essential information, no extra commentary.""",
            server_names=["plot-generator", "chapter-writer"],
            context=context
        )

        # Initialize the agent
        await main_agent.initialize()

        try:
            # Attach LLM to the main agent
            llm = await main_agent.attach_llm(AnthropicAugmentedLLM)

            # STEP 1: Generate the overall plot
            print("📖 Step 1: Generating overall plot...\n")

            plot_query = f'Use the generate_plot tool with themes: {themes}. Return only the plot text.'
            plot_response = await llm.generate(plot_query)

            # Extract plot from response
            plot = None
            if isinstance(plot_response, list):
                for msg in reversed(plot_response):
                    if hasattr(msg, 'content'):
                        for block in msg.content:
                            if hasattr(block, 'text') and block.text:
                                plot = block.text
                                break
                    if plot:
                        break

            if not plot:
                plot = "Error: Could not generate plot"
                print(plot)
                return

            print("="*60)
            print("OVERALL PLOT:")
            print("="*60)
            print(plot)
            print("="*60 + "\n")

            # STEP 2: Create chapter outlines
            print("📝 Step 2: Creating chapter outlines...\n")

            outline_query = f"""Based on this plot, create a brief outline for 5 chapters.
For each chapter, provide a 1-2 sentence description of what happens.
Format as:
Chapter 1: [description]
Chapter 2: [description]
Chapter 3: [description]
Chapter 4: [description]
Chapter 5: [description]

Plot:
{plot}"""

            outline_response = await llm.generate(outline_query)

            # Extract outlines
            chapter_outlines = None
            if isinstance(outline_response, list):
                for msg in reversed(outline_response):
                    if hasattr(msg, 'content'):
                        for block in msg.content:
                            if hasattr(block, 'text') and block.text:
                                chapter_outlines = block.text
                                break
                    if chapter_outlines:
                        break

            print(chapter_outlines)
            print("\n")

            # STEP 3: Generate each chapter
            print("✍️  Step 3: Writing chapters...\n")

            # Parse chapter outlines (simple approach)
            chapter_descriptions = []
            for line in chapter_outlines.split('\n'):
                if line.strip().startswith('Chapter'):
                    # Extract description after the colon
                    parts = line.split(':', 1)
                    if len(parts) > 1:
                        chapter_descriptions.append(parts[1].strip())

            # Write each chapter
            previous_summary = ""
            for i in range(5):
                chapter_num = i + 1
                chapter_outline = chapter_descriptions[i] if i < len(chapter_descriptions) else f"Chapter {chapter_num}"

                print(f"  Writing Chapter {chapter_num}...")

                write_query = f"""Use the write_chapter tool to write chapter {chapter_num}.

Arguments:
- chapter_number: {chapter_num}
- overall_plot: {plot}
- chapter_outline: {chapter_outline}
- previous_chapters_summary: {previous_summary if previous_summary else "This is the first chapter"}

Just call the tool and report the filename."""

                chapter_response = await llm.generate(write_query)

                # Extract result
                result = None
                if isinstance(chapter_response, list):
                    for msg in reversed(chapter_response):
                        if hasattr(msg, 'content'):
                            for block in msg.content:
                                if hasattr(block, 'text') and block.text:
                                    result = block.text
                                    break
                        if result:
                            break

                print(f"  ✓ {result}")

                # Update summary for next chapter
                previous_summary += f"\nChapter {chapter_num}: {chapter_outline}"

            print("\n" + "="*60)
            print("✅ STORY GENERATION COMPLETE!")
            print("="*60)
            print("All chapters have been written to the 'chapters/' directory.")
            print("="*60 + "\n")

        finally:
            # Clean up
            await main_agent.close()


if __name__ == "__main__":
    asyncio.run(main())
