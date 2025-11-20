# Gmail MCP Server

A Model Context Protocol (MCP) server that provides comprehensive Gmail functionality for AI agents.

## Features

This MCP server enables AI agents to interact with Gmail through a well-designed set of tools:

- **Email Search**: Search emails using Gmail's powerful query syntax
- **Email Reading**: Retrieve full email details including headers and body
- **Email Sending**: Send new emails with support for CC, BCC, HTML content
- **Email Replies**: Reply to existing email threads
- **Label Management**: List, create, and modify email labels
- **Email Organization**: Archive and delete emails in batches
- **Flexible Formatting**: Output results in markdown or JSON format

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt --break-system-packages
   ```

2. **Ensure you have a valid Gmail token**:
   Place your `gmail_token.pickle` file at `/mnt/user-data/uploads/gmail_token.pickle`

   The token file should contain OAuth2 credentials with the following Gmail API scopes:
   - `https://www.googleapis.com/auth/gmail.readonly` (for reading emails)
   - `https://www.googleapis.com/auth/gmail.send` (for sending emails)
   - `https://www.googleapis.com/auth/gmail.modify` (for modifying labels, archiving)
   - `https://www.googleapis.com/auth/gmail.labels` (for label management)

## Usage

### Running the Server

**Local/stdio mode** (default):
```bash
python gmail_mcp.py
```

**Remote/HTTP mode**:
```bash
python gmail_mcp.py --transport streamable_http --port 8000
```

### Connecting to Claude Desktop

Add this to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "gmail": {
      "command": "python",
      "args": ["/path/to/gmail_mcp.py"]
    }
  }
}
```

## Available Tools

### 1. gmail_search_emails

Search for Gmail messages using standard Gmail search syntax.

**Parameters**:
- `query` (required): Gmail search query (e.g., "from:john@example.com subject:invoice is:unread")
- `max_results` (optional): Maximum number of results (1-100, default: 20)
- `include_body` (optional): Include full message body (default: false)
- `response_format` (optional): "markdown" or "json" (default: "markdown")

**Example**:
```json
{
  "query": "is:unread after:2024/01/01",
  "max_results": 10,
  "include_body": false,
  "response_format": "markdown"
}
```

**Gmail Search Operators**:
- `from:sender@example.com` - From specific sender
- `to:recipient@example.com` - To specific recipient
- `subject:keyword` - Subject contains keyword
- `is:unread` / `is:read` - Read status
- `in:inbox` / `in:sent` - Location
- `after:YYYY/MM/DD` / `before:YYYY/MM/DD` - Date range
- `has:attachment` - Has attachments
- `label:labelname` - Has specific label

### 2. gmail_get_email

Retrieve complete details of a specific email message.

**Parameters**:
- `message_id` (required): The Gmail message ID
- `response_format` (optional): "markdown" or "json" (default: "markdown")

**Example**:
```json
{
  "message_id": "18c5a1b2f3d4e5f6",
  "response_format": "markdown"
}
```

### 3. gmail_send_email

Send a new email message.

**Parameters**:
- `to` (required): List of recipient email addresses
- `subject` (required): Email subject line
- `body` (required): Email body content
- `cc` (optional): List of CC recipients
- `bcc` (optional): List of BCC recipients
- `reply_to` (optional): Custom reply-to address
- `is_html` (optional): Whether body is HTML (default: false)

**Example**:
```json
{
  "to": ["recipient@example.com"],
  "subject": "Meeting Follow-up",
  "body": "Hi,\n\nThank you for meeting with me today...",
  "cc": ["team@example.com"],
  "is_html": false
}
```

### 4. gmail_reply_to_email

Reply to an existing email thread.

**Parameters**:
- `thread_id` (required): The Gmail thread ID to reply to
- `body` (required): Reply body content
- `reply_all` (optional): Reply to all recipients (default: false)
- `is_html` (optional): Whether body is HTML (default: false)

**Example**:
```json
{
  "thread_id": "18c5a1b2f3d4e5f6",
  "body": "Thank you for your email. I'll review and get back to you.",
  "reply_all": false
}
```

### 5. gmail_modify_labels

Add or remove labels from messages.

**Parameters**:
- `message_ids` (required): List of message IDs to modify
- `add_labels` (optional): List of label names or IDs to add
- `remove_labels` (optional): List of label names or IDs to remove

**Example**:
```json
{
  "message_ids": ["18c5a1b2f3d4e5f6", "18c5a1b2f3d4e5f7"],
  "add_labels": ["Important", "Follow-up"],
  "remove_labels": ["UNREAD"]
}
```

### 6. gmail_archive_emails

Archive messages by removing them from inbox.

**Parameters**:
- `message_ids` (required): List of message IDs to archive

**Example**:
```json
{
  "message_ids": ["18c5a1b2f3d4e5f6", "18c5a1b2f3d4e5f7"]
}
```

### 7. gmail_delete_emails

Move messages to trash (auto-deleted after 30 days).

**Parameters**:
- `message_ids` (required): List of message IDs to delete

**Example**:
```json
{
  "message_ids": ["18c5a1b2f3d4e5f6"]
}
```

### 8. gmail_list_labels

List all Gmail labels (system and user-created).

**Parameters**:
- `response_format` (optional): "markdown" or "json" (default: "markdown")

**Example**:
```json
{
  "response_format": "json"
}
```

### 9. gmail_create_label

Create a new Gmail label.

**Parameters**:
- `name` (required): Name for the new label
- `label_list_visibility` (optional): "labelShow", "labelShowIfUnread", or "labelHide" (default: "labelShow")
- `message_list_visibility` (optional): "show" or "hide" (default: "show")

**Example**:
```json
{
  "name": "Important Projects",
  "label_list_visibility": "labelShow",
  "message_list_visibility": "show"
}
```

## Integration with Gmail Manager Skill

This MCP server is designed to work seamlessly with the `gmail-manager` skill. The gmail-manager skill can use these tools to:

1. **Clean inbox**: Search and archive/delete unimportant emails in batches
2. **Identify important emails**: Find and summarize emails needing attention
3. **Draft and send responses**: Write and send emails matching user's style
4. **Manage labels**: Organize emails with custom labels
5. **Learn patterns**: Build knowledge about email importance over time

## Error Handling

The server provides clear, actionable error messages:

- **404 errors**: "Resource not found. Please check the ID is correct."
- **403 errors**: "Permission denied. Check your Gmail API permissions."
- **429 errors**: "Rate limit exceeded. Please wait before making more requests."
- **400 errors**: "Invalid request. Check your parameters."

## Security Notes

- The token file contains sensitive OAuth2 credentials - keep it secure
- The server uses read-only hints for search/read operations
- Destructive operations (delete) are marked with destructiveHint
- All network operations are asynchronous for better performance

## Troubleshooting

### Token expired or invalid
If you get authentication errors, your token may have expired. Generate a new `gmail_token.pickle` file with the required OAuth2 scopes.

### Missing permissions
Ensure your OAuth2 credentials have all required Gmail API scopes:
- gmail.readonly
- gmail.send
- gmail.modify
- gmail.labels

### Rate limiting
Gmail API has rate limits. If you hit them, the server will return a clear error message. Wait a few minutes before retrying.

## Development

### Code Structure

- **Authentication**: `get_gmail_service()` manages OAuth2 credentials
- **Error Handling**: `_handle_api_error()` provides user-friendly error messages
- **Helpers**: Utility functions for decoding messages, formatting timestamps, etc.
- **Tools**: Each Gmail operation is implemented as a separate MCP tool
- **Input Validation**: Pydantic models ensure type safety and validation

### Testing

Test the server with MCP Inspector:

```bash
npx @modelcontextprotocol/inspector python gmail_mcp.py
```

## License

This MCP server follows MCP best practices and is designed to integrate with Claude and other MCP-compatible AI systems.
