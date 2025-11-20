You are executing the /clean50 command for Gmail inbox management.

## Task
Automatically clean 50 emails that match learned patterns with 100% confidence. No user approval needed.

## Instructions

1. **Load Patterns**: Read `gmail_cleanup_patterns.json` to get all patterns with 100% confidence

2. **Find Exact Matches**:
   - Use gmail_search_emails to find emails matching patterns EXACTLY
   - Match sender/sender_contains/sender_pattern fields precisely
   - Match subject_contains/subject_excludes if specified
   - Apply age_days threshold correctly (calculate from email date)
   - Collect up to 50 emails that perfectly match learned patterns

3. **Take Action Immediately**:
   - Archive emails matching archive patterns using gmail_archive_emails
   - Delete emails matching delete patterns using gmail_delete_emails
   - Process in batches if needed for API efficiency
   - Track what was cleaned for the summary

4. **Show Summary**:
   ```
   ✓ Cleaned 50 emails from inbox

   Archived: 28 emails
   - Google Calendar Notifications (15)
   - Food Delivery Receipts (8)
   - Cash App Transactions (5)

   Deleted: 22 emails
   - Bridgerise Daily Digests (10)
   - Promotional emails (12)

   Total processed: 50 emails
   ```

## Pattern Matching Rules
- Must match patterns EXACTLY from gmail_cleanup_patterns.json
- Only use patterns with confidence: 100
- Calculate email age based on date headers and age_days threshold
- Respect the action type (archive vs delete) from pattern category
- If patterns exist but don't specify age_days, match on sender/subject only

## Important
- No user confirmation needed - execute immediately
- Only process emails with 100% confident pattern matches
- If fewer than 50 emails match, clean what you find and report actual count
- Group summary by pattern for clarity
- Be efficient with API calls (batch operations when possible)
