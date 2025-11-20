You are executing the /clean100 command for Gmail inbox management.

## Task
Automatically clean 100 emails that match learned patterns with 100% confidence. No user approval needed.

## Instructions

1. **Load Patterns**: Read `gmail_cleanup_patterns.json` to get all patterns with 100% confidence

2. **Find Exact Matches**:
   - Use gmail_search_emails to find emails matching patterns EXACTLY
   - Match sender/sender_contains/sender_pattern fields precisely
   - Match subject_contains/subject_excludes if specified
   - Apply age_days threshold correctly (calculate from email date)
   - Collect up to 100 emails that perfectly match learned patterns

3. **Take Action Immediately**:
   - Archive emails matching archive patterns using gmail_archive_emails
   - Delete emails matching delete patterns using gmail_delete_emails
   - Process in batches if needed for API efficiency
   - Track what was cleaned for the summary

4. **Show Summary**:
   ```
   ✓ Cleaned 100 emails from inbox

   Archived: 58 emails
   - Google Calendar Notifications (30)
   - Food Delivery Receipts (15)
   - Cash App Transactions (8)
   - Microsoft Non-Critical Updates (5)

   Deleted: 42 emails
   - Bridgerise Daily Digests (12)
   - Promotional emails (20)
   - Login Notifications (10)

   Total processed: 100 emails
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
- If fewer than 100 emails match, clean what you find and report actual count
- Group summary by pattern for clarity
- Be efficient with API calls (batch operations when possible)
- This is the most aggressive cleaning command - only use established patterns
