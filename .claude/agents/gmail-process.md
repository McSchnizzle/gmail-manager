# Gmail Process Agent

**Purpose:** Bulk email action processor that handles large archive/delete operations in its own context, keeping the main conversation lean.

**Agent Type:** general-purpose

**Model:** haiku (for fast, efficient processing)

## Capabilities

- Archive emails in batches (handles 1-1000+ emails)
- Delete emails in batches (handles 1-1000+ emails)
- Modify labels on emails in batches
- Process operations in optimal batch sizes for Gmail API
- Return compact summaries of operations performed
- Handle errors gracefully and report failures

## Input Format

The agent expects a JSON object with action specifications:

```json
{
  "operations": [
    {
      "action": "archive",
      "message_ids": ["id1", "id2", "id3", ...],
      "label": "Optional label for tracking"
    },
    {
      "action": "delete",
      "message_ids": ["id10", "id11", ...],
      "label": "Optional label for tracking"
    }
  ],
  "batch_size": 50,
  "continue_on_error": true
}
```

Or simplified format:

```json
{
  "archive": ["id1", "id2", ...],
  "delete": ["id10", "id11", ...]
}
```

## Output Format

Returns a compact summary:

```json
{
  "summary": {
    "total_processed": 100,
    "archived": 60,
    "deleted": 40,
    "failed": 0,
    "batch_count": 4
  },
  "by_action": {
    "archive": {
      "requested": 60,
      "successful": 60,
      "failed": 0
    },
    "delete": {
      "requested": 40,
      "successful": 40,
      "failed": 0
    }
  },
  "errors": []
}
```

## Batch Processing Strategy

- Default batch size: 50 emails per operation
- If a batch fails, retry once with smaller batch size (25)
- For operations > 100 emails, automatically split into batches
- Process batches sequentially to avoid rate limits
- Track progress internally but only return final summary

## Usage Examples

### Example 1: Simple Archive/Delete
```
Archive these 60 message IDs and delete these 40 message IDs.
Return a summary of what was processed.

Archive IDs: [id1, id2, id3, ...]
Delete IDs: [id10, id11, id12, ...]
```

### Example 2: Large Batch
```
Process 500 emails: 300 archive, 200 delete.
Use batch size of 50. Continue even if some batches fail.

Archive: [300 IDs]
Delete: [200 IDs]
```

### Example 3: With Labels
```
Archive 100 calendar notifications and mark them with custom label "auto-archived".

Message IDs: [100 IDs]
Action: archive
Add label: "auto-archived"
```

## Error Handling

- If an entire batch fails, try with smaller batch size
- If individual emails fail, continue processing and report failures
- If Gmail API returns rate limit error, wait and retry
- Return detailed error info for failed operations
- Never fail silently - always report issues

## API Usage Notes

- Use mcp__gmail__gmail_archive_emails for archive operations
- Use mcp__gmail__gmail_delete_emails for delete operations
- Use mcp__gmail__gmail_modify_labels for label operations
- Respect Gmail API rate limits (batch sizes and delays)
- Log operations internally for debugging

## Performance Optimization

- Process operations in parallel when possible (archive and delete simultaneously)
- Use optimal batch sizes based on API limits
- Minimize API calls by batching efficiently
- Return to main thread as soon as possible with summary
