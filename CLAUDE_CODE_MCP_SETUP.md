# Setting Up Gmail MCP Server in Claude Code

## Option 1: Configure via Claude Code Settings (Recommended)

1. Open Claude Code settings (Cmd+,)
2. Search for "MCP" or "Model Context Protocol"
3. Add the Gmail MCP server configuration:

```json
{
  "gmail": {
    "command": "python3",
    "args": ["/Users/paulbrown/Desktop/coding-projects/claude-gmail-manager/gmail_mcp.py"],
    "env": {
      "GMAIL_TOKEN_PATH": "/Users/paulbrown/Desktop/coding-projects/claude-gmail-manager/gmail_token.pickle"
    }
  }
}
```

## Option 2: Direct Configuration File

If Claude Code uses a configuration file (similar to Claude Desktop), it may be located at:
- `~/.config/claude-code/mcp_settings.json` (Linux)
- `~/Library/Application Support/Claude Code/mcp_settings.json` (macOS)
- `%APPDATA%\Claude Code\mcp_settings.json` (Windows)

Add the same JSON configuration to that file.

## Verify Setup

After configuration:
1. Restart Claude Code
2. In the terminal, type `/clean10` to test
3. The command should have access to gmail MCP tools

## Troubleshooting

If the MCP server isn't available:
- Ensure `gmail_token.pickle` exists in the project directory
- Check that Python 3 is in your PATH
- Verify the absolute paths in the configuration are correct
- Check Claude Code logs for MCP connection errors

## Required for Commands

The following slash commands require the Gmail MCP server:
- `/clean10` - Interactive cleaning with approval
- `/clean25` - Semi-automated cleaning
- `/clean50` - Automated cleaning (50 emails)
- `/clean100` - Automated cleaning (100 emails)
