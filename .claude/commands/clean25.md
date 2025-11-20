You are executing the /clean25 command for Gmail inbox management.

## Task
Automatically clean 20 emails with 100% pattern confidence, then show 5 uncertain emails for user approval.

## Instructions

### Phase 1: Auto-Clean (20 emails)

1. **Load Patterns**: Read `gmail_cleanup_patterns.json` for exact pattern matches

2. **Find 100% Confident Matches**:
   - Use gmail_search_emails to find emails matching patterns EXACTLY
   - Match sender, subject, and age criteria precisely
   - Collect 20 emails that perfectly match learned patterns

3. **Take Action Immediately**:
   - Archive or delete these 20 emails using gmail_archive_emails or gmail_delete_emails
   - Do NOT show these to the user beforehand
   - Keep track of what was cleaned for the summary

### Phase 2: Show Uncertain Emails (5 emails)

4. **Find Uncertain Candidates**: Search for 5 emails that are:
   - Partial pattern matches (sender similar but not exact)
   - Obvious promotional/spam patterns not yet in patterns file
   - Match pattern intent but outside age threshold
   - Old emails that have aged into irrelevance (newsletters, notifications, etc.)
   - Similar to existing patterns but from new senders

5. **Display Format** (1-2 lines per email, number them 1-5):
   ```
   1. [ARCHIVE?] sender@example.com | "Subject" | Dec 15 | Similar to: Food Delivery Receipts
   2. [DELETE?] promo@site.com | "Weekly Update" | Dec 12 | New: Promotional digest pattern
   ```

6. **Wait for Response**: Ask user to reply with numbers they approve (e.g., "1, 3, 5")

7. **Take Action**: Process approved uncertain emails

### Phase 3: Summary

8. **Show Complete Summary**:
   ```
   ✓ Auto-cleaned: 20 emails (12 archived, 8 deleted)
   ✓ User-approved: 3 emails (2 archived, 1 deleted)
   Total cleaned: 23 emails
   ```

## Pattern Matching Rules
- **100% confidence**: Must match patterns EXACTLY from gmail_cleanup_patterns.json
- **Uncertain**: Partially matches or seems like it should match based on similarity
- Calculate email age from date headers
- Respect archive vs delete distinction

## Important
- Execute Phase 1 immediately without user confirmation
- Only show uncertain emails in Phase 2
- Be thoughtful about what qualifies as "uncertain but probably safe"
- Emails that are valuable when new but age poorly are good uncertain candidates
