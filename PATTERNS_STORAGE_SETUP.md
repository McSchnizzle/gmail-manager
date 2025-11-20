# Gmail Cleanup Patterns - Permanent Storage Setup

## The Problem We Just Solved

Your Gmail cleanup patterns were stored in the Claude skill folder (`/mnt/skills/user/gmail-manager/`), which doesn't persist reliably between sessions. You have **17 established cleanup rules**, but only 6 were showing up in the skill file.

## The Solution: Store Patterns Locally

Store your patterns file alongside your Gmail MCP server so it's always available and under your control.

## Setup Instructions

### 1. Copy the Patterns File to Your MCP Server Directory

```bash
# Navigate to your Gmail MCP server directory
cd /Users/paulbrown/Desktop/coding-projects/claude-gmail-manager/

# The patterns file is ready to download from outputs
# Copy it to your MCP server directory
cp ~/Downloads/gmail_cleanup_patterns.json .
```

### 2. Verify the File is There

```bash
ls -la ~/Desktop/coding-projects/claude-gmail-manager/gmail_cleanup_patterns.json
```

You should see the file with today's date.

### 3. How It Works Going Forward

**The patterns file contains all 17 of your cleanup rules:**

**Archive Patterns (5):**
1. Google Calendar notifications (>1 day)
2. Cash App transactions (>3 days)
3. Food delivery receipts (>5 days)
4. Microsoft non-critical updates (>2 weeks)
5. Robotime Online emails

**Delete Patterns (12):**
1. Bridgerise Daily Digests (>1 day)
2. USPS Informed Delivery (>1 week)
3. Google Alerts daily digests (>1 week)
4. YouTube TV promotional (>1 week)
5. Ridwell notifications (>1 week)
6. Spotify concert presales (>3 days)
7. NBC promotional (>1 week)
8. Oura Ring marketing (>2 weeks)
9. Google Store promotions (>1 week)
10. Lyft and Uber receipts (>10 days)
11. Login notifications any service (>10 days)
12. Vercel deployment errors (>3 days)

### 4. Future Updates

When new patterns are added:
1. I'll update both the JSON file and the skill's markdown file
2. You'll get a notification to save the updated JSON file
3. The JSON file is the master - always keep it in your MCP server directory

### 5. Backup Recommendation

Consider backing up this file periodically:

```bash
# Create a backup
cp gmail_cleanup_patterns.json gmail_cleanup_patterns_backup_$(date +%Y%m%d).json
```

## File Locations

- **Master patterns file:** `/Users/paulbrown/Desktop/coding-projects/claude-gmail-manager/gmail_cleanup_patterns.json`
- **Skill reference (human-readable):** `/mnt/skills/user/gmail-manager/references/learned_patterns.md`
- **Your memory:** Also stores all patterns as individual rules

## Why This is Better

✅ **Persistent** - Survives session resets  
✅ **Version controlled** - You can track changes  
✅ **Portable** - Easy to back up or share  
✅ **Source of truth** - One authoritative file  
✅ **Human and machine readable** - JSON format with clear structure

## Download Your Patterns File

The file is ready in your outputs: `gmail_cleanup_patterns.json`
