# BestSeller - MCP Multi-Agent Story Generator

A multi-agent system built with the Model Context Protocol (MCP) that generates complete 5-chapter stories. The main agent orchestrates two specialized MCP servers to create cohesive short stories from simple themes.

## Architecture

- **main_agent.py** - Main orchestrator that coordinates story generation
- **plot_generator_server.py** - MCP server that generates 200-word story plots
- **chapter_writer_server.py** - MCP server that writes chapters and saves them to files
- **mcp_agent.config.yaml** - Configuration file (not in git, contains secrets)

## How It Works

1. **Plot Generation**: Main agent uses plot-generator to create an overall story plot from themes
2. **Chapter Planning**: Creates outlines for 5 chapters based on the plot
3. **Chapter Writing**: Uses chapter-writer to generate each chapter (500-800 words) and save to files
4. **Output**: All chapters are saved in the `chapters/` directory

## Setup

### 1. Install Dependencies

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install mcp-agent anthropic
```

### 2. Configure API Key

Copy the example config:
```bash
cp mcp_agent.config.yaml.example mcp_agent.config.yaml
```

Edit `mcp_agent.config.yaml` and replace `YOUR_API_KEY_HERE` with your Anthropic API key.

You can get an API key from: https://console.anthropic.com/

### 3. Update Paths in Config

In `mcp_agent.config.yaml`, update the paths to match your local directory:
- `plot_generator_server.py`
- `chapter_writer_server.py`

## Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Set your API key in environment
export ANTHROPIC_API_KEY='your-api-key-here'

# Generate a complete 5-chapter story
python main_agent.py "mystery, haunted lighthouse, unreliable narrator"
```

## Examples

```bash
# Mystery story
python main_agent.py "mystery, haunted lighthouse, unreliable narrator"

# Science fiction story
python main_agent.py "science fiction, time travel, dystopian future"

# Romance story
python main_agent.py "romance, second chances, small town"

# Horror story
python main_agent.py "horror, ancient curse, archaeological dig"

# Fantasy story
python main_agent.py "fantasy, magic academy, prophecy, betrayal"
```

## Output

After running, you'll find:
- `chapters/chapter_1.txt`
- `chapters/chapter_2.txt`
- `chapters/chapter_3.txt`
- `chapters/chapter_4.txt`
- `chapters/chapter_5.txt`

Each chapter is approximately 500-800 words with full narrative detail.

## Workflow

1. **Plot Generation** - Main agent calls plot-generator to create a cohesive 200-word plot
2. **Chapter Planning** - Main agent creates outlines for 5 chapters
3. **Chapter Writing** - For each chapter:
   - Main agent calls chapter-writer with plot, outline, and previous chapter summaries
   - Chapter-writer generates detailed content using Claude
   - Chapter is saved to `chapters/chapter_N.txt`
4. **Completion** - All 5 chapters are written and saved

## Files

- `main_agent.py` - Main orchestrator agent
- `plot_generator_server.py` - MCP server for plot generation
- `chapter_writer_server.py` - MCP server for chapter writing
- `mcp_agent.config.yaml` - Configuration (gitignored, contains secrets)
- `mcp_agent.config.yaml.example` - Example configuration template
- `chapters/` - Directory where generated chapters are saved

## Security Notes

⚠️ **IMPORTANT**: Never commit `mcp_agent.config.yaml` to git as it contains your API key!

The `.gitignore` file is configured to exclude:
- `mcp_agent.config.yaml`
- `venv/`
- `*.key` files
- `.env` files
