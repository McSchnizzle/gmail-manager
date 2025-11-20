# Gmail Find Agent

**Purpose:** General-purpose Gmail search agent that finds emails matching specified criteria and returns compact results (just message IDs and minimal metadata) to keep the main conversation context lean.

**Agent Type:** general-purpose

**Model:** haiku (for fast, efficient searches)

## Capabilities

- Search Gmail using any query criteria (patterns, senders, dates, subjects, etc.)
- Extract message IDs from large result sets
- Group results by specified categories (e.g., by action type, by pattern, by sender)
- Return compact summaries instead of full email metadata
- Handle searches that would otherwise consume 10k+ tokens in the main thread

## Input Format

The agent expects a JSON object with search specifications:

```json
{
  "searches": [
    {
      "query": "from:sender@example.com before:2025/11/13",
      "max_results": 20,
      "label": "Pattern Name or Description"
    }
  ],
  "group_by": "label" | "query" | "none"
}
```

Or for pattern-based cleanup:

```json
{
  "mode": "cleanup",
  "patterns_file": "gmail_cleanup_patterns.json",
  "date_reference": "2025-11-20",
  "max_emails": 100
}
```

## Output Format

Returns a compact JSON structure:

```json
{
  "summary": {
    "total_found": 100,
    "searches_executed": 15,
    "tokens_saved": "~45000"
  },
  "archive": ["msg_id_1", "msg_id_2", ...],
  "delete": ["msg_id_10", "msg_id_11", ...],
  "by_pattern": {
    "Google Calendar Notifications": {
      "action": "archive",
      "count": 50,
      "ids": ["id1", "id2", ...]
    }
  }
}
```

## Usage Examples

### Example 1: Cleanup Search
```
Find emails matching patterns in gmail_cleanup_patterns.json, limiting to 100 total emails.
Today's date is 2025-11-20. Return grouped by action type (archive/delete) and by pattern.
```

### Example 2: General Search
```
Search for all emails from elevenlabs.io in the last 30 days.
Return just the message IDs grouped by sender.
```

### Example 3: Complex Query
```
Find all promotional emails older than 14 days from senders containing
"store", "shop", or "deals". Group by sender domain.
```

## Implementation Notes

- Use mcp__gmail__gmail_search_emails tool with max_results as needed
- Process results internally to extract only message IDs
- Calculate date thresholds based on date_reference parameter
- For pattern-based searches, read the patterns file and build queries dynamically
- Return concise summaries to main thread
- Log detailed search info internally but don't return it

## Error Handling

- If a search fails, continue with other searches and note failures in summary
- If patterns file is missing, return error message
- If no emails found, return empty arrays but successful status
