You are executing the /clean10 command for Gmail inbox management.

## Task
Show the user 10 emails that match learned cleanup patterns and wait for their approval before taking action.

## Instructions

1. **Load Patterns**: Read `gmail_cleanup_patterns.json` to get all archive and delete patterns with 100% confidence.

2. **Search for Matching Emails**:
   - Use gmail_search_emails to find emails matching each pattern
   - Match patterns exactly as specified (sender, subject_contains, age_days)
   - Calculate age based on the `age_days` threshold in each pattern
   - Collect up to 10 emails total

3. **Display Format** (1-2 lines per email, number them 1-10):
   ```
   1. [ARCHIVE] sender@example.com | "Subject Line" | Dec 15 | Pattern: Google Calendar Notifications
   2. [DELETE] spam@company.com | "Daily Digest" | Dec 10 | Pattern: Bridgerise Daily Digests
   ```

4. **Show Your Logic**: Briefly explain the criteria being used (age thresholds, sender patterns, etc.)

5. **Wait for Response**: Ask the user to reply with the numbers they approve (e.g., "1, 3, 5, 7")

6. **Take Action**:
   - Archive or delete only the approved emails using gmail_archive_emails or gmail_delete_emails
   - Show confirmation of actions taken

## Pattern Matching Rules
- Must match patterns EXACTLY from gmail_cleanup_patterns.json
- Check sender/sender_contains/sender_pattern fields
- Check subject_contains/subject_excludes if specified
- Apply age_days threshold (if specified) - calculate from email date
- Respect the action type (archive vs delete) from the pattern's category

## Important
- Only show emails that match existing 100% confidence patterns
- Be clear about which action (archive/delete) will be taken
- If fewer than 10 emails match, show what you found
- Display emails in order of age (oldest first)
