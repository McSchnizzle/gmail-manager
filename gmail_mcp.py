#!/usr/bin/env python3
"""
Gmail MCP Server - Model Context Protocol server for Gmail operations.

This server provides comprehensive Gmail functionality including:
- Email search and reading
- Sending and replying to emails
- Label management
- Archive and delete operations
- Email organization tools

Authentication uses the Gmail API with a token.pickle file.
"""

import pickle
import os
import json
import base64
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict

# Google API imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Initialize FastMCP server
mcp = FastMCP("gmail_mcp")

# Global Gmail API service
_gmail_service = None
TOKEN_PATH = os.path.join(os.path.dirname(__file__), "gmail_token.pickle")


def get_gmail_service():
    """Get or create Gmail API service instance."""
    global _gmail_service
    
    if _gmail_service is not None:
        return _gmail_service
    
    # Load credentials from pickle file
    if not os.path.exists(TOKEN_PATH):
        raise FileNotFoundError(
            f"Gmail token not found at {TOKEN_PATH}. "
            "Please provide a valid gmail_token.pickle file."
        )
    
    with open(TOKEN_PATH, 'rb') as token:
        creds = pickle.load(token)
    
    # Refresh token if expired
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Save refreshed credentials
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
    
    _gmail_service = build('gmail', 'v1', credentials=creds)
    return _gmail_service


def _handle_api_error(e: Exception) -> str:
    """Convert API errors to user-friendly messages."""
    if isinstance(e, HttpError):
        status = e.resp.status
        if status == 404:
            return "Error: Resource not found. Please check the ID is correct."
        elif status == 403:
            return "Error: Permission denied. Check your Gmail API permissions."
        elif status == 429:
            return "Error: Rate limit exceeded. Please wait before making more requests."
        elif status == 400:
            return f"Error: Invalid request. {e.error_details if hasattr(e, 'error_details') else 'Check your parameters.'}"
        return f"Error: Gmail API error (status {status})"
    elif isinstance(e, FileNotFoundError):
        return str(e)
    return f"Error: {type(e).__name__}: {str(e)}"


def _format_timestamp(timestamp: str) -> str:
    """Convert Gmail internal date to human-readable format."""
    try:
        dt = datetime.fromtimestamp(int(timestamp) / 1000)
        return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    except:
        return timestamp


def _decode_message_body(payload: Dict[str, Any]) -> str:
    """Decode message body from Gmail API payload."""
    body = ""
    
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                if 'data' in part['body']:
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    break
            elif part['mimeType'] == 'text/html' and not body:
                if 'data' in part['body']:
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
    elif 'body' in payload and 'data' in payload['body']:
        body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
    
    return body


def _get_header_value(headers: List[Dict[str, str]], name: str) -> str:
    """Extract header value from Gmail message headers."""
    for header in headers:
        if header['name'].lower() == name.lower():
            return header['value']
    return ""


# ==================== PYDANTIC MODELS ====================

class ResponseFormat(str, Enum):
    """Output format for tool responses."""
    MARKDOWN = "markdown"
    JSON = "json"


class SearchEmailsInput(BaseModel):
    """Input model for searching Gmail messages."""
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    
    query: str = Field(
        ...,
        description=(
            "Gmail search query. Supports standard Gmail operators like: "
            "from:, to:, subject:, is:unread, is:read, in:inbox, after:YYYY/MM/DD, "
            "before:YYYY/MM/DD, has:attachment, label:, etc. "
            "Example: 'from:john@example.com subject:invoice is:unread'"
        ),
        min_length=1
    )
    max_results: int = Field(
        default=20,
        description="Maximum number of messages to return (1-100)",
        ge=1,
        le=100
    )
    include_body: bool = Field(
        default=False,
        description="If true, include full message body in results (slower but more complete)"
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for machine-readable"
    )


class GetEmailInput(BaseModel):
    """Input model for retrieving a specific email."""
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    
    message_id: str = Field(
        ...,
        description="The Gmail message ID to retrieve",
        min_length=1
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for machine-readable"
    )


class SendEmailInput(BaseModel):
    """Input model for sending an email."""
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    
    to: List[str] = Field(
        ...,
        description="List of recipient email addresses",
        min_items=1
    )
    subject: str = Field(
        ...,
        description="Email subject line",
        min_length=1
    )
    body: str = Field(
        ...,
        description="Email body content (plain text or HTML)",
        min_length=1
    )
    cc: Optional[List[str]] = Field(
        default=None,
        description="List of CC recipient email addresses"
    )
    bcc: Optional[List[str]] = Field(
        default=None,
        description="List of BCC recipient email addresses"
    )
    reply_to: Optional[str] = Field(
        default=None,
        description="Reply-to email address"
    )
    is_html: bool = Field(
        default=False,
        description="If true, body is treated as HTML content"
    )


class ReplyToEmailInput(BaseModel):
    """Input model for replying to an email."""
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    
    thread_id: str = Field(
        ...,
        description="The Gmail thread ID to reply to",
        min_length=1
    )
    body: str = Field(
        ...,
        description="Reply body content",
        min_length=1
    )
    reply_all: bool = Field(
        default=False,
        description="If true, reply to all recipients in the thread"
    )
    is_html: bool = Field(
        default=False,
        description="If true, body is treated as HTML content"
    )


class ModifyLabelsInput(BaseModel):
    """Input model for modifying email labels."""
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    
    message_ids: List[str] = Field(
        ...,
        description="List of Gmail message IDs to modify",
        min_items=1
    )
    add_labels: Optional[List[str]] = Field(
        default=None,
        description="List of label names or IDs to add"
    )
    remove_labels: Optional[List[str]] = Field(
        default=None,
        description="List of label names or IDs to remove"
    )


class ArchiveEmailsInput(BaseModel):
    """Input model for archiving emails."""
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    
    message_ids: List[str] = Field(
        ...,
        description="List of Gmail message IDs to archive",
        min_items=1
    )


class DeleteEmailsInput(BaseModel):
    """Input model for deleting emails."""
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    
    message_ids: List[str] = Field(
        ...,
        description="List of Gmail message IDs to delete (moves to trash)",
        min_items=1
    )


class ListLabelsInput(BaseModel):
    """Input model for listing labels."""
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for machine-readable"
    )


class CreateLabelInput(BaseModel):
    """Input model for creating a new label."""
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    
    name: str = Field(
        ...,
        description="Name for the new label",
        min_length=1,
        max_length=100
    )
    label_list_visibility: str = Field(
        default="labelShow",
        description="Label visibility in label list: 'labelShow', 'labelShowIfUnread', or 'labelHide'"
    )
    message_list_visibility: str = Field(
        default="show",
        description="Message visibility in message list: 'show' or 'hide'"
    )


# ==================== TOOL IMPLEMENTATIONS ====================

@mcp.tool(
    name="gmail_search_emails",
    annotations={
        "title": "Search Gmail Messages",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def search_emails(params: SearchEmailsInput) -> str:
    """Search for Gmail messages using Gmail search syntax.
    
    This tool searches the user's Gmail inbox using standard Gmail search operators.
    It returns metadata about matching messages including sender, subject, date, and snippets.
    
    Args:
        params (SearchEmailsInput): Search parameters containing:
            - query (str): Gmail search query with standard operators
            - max_results (int): Maximum number of results to return (1-100)
            - include_body (bool): Whether to include full message bodies
            - response_format (ResponseFormat): Output format (markdown or json)
    
    Returns:
        str: Search results in the requested format. For markdown, returns a formatted
        list of emails. For json, returns structured data with message details.
    """
    try:
        service = get_gmail_service()
        
        # Execute search
        results = service.users().messages().list(
            userId='me',
            q=params.query,
            maxResults=params.max_results
        ).execute()
        
        messages = results.get('messages', [])
        
        if not messages:
            return "No messages found matching your search query."
        
        # Fetch full message details
        detailed_messages = []
        for msg in messages:
            msg_data = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='full' if params.include_body else 'metadata'
            ).execute()
            detailed_messages.append(msg_data)
        
        # Format response
        if params.response_format == ResponseFormat.JSON:
            output = {
                "total_results": len(detailed_messages),
                "query": params.query,
                "messages": []
            }
            
            for msg in detailed_messages:
                headers = msg['payload']['headers']
                message_info = {
                    "id": msg['id'],
                    "thread_id": msg['threadId'],
                    "from": _get_header_value(headers, 'From'),
                    "to": _get_header_value(headers, 'To'),
                    "subject": _get_header_value(headers, 'Subject'),
                    "date": _get_header_value(headers, 'Date'),
                    "snippet": msg.get('snippet', ''),
                    "labels": msg.get('labelIds', [])
                }
                
                if params.include_body:
                    message_info['body'] = _decode_message_body(msg['payload'])
                
                output["messages"].append(message_info)
            
            return json.dumps(output, indent=2)
        
        else:  # Markdown format
            output = f"# Search Results\n\n"
            output += f"**Query:** {params.query}\n"
            output += f"**Found:** {len(detailed_messages)} message(s)\n\n"
            output += "---\n\n"
            
            for i, msg in enumerate(detailed_messages, 1):
                headers = msg['payload']['headers']
                output += f"## {i}. Message\n\n"
                output += f"**ID:** `{msg['id']}`\n"
                output += f"**Thread ID:** `{msg['threadId']}`\n"
                output += f"**From:** {_get_header_value(headers, 'From')}\n"
                output += f"**To:** {_get_header_value(headers, 'To')}\n"
                output += f"**Subject:** {_get_header_value(headers, 'Subject')}\n"
                output += f"**Date:** {_get_header_value(headers, 'Date')}\n"
                output += f"**Labels:** {', '.join(msg.get('labelIds', []))}\n\n"
                output += f"**Snippet:** {msg.get('snippet', '')}\n\n"
                
                if params.include_body:
                    body = _decode_message_body(msg['payload'])
                    output += f"**Body:**\n```\n{body[:500]}{'...' if len(body) > 500 else ''}\n```\n\n"
                
                output += "---\n\n"
            
            return output
    
    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="gmail_get_email",
    annotations={
        "title": "Get Email Details",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def get_email(params: GetEmailInput) -> str:
    """Retrieve the full details of a specific Gmail message.
    
    This tool fetches complete information about a single email including headers,
    body content, and metadata.
    
    Args:
        params (GetEmailInput): Input parameters containing:
            - message_id (str): The Gmail message ID to retrieve
            - response_format (ResponseFormat): Output format (markdown or json)
    
    Returns:
        str: Complete message details in the requested format including sender, recipients,
        subject, date, body content, and labels.
    """
    try:
        service = get_gmail_service()
        
        # Get full message
        msg = service.users().messages().get(
            userId='me',
            id=params.message_id,
            format='full'
        ).execute()
        
        headers = msg['payload']['headers']
        body = _decode_message_body(msg['payload'])
        
        if params.response_format == ResponseFormat.JSON:
            output = {
                "id": msg['id'],
                "thread_id": msg['threadId'],
                "from": _get_header_value(headers, 'From'),
                "to": _get_header_value(headers, 'To'),
                "cc": _get_header_value(headers, 'Cc'),
                "bcc": _get_header_value(headers, 'Bcc'),
                "subject": _get_header_value(headers, 'Subject'),
                "date": _get_header_value(headers, 'Date'),
                "labels": msg.get('labelIds', []),
                "snippet": msg.get('snippet', ''),
                "body": body
            }
            return json.dumps(output, indent=2)
        
        else:  # Markdown format
            output = f"# Email Details\n\n"
            output += f"**ID:** `{msg['id']}`\n"
            output += f"**Thread ID:** `{msg['threadId']}`\n"
            output += f"**From:** {_get_header_value(headers, 'From')}\n"
            output += f"**To:** {_get_header_value(headers, 'To')}\n"
            
            cc = _get_header_value(headers, 'Cc')
            if cc:
                output += f"**CC:** {cc}\n"
            
            output += f"**Subject:** {_get_header_value(headers, 'Subject')}\n"
            output += f"**Date:** {_get_header_value(headers, 'Date')}\n"
            output += f"**Labels:** {', '.join(msg.get('labelIds', []))}\n\n"
            output += f"**Snippet:** {msg.get('snippet', '')}\n\n"
            output += f"## Body\n\n{body}\n"
            
            return output
    
    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="gmail_send_email",
    annotations={
        "title": "Send Email",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True
    }
)
async def send_email(params: SendEmailInput) -> str:
    """Send a new email message.
    
    This tool creates and sends a new email to one or more recipients. Supports
    CC, BCC, custom reply-to addresses, and both plain text and HTML content.
    
    Args:
        params (SendEmailInput): Email parameters containing:
            - to (List[str]): List of recipient email addresses
            - subject (str): Email subject line
            - body (str): Email body content
            - cc (Optional[List[str]]): CC recipients
            - bcc (Optional[List[str]]): BCC recipients
            - reply_to (Optional[str]): Custom reply-to address
            - is_html (bool): Whether body is HTML
    
    Returns:
        str: Success message with sent message ID, or error message if sending fails.
    """
    try:
        service = get_gmail_service()
        
        # Create message
        if params.is_html:
            message = MIMEMultipart('alternative')
            html_part = MIMEText(params.body, 'html')
            message.attach(html_part)
        else:
            message = MIMEText(params.body)
        
        message['To'] = ', '.join(params.to)
        message['Subject'] = params.subject
        
        if params.cc:
            message['Cc'] = ', '.join(params.cc)
        
        if params.bcc:
            message['Bcc'] = ', '.join(params.bcc)
        
        if params.reply_to:
            message['Reply-To'] = params.reply_to
        
        # Send message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_message = {'raw': encoded_message}
        
        result = service.users().messages().send(
            userId='me',
            body=send_message
        ).execute()
        
        return (
            f"✓ Email sent successfully!\n\n"
            f"**Message ID:** {result['id']}\n"
            f"**Thread ID:** {result['threadId']}\n"
            f"**To:** {', '.join(params.to)}\n"
            f"**Subject:** {params.subject}"
        )
    
    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="gmail_reply_to_email",
    annotations={
        "title": "Reply to Email",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True
    }
)
async def reply_to_email(params: ReplyToEmailInput) -> str:
    """Reply to an existing email thread.
    
    This tool sends a reply to an existing email conversation. Can reply to just
    the sender or to all recipients (reply all).
    
    Args:
        params (ReplyToEmailInput): Reply parameters containing:
            - thread_id (str): The Gmail thread ID to reply to
            - body (str): Reply body content
            - reply_all (bool): Whether to reply to all recipients
            - is_html (bool): Whether body is HTML
    
    Returns:
        str: Success message with reply message ID, or error message if reply fails.
    """
    try:
        service = get_gmail_service()
        
        # Get original message to extract headers
        thread = service.users().threads().get(
            userId='me',
            id=params.thread_id
        ).execute()
        
        original_msg = thread['messages'][0]
        headers = original_msg['payload']['headers']
        
        # Create reply
        if params.is_html:
            message = MIMEMultipart('alternative')
            html_part = MIMEText(params.body, 'html')
            message.attach(html_part)
        else:
            message = MIMEText(params.body)
        
        # Set reply headers
        subject = _get_header_value(headers, 'Subject')
        if not subject.lower().startswith('re:'):
            subject = f"Re: {subject}"
        
        message['Subject'] = subject
        message['In-Reply-To'] = _get_header_value(headers, 'Message-ID')
        message['References'] = _get_header_value(headers, 'Message-ID')
        
        # Set recipients
        if params.reply_all:
            to_addresses = _get_header_value(headers, 'From')
            cc_addresses = _get_header_value(headers, 'Cc')
            message['To'] = to_addresses
            if cc_addresses:
                message['Cc'] = cc_addresses
        else:
            message['To'] = _get_header_value(headers, 'From')
        
        # Send reply
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_message = {
            'raw': encoded_message,
            'threadId': params.thread_id
        }
        
        result = service.users().messages().send(
            userId='me',
            body=send_message
        ).execute()
        
        return (
            f"✓ Reply sent successfully!\n\n"
            f"**Message ID:** {result['id']}\n"
            f"**Thread ID:** {result['threadId']}\n"
            f"**To:** {message['To']}\n"
            f"**Subject:** {subject}"
        )
    
    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="gmail_modify_labels",
    annotations={
        "title": "Modify Email Labels",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def modify_labels(params: ModifyLabelsInput) -> str:
    """Add or remove labels from Gmail messages.
    
    This tool modifies the labels on one or more messages. Can add labels, remove labels,
    or both in a single operation. Supports both label names and label IDs.
    
    Args:
        params (ModifyLabelsInput): Label modification parameters containing:
            - message_ids (List[str]): List of message IDs to modify
            - add_labels (Optional[List[str]]): Labels to add
            - remove_labels (Optional[List[str]]): Labels to remove
    
    Returns:
        str: Success message indicating how many messages were modified and which
        labels were added or removed.
    """
    try:
        service = get_gmail_service()
        
        # Get all available labels to resolve names to IDs
        labels_result = service.users().labels().list(userId='me').execute()
        label_map = {label['name']: label['id'] for label in labels_result.get('labels', [])}
        label_map.update({label['id']: label['id'] for label in labels_result.get('labels', [])})
        
        # Resolve label names to IDs
        add_label_ids = []
        if params.add_labels:
            for label in params.add_labels:
                if label in label_map:
                    add_label_ids.append(label_map[label])
                else:
                    return f"Error: Label '{label}' not found. Use gmail_list_labels to see available labels."
        
        remove_label_ids = []
        if params.remove_labels:
            for label in params.remove_labels:
                if label in label_map:
                    remove_label_ids.append(label_map[label])
                else:
                    return f"Error: Label '{label}' not found. Use gmail_list_labels to see available labels."
        
        # Modify labels
        body = {}
        if add_label_ids:
            body['addLabelIds'] = add_label_ids
        if remove_label_ids:
            body['removeLabelIds'] = remove_label_ids
        
        if not body:
            return "Error: No labels to add or remove. Specify at least one label operation."
        
        # Apply to all messages
        modified_count = 0
        for message_id in params.message_ids:
            service.users().messages().modify(
                userId='me',
                id=message_id,
                body=body
            ).execute()
            modified_count += 1
        
        output = f"✓ Successfully modified {modified_count} message(s)\n\n"
        
        if add_label_ids:
            output += f"**Added labels:** {', '.join(params.add_labels)}\n"
        if remove_label_ids:
            output += f"**Removed labels:** {', '.join(params.remove_labels)}\n"
        
        return output
    
    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="gmail_archive_emails",
    annotations={
        "title": "Archive Emails",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def archive_emails(params: ArchiveEmailsInput) -> str:
    """Archive Gmail messages by removing them from the inbox.
    
    This tool removes messages from the inbox while keeping them in "All Mail".
    Messages remain searchable and accessible but won't appear in the inbox.
    
    Args:
        params (ArchiveEmailsInput): Archive parameters containing:
            - message_ids (List[str]): List of message IDs to archive
    
    Returns:
        str: Success message indicating how many messages were archived.
    """
    try:
        service = get_gmail_service()
        
        # Archive by removing INBOX label
        body = {'removeLabelIds': ['INBOX']}
        
        archived_count = 0
        for message_id in params.message_ids:
            service.users().messages().modify(
                userId='me',
                id=message_id,
                body=body
            ).execute()
            archived_count += 1
        
        return f"✓ Successfully archived {archived_count} message(s)"
    
    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="gmail_delete_emails",
    annotations={
        "title": "Delete Emails",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def delete_emails(params: DeleteEmailsInput) -> str:
    """Move Gmail messages to trash.
    
    This tool moves messages to the trash folder. Messages in trash are automatically
    deleted after 30 days. Messages can be restored from trash if needed.
    
    Args:
        params (DeleteEmailsInput): Delete parameters containing:
            - message_ids (List[str]): List of message IDs to delete
    
    Returns:
        str: Success message indicating how many messages were moved to trash.
    """
    try:
        service = get_gmail_service()
        
        deleted_count = 0
        for message_id in params.message_ids:
            service.users().messages().trash(
                userId='me',
                id=message_id
            ).execute()
            deleted_count += 1
        
        return f"✓ Successfully moved {deleted_count} message(s) to trash"
    
    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="gmail_list_labels",
    annotations={
        "title": "List Gmail Labels",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def list_labels(params: ListLabelsInput) -> str:
    """List all Gmail labels in the user's account.
    
    This tool retrieves all labels including system labels (INBOX, SENT, DRAFT, etc.)
    and user-created labels.
    
    Args:
        params (ListLabelsInput): Input parameters containing:
            - response_format (ResponseFormat): Output format (markdown or json)
    
    Returns:
        str: List of all labels with their IDs, names, and types in the requested format.
    """
    try:
        service = get_gmail_service()
        
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        
        if not labels:
            return "No labels found."
        
        if params.response_format == ResponseFormat.JSON:
            output = {
                "total_labels": len(labels),
                "labels": [
                    {
                        "id": label['id'],
                        "name": label['name'],
                        "type": label['type']
                    }
                    for label in labels
                ]
            }
            return json.dumps(output, indent=2)
        
        else:  # Markdown format
            output = f"# Gmail Labels\n\n**Total:** {len(labels)} label(s)\n\n"
            
            # Group by type
            system_labels = [l for l in labels if l['type'] == 'system']
            user_labels = [l for l in labels if l['type'] == 'user']
            
            if system_labels:
                output += "## System Labels\n\n"
                for label in sorted(system_labels, key=lambda x: x['name']):
                    output += f"- **{label['name']}** (`{label['id']}`)\n"
                output += "\n"
            
            if user_labels:
                output += "## User Labels\n\n"
                for label in sorted(user_labels, key=lambda x: x['name']):
                    output += f"- **{label['name']}** (`{label['id']}`)\n"
                output += "\n"
            
            return output
    
    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="gmail_create_label",
    annotations={
        "title": "Create Gmail Label",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False
    }
)
async def create_label(params: CreateLabelInput) -> str:
    """Create a new Gmail label.
    
    This tool creates a new user label with specified visibility settings. Labels
    can be used to organize and categorize emails.
    
    Args:
        params (CreateLabelInput): Label creation parameters containing:
            - name (str): Name for the new label
            - label_list_visibility (str): Visibility in label list
            - message_list_visibility (str): Visibility in message list
    
    Returns:
        str: Success message with the new label's ID and name.
    """
    try:
        service = get_gmail_service()
        
        # Check if label already exists
        existing_labels = service.users().labels().list(userId='me').execute()
        for label in existing_labels.get('labels', []):
            if label['name'].lower() == params.name.lower():
                return f"Error: Label '{params.name}' already exists (ID: {label['id']})"
        
        # Create label
        label_object = {
            'name': params.name,
            'labelListVisibility': params.label_list_visibility,
            'messageListVisibility': params.message_list_visibility
        }
        
        result = service.users().labels().create(
            userId='me',
            body=label_object
        ).execute()
        
        return (
            f"✓ Label created successfully!\n\n"
            f"**Name:** {result['name']}\n"
            f"**ID:** {result['id']}"
        )
    
    except Exception as e:
        return _handle_api_error(e)


# ==================== MAIN ====================

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
