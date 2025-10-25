# Bug Tracking

This directory contains all documented bugs and issues found during user testing.

## Folder Structure

```
bugs/
├── open/               # Bugs that need to be fixed
├── in-progress/        # Bugs currently being worked on
├── fixed/              # Bugs that have been resolved
├── wont-fix/          # Bugs that won't be addressed (with explanation)
└── screenshots/        # Visual evidence for bugs
```

## Bug Workflow

1. **Discovery**: Find bug during testing
2. **Document**: Create bug report using `../BUG_REPORT_TEMPLATE.md`
3. **Save**: Place in `open/` folder with naming: `BUG-XXX-[short-description].md`
4. **Triage**: Assign severity (Critical/High/Medium/Low)
5. **Track**: Move through folders as status changes
6. **Verify**: When fixed, re-test and move to `fixed/`

## Bug Naming Convention

Format: `BUG-[ID]-[short-description].md`

Examples:
- `BUG-001-progress-lost-on-logout.md`
- `BUG-002-submit-button-disabled.md`
- `BUG-003-mobile-tooltip-cutoff.md`

## Bug ID Assignment

Use sequential numbering starting from 001. Check existing bugs to get next available ID:

```bash
# Count existing bugs to get next ID
ls open/ in-progress/ fixed/ wont-fix/ | grep "BUG-" | wc -l
```

## Screenshot Guidelines

**Naming**: `bug-[ID]-[description]-[optional-number].png`

Examples:
- `screenshots/bug-001-progress-dashboard.png`
- `screenshots/bug-001-console-error.png`
- `screenshots/bug-002-mobile-view.png`

**Tips**:
- Capture full browser window including address bar
- Include browser console if there are errors
- Circle or annotate the issue if not obvious
- For mobile: capture both portrait and landscape if relevant

## Quick Bug Logging

For rapid testing, you can use this one-liner format:

```bash
echo "# BUG-XXX: [Title]
- **Severity**: [Critical/High/Medium/Low]
- **What**: [Description]
- **Expected**: [What should happen]
- **Actual**: [What happened]
- **Steps**: [How to reproduce]
" > open/BUG-XXX-[description].md
```

## Bug Status Tracking

### Open (Unaddressed)
Bugs in this folder need attention. Sort by severity:
1. Critical - App broken, data loss
2. High - Major feature broken
3. Medium - Minor feature broken, has workaround
4. Low - Cosmetic, minor inconvenience

### In Progress (Being Fixed)
Developer is actively working on fix. Include:
- Assigned developer name
- Expected completion date
- Related code changes

### Fixed (Resolved)
Bug has been fixed and verified. Include in report:
- Version fixed in
- Verification date
- Who verified

### Won't Fix (Closed)
Bug won't be addressed. Always include explanation:
- Why not fixing (edge case, out of scope, design decision, etc.)
- Workaround if available
- Who made decision

## Current Bug Summary

Track your bug counts here:

| Status | Critical | High | Medium | Low | Total |
|--------|----------|------|--------|-----|-------|
| Open | 0 | 0 | 0 | 0 | 0 |
| In Progress | 0 | 0 | 0 | 0 | 0 |
| Fixed | 0 | 0 | 0 | 0 | 0 |
| Won't Fix | 0 | 0 | 0 | 0 | 0 |
| **TOTAL** | **0** | **0** | **0** | **0** | **0** |

Update this table as you find and resolve bugs.

## Example Bug Report

See `BUG_REPORT_TEMPLATE.md` in parent directory for full template.

Quick example:
```markdown
# Bug Report: BUG-001

**Date**: 2025-10-24
**Status**: 🔴 Open
**Severity**: 🔴 Critical

## Summary
User progress resets to zero after logout

## Steps to Reproduce
1. Register new account
2. Complete 5 exercises (verify XP shows)
3. Logout
4. Login again
5. Check dashboard

## Expected
Progress shows 500 XP and 5 exercises completed

## Actual
Progress reset to 0 XP, 0 exercises

## Environment
- Browser: Chrome 120
- OS: macOS 14
- Device: Desktop

## Console Errors
```
POST /api/progress 500 Internal Server Error
{"detail": "User not found"}
```
```

## Tips for Bug Management

1. **Be Consistent**: Use the template and naming conventions
2. **Be Thorough**: Include all reproduction steps
3. **Be Organized**: Keep folders tidy, move bugs promptly
4. **Be Visual**: Screenshot everything
5. **Be Updated**: Change status as bugs progress
6. **Be Prioritized**: Critical bugs first
7. **Be Verified**: Re-test fixed bugs before closing

## Integration with GitHub Issues

When ready to create GitHub issues from bugs:

```bash
# For each critical/high bug:
gh issue create \
  --title "$(head -n 1 open/BUG-001-description.md | sed 's/# //')" \
  --body "$(cat open/BUG-001-description.md)" \
  --label "bug,user-testing" \
  --assignee username
```

## Bulk Bug Export

Export all bugs to CSV for tracking:

```bash
# Create bugs.csv with all bug summaries
echo "ID,Status,Severity,Title,Date" > bugs.csv
for file in open/* in-progress/* fixed/* wont-fix/*; do
  # Parse bug file and append to CSV
  # (You can create a script for this)
done
```

Happy bug hunting!
