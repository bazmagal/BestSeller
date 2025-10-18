# MCP Multi-Agent System

A multi-agent system built with the Model Context Protocol (MCP) where a main agent delegates continent identification tasks to a specialized MCP server.

## Architecture

- **main_agent.py** - Main agent that orchestrates queries and uses MCP servers
- **continent_helper_server.py** - MCP server that provides continent identification
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

In `mcp_agent.config.yaml`, update the path to `continent_helper_server.py` to match your local path.

## Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Set your API key in environment
export ANTHROPIC_API_KEY='your-api-key-here'

# Run the main agent
python main_agent.py "Tokyo is the capital of Japan"
```

## Examples

```bash
python main_agent.py "Paris is a beautiful city in France"
# Expected: Europe

python main_agent.py "The pyramids are in Egypt"
# Expected: Africa

python main_agent.py "Tokyo is the capital of Japan"
# Expected: Asia
```

## How It Works

1. **Main Agent** receives text input from command line
2. **Main Agent** uses mcp-agent framework with `AnthropicAugmentedLLM`
3. **Main Agent** calls the `identify_continent` tool from the continent helper MCP server
4. **Continent Helper Server** analyzes the text using Claude
5. **Continent Helper Server** returns the continent name via MCP protocol
6. **Main Agent** logs the result

## Files

- `main_agent.py` - Main agent implementation
- `continent_helper_server.py` - MCP server for continent identification
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
