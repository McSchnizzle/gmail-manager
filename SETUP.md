# Gmail MCP Server Setup Guide

## Quick Start

### 1. Install Dependencies

In your terminal, navigate to the `claude-gmail-manager` directory and run:

```bash
cd ~/Desktop/coding-projects/claude-gmail-manager
pip3 install -r requirements.txt
```

Or if you want to install them with Python 3.12 specifically:

```bash
python3.12 -m pip install -r requirements.txt
```

### 2. Set Up Gmail Token

You need a `gmail_token.pickle` file in the same directory as `gmail_mcp.py`. This file should already exist if you've authenticated with Gmail before. If not, you'll need to:

1. Create a Google Cloud Project
2. Enable the Gmail API
3. Download OAuth credentials
4. Run the authentication flow to generate the token file

### 3. Configure Claude Desktop

Edit your Claude Desktop configuration file:

**Location:** `~/Library/Application Support/Claude/claude_desktop_config.json`

Add this to your configuration:

```json
{
  "mcpServers": {
    "gmail": {
      "command": "python3.12",
      "args": [
        "/Users/paulbrown/Desktop/coding-projects/claude-gmail-manager/gmail_mcp.py"
      ]
    }
  }
}
```

**Note:** Make sure to use the full absolute path to your `gmail_mcp.py` file!

### 4. Restart Claude Desktop

After updating the config file, completely quit and restart the Claude Desktop app.

### 5. Test the Connection

Once Claude Desktop restarts, you should see the Gmail tools available. Try asking Claude:

```
Search my Gmail for unread messages from the last week
```

## Troubleshooting

### "No module named 'mcp'" Error
Run: `pip3 install -r requirements.txt` or `python3.12 -m pip install -r requirements.txt`

### Token File Not Found
Make sure `gmail_token.pickle` is in the same directory as `gmail_mcp.py`

### Claude Desktop Not Seeing the Server
1. Check that the path in `claude_desktop_config.json` is correct (use full path)
2. Make sure you completely quit and restarted Claude Desktop (not just closed the window)
3. Check the Claude Desktop logs for errors

### Permission Errors
The Gmail token needs proper OAuth scopes. If you get permission errors, you may need to re-authenticate with broader scopes.

## What Changed

The fixed `gmail_mcp.py` file now:
- Uses a relative path for the token file (looks for `gmail_token.pickle` in the same directory)
- This makes it work correctly when called from Claude Desktop

## Files Included

- `gmail_mcp.py` - The fixed MCP server script
- `requirements.txt` - All Python dependencies
- `SETUP.md` - This setup guide
