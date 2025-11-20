# Gmail Manager Agents

This directory contains specialized agents that help keep the main conversation context lean while processing large volumes of Gmail data.

## Architecture Overview

The Gmail Manager uses an agent-based architecture for commands that process 50+ emails. This approach solves the **context bloat problem** where large Gmail search results consume 15k-50k+ tokens in the main conversation.

### The Problem (Before Agents)

```
User: /clean100

Main Thread:
  ↓ Search 100 calendar notifications → 15k tokens of email metadata
  ↓ Search 20 food receipts → 3k tokens
  ↓ Search 10 promotional emails → 2k tokens
  ↓ ... (more searches)

Total: ~50k tokens consumed just for search results!
Main conversation becomes expensive and slow.
```

### The Solution (With Agents)

```
User: /clean100

Main Thread:
  ↓ Launch gmail-find agent

gmail-find Agent (in separate context):
  ↓ Reads patterns file
  ↓ Executes all searches (50k tokens here, isolated)
  ↓ Extracts just message IDs
  ↓ Returns compact result: ~500 tokens

Main Thread:
  ↓ Receives compact list
  ↓ Launch gmail-process agent

gmail-process Agent (in separate context):
  ↓ Processes archive/delete in batches
  ↓ Returns summary: ~300 tokens

Main Thread:
  ↓ Shows user final summary

Total main thread usage: ~1k tokens (50x improvement!)
```

## Available Agents

### 1. gmail-find

**Purpose:** General-purpose Gmail search agent

**Model:** Haiku (fast and efficient)

**Use Cases:**
- Pattern-based cleanup searches
- Finding emails by complex criteria
- Bulk email discovery
- Any search that would return >100 emails

**Input:**
```json
{
  "mode": "cleanup",
  "patterns_file": "gmail_cleanup_patterns.json",
  "date_reference": "2025-11-20",
  "max_emails": 100
}
```

**Output:**
```json
{
  "summary": {"total_found": 100, "searches_executed": 15},
  "archive": ["id1", "id2", ...],
  "delete": ["id10", "id11", ...],
  "by_pattern": {
    "Pattern Name": {"action": "archive", "count": 50, "ids": [...]}
  }
}
```

**Token Savings:** ~40-50k tokens per 100 emails

### 2. gmail-process

**Purpose:** Bulk email action processor

**Model:** Haiku (fast and efficient)

**Use Cases:**
- Archiving 50+ emails
- Deleting 50+ emails
- Batch label modifications
- Any bulk operation

**Input:**
```json
{
  "archive": ["id1", "id2", ...],
  "delete": ["id10", "id11", ...],
  "batch_size": 50
}
```

**Output:**
```json
{
  "summary": {
    "total_processed": 100,
    "archived": 60,
    "deleted": 40,
    "failed": 0
  },
  "by_action": {
    "archive": {"successful": 60, "failed": 0},
    "delete": {"successful": 40, "failed": 0}
  }
}
```

**Token Savings:** ~5-10k tokens per 100 emails

## Commands Using Agents

- `/clean50` - Uses both agents for 50 email cleanup
- `/clean100` - Uses both agents for 100 email cleanup
- (Future: `/clean500`, `/clean1000` can easily use the same agents)

**Commands NOT using agents** (small enough to not need them):
- `/clean10` - Only 10 emails, direct processing is fine
- `/clean25` - 20 auto + 5 manual, direct processing is fine

## Performance Benefits

| Command | Without Agents | With Agents | Savings |
|---------|---------------|-------------|---------|
| /clean50 | ~20k tokens | ~1k tokens | 20x |
| /clean100 | ~50k tokens | ~1k tokens | 50x |
| /clean500 | ~250k tokens | ~2k tokens | 125x |

## Reusability

These agents are **not just for cleanup**. They can be used for:

- **gmail-find:**
  - "Find all emails from X in the last month"
  - "Search for emails with attachments > 5MB"
  - "Find all newsletters I haven't unsubscribed from"
  - Any complex Gmail query that returns many results

- **gmail-process:**
  - Bulk star/unstar operations
  - Batch label applications
  - Mass archiving of old threads
  - Any bulk Gmail modification

## Future Enhancements

Potential new agents:
- **gmail-learn:** Analyzes emails and suggests new patterns
- **gmail-analyze:** Generates inbox statistics and insights
- **gmail-unsubscribe:** Finds and unsubscribes from newsletters

## Implementation Details

Agents are defined as markdown files in `.claude/agents/`:
- `gmail-find.md` - Search agent specification
- `gmail-process.md` - Process agent specification

Commands launch agents using the Task tool:
```
Launch gmail-find agent with task: "Find emails matching patterns..."
```

Agents execute in their own context and return compact results to the main thread.

## Testing

To test the agent-based approach:
1. Run `/clean50` or `/clean100`
2. Observe the agent launches in the UI
3. Check that main thread token usage stays low
4. Verify cleanup results are accurate

Compare with non-agent commands (`/clean10`) to see the difference in token usage.
