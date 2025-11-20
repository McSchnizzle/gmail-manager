# Gmail MCP Server - Quick Start Guide

## What You've Built

A complete Model Context Protocol (MCP) server that connects Gmail to your gmail-manager skill, eliminating the need for Zapier MCP. The server provides 9 comprehensive tools for email management:

✓ **gmail_search_emails** - Search with Gmail query syntax
✓ **gmail_get_email** - Retrieve full email details  
✓ **gmail_send_email** - Send new emails
✓ **gmail_reply_to_email** - Reply to threads
✓ **gmail_modify_labels** - Add/remove labels
✓ **gmail_archive_emails** - Archive messages
✓ **gmail_delete_emails** - Move to trash
✓ **gmail_list_labels** - List all labels
✓ **gmail_create_label** - Create new labels

## Setup Instructions

### 1. Install the Server

Place these files somewhere permanent on your system (e.g., `~/mcp-servers/gmail/`):
- `gmail_mcp.py` - The MCP server
- `requirements.txt` - Python dependencies  
- `gmail_token.pickle` - Your Gmail authentication token

Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configure Claude Desktop

Edit your Claude Desktop MCP settings file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration:

```json
{
  "mcpServers": {
    "gmail": {
      "command": "python",
      "args": ["/absolute/path/to/gmail_mcp.py"],
      "env": {
        "GMAIL_TOKEN_PATH": "/absolute/path/to/gmail_token.pickle"
      }
    }
  }
}
```

**Important**: Replace `/absolute/path/to/` with the actual paths where you saved the files.

### 3. Update the Server (Optional)

If you want to specify a custom token path, update line 31 in `gmail_mcp.py`:

```python
TOKEN_PATH = "/your/custom/path/gmail_token.pickle"
```

Or set it via environment variable in the config above.

### 4. Restart Claude Desktop

After updating the config file, quit and restart Claude Desktop completely.

### 5. Verify It's Working

In a new conversation with Claude, try:

```
Can you search my Gmail for unread messages from the last week?
```

Claude should now be able to use the gmail_search_emails tool directly!

## Using with Gmail Manager Skill

The gmail-manager skill will automatically use these MCP tools instead of Zapier. Try commands like:

- "Clean 10 emails from my inbox"
- "Tell me 5 important things in my inbox"  
- "Identify an email that needs a response"
- "Archive all emails from [sender]"
- "Create a label called 'Important Projects'"

The skill will use your MCP server for all Gmail operations.

## Token Requirements

Your `gmail_token.pickle` must have these Gmail API scopes:
- `https://www.googleapis.com/auth/gmail.readonly`
- `https://www.googleapis.com/auth/gmail.send`
- `https://www.googleapis.com/auth/gmail.modify`
- `https://www.googleapis.com/auth/gmail.labels`

If you get authentication errors, you may need to regenerate the token with the correct scopes.

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "Token not found" errors
- Verify the token path in the config matches where you saved gmail_token.pickle
- Make sure the path is absolute (starts with `/` on macOS/Linux or `C:\` on Windows)

### "Permission denied" errors
- Check that your token has all required Gmail API scopes
- You may need to re-authorize the application

### MCP server not appearing in Claude
- Make sure the config file is valid JSON (use a JSON validator)
- Verify paths are absolute, not relative
- Restart Claude Desktop completely (quit and reopen)
- Check the Claude logs for error messages

## Testing the Server Directly

You can test the server using the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector python gmail_mcp.py
```

This will open a web interface where you can test each tool manually.

## What's Next?

With your Gmail MCP server running, you can:

1. **Use gmail-manager skill** - All gmail-manager commands now work without Zapier
2. **Build custom workflows** - Create your own skills that use these Gmail tools
3. **Extend the server** - Add more Gmail operations if needed
4. **Share it** - This server can be used by others with their own tokens

## Key Features

- **No rate limits** (beyond Gmail API limits) - Unlike Zapier
- **Full Gmail search syntax** - All standard operators supported
- **Batch operations** - Archive/delete multiple emails at once
- **Rich formatting** - Markdown and JSON output options
- **Production ready** - Error handling, type validation, async operations

Enjoy your direct Gmail integration with Claude!
