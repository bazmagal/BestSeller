# MCP Multi-Agent System - Plot Generator

A multi-agent system built with the Model Context Protocol (MCP) where a main agent delegates creative plot generation tasks to a specialized MCP server.

## Architecture

- **main_agent.py** - Main agent that orchestrates queries and uses MCP servers
- **plot_generator_server.py** - MCP server that generates creative 200-word plots for short stories
- **mcp_agent.config.yaml** - Configuration file (not in git, contains secrets)

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

### 3. Update Path in Config

In `mcp_agent.config.yaml`, update the path to `plot_generator_server.py` to match your local path.

## Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Set your API key in environment
export ANTHROPIC_API_KEY='your-api-key-here'

# Run the main agent with your themes
python main_agent.py "mystery, haunted lighthouse, unreliable narrator"
```

## Examples

```bash
python main_agent.py "mystery, haunted lighthouse, unreliable narrator"
# Generates a 200-word mystery plot

python main_agent.py "science fiction, time travel, dystopian future"
# Generates a 200-word sci-fi plot

python main_agent.py "romance, second chances, small town"
# Generates a 200-word romance plot

python main_agent.py "horror, ancient curse, archaeological dig"
# Generates a 200-word horror plot
```

## How It Works

1. **Main Agent** receives theme input from command line
2. **Main Agent** uses mcp-agent framework with `AnthropicAugmentedLLM`
3. **Main Agent** calls the `generate_plot` tool from the plot generator MCP server
4. **Plot Generator Server** creates a compelling 200-word plot using Claude
5. **Plot Generator Server** returns the generated plot via MCP protocol
6. **Main Agent** logs the result

## Files

- `main_agent.py` - Main agent implementation
- `plot_generator_server.py` - MCP server for plot generation
- `mcp_agent.config.yaml` - Configuration (gitignored, contains secrets)
- `mcp_agent.config.yaml.example` - Example configuration template
- `simple_agent.py` - Simple single-agent example (no MCP)
- `mcp_agent_example.py` - Basic mcp-agent example
- `test.py` - Hello world test file

## Security Notes

⚠️ **IMPORTANT**: Never commit `mcp_agent.config.yaml` to git as it contains your API key!

The `.gitignore` file is configured to exclude:
- `mcp_agent.config.yaml`
- `venv/`
- `*.key` files
- `.env` files
