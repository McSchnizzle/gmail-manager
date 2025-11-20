# Setting Up Gmail MCP Server in Claude Code

## Quick Setup

1. **Copy the example configuration**:
   ```bash
   cp .mcp.json.example .mcp.json
   ```

2. **Edit `.mcp.json`** with your absolute paths:
   ```json
   {
     "mcpServers": {
       "gmail": {
         "command": "python3",
         "args": [
           "/absolute/path/to/gmail_mcp.py"
         ],
         "env": {
           "GMAIL_TOKEN_PATH": "/absolute/path/to/gmail_token.pickle"
         }
       }
     }
   }
   ```

3. **Update the paths** to match your system:
   - Replace `/absolute/path/to/gmail_mcp.py` with the full path to this project's `gmail_mcp.py`
   - Replace `/absolute/path/to/gmail_token.pickle` with the full path to your token file

4. **Restart Claude Code** completely

## Configuration Details

The `.mcp.json` file at your project root configures MCP servers for Claude Code:
- **Local scope**: Project-specific configuration
- **Loaded on startup**: Changes require restart
- **Not in git**: `.mcp.json` is gitignored (contains local paths)

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
