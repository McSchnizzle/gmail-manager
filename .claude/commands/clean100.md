You are executing the /clean100 command for Gmail inbox management.

## Task
Automatically clean 100 emails that match learned patterns with 100% confidence. No user approval needed.

## Agent-Based Architecture

This command uses two specialized agents to keep the main conversation context lean:

1. **gmail-find agent**: Searches for matching emails and returns compact results (just IDs)
2. **gmail-process agent**: Executes bulk archive/delete operations in its own context

## Instructions

### Step 1: Launch Gmail Find Agent

Launch the `gmail-find` agent to search for emails matching patterns:

```
Task: Find up to 100 emails matching patterns in gmail_cleanup_patterns.json

Input:
{
  "mode": "cleanup",
  "patterns_file": "gmail_cleanup_patterns.json",
  "date_reference": "YYYY-MM-DD",  // Use today's date
  "max_emails": 100
}

Expected output: Compact JSON with message IDs grouped by action type (archive/delete) and by pattern.
```

The agent will:
- Read gmail_cleanup_patterns.json
- Execute searches for all 100% confidence patterns
- Calculate age thresholds based on today's date
- Return only message IDs (not full email metadata)
- Save ~40k+ tokens by keeping heavy results in agent context

### Step 2: Launch Gmail Process Agent

Once you receive the compact results from gmail-find, launch the `gmail-process` agent:

```
Task: Process the following email operations

Input:
{
  "archive": ["msg_id_1", "msg_id_2", ...],
  "delete": ["msg_id_10", "msg_id_11", ...],
  "batch_size": 50
}

Expected output: Summary of operations performed (counts, success/failure).
```

The agent will:
- Archive emails in batches
- Delete emails in batches
- Handle any errors gracefully
- Return compact summary of what was processed

### Step 3: Display Summary

Format and display the combined results to the user:

```
✓ Cleaned [N] emails from inbox

Archived: [N] emails
- [Pattern Name] (count)
- [Pattern Name] (count)
...

Deleted: [N] emails
- [Pattern Name] (count)
- [Pattern Name] (count)
...

Total processed: [N] emails
```

## Pattern Matching Rules (Handled by gmail-find agent)

- Must match patterns EXACTLY from gmail_cleanup_patterns.json
- Only use patterns with confidence: 100
- Calculate email age based on date headers and age_days threshold
- Respect the action type (archive vs delete) from pattern category
- If patterns exist but don't specify age_days, match on sender/subject only

## Important Notes

- **No user confirmation needed** - execute immediately
- Only process emails with 100% confident pattern matches
- If fewer than 100 emails match, clean what you find and report actual count
- Group summary by pattern for clarity
- Agents handle all heavy lifting and keep main thread context clean
- This is the most aggressive cleaning command - only use established patterns

## Benefits of Agent-Based Approach

- **Context Efficiency**: Main thread uses ~500 tokens instead of 50k+ tokens
- **Parallel Processing**: Agents can work independently and efficiently
- **Scalability**: Easy to scale to /clean500 or /clean1000 commands
- **Error Isolation**: Agent errors don't pollute main conversation
- **Reusability**: gmail-find and gmail-process agents can be used by other commands
