# Bug Report Template

Use this template to document bugs and issues found during user testing. Copy this template for each new bug.

---

## Bug ID: [BUG-001]

**Date Found**: 2025-10-24
**Found By**: [Your Name]
**Status**: 🔴 Open | 🟡 In Progress | 🟢 Fixed | ⚫ Won't Fix

---

## Summary
[One-line description of the issue]

**Example**: Submit button remains disabled after entering valid answer

---

## Severity

**Priority**: 🔴 Critical | 🟠 High | 🟡 Medium | 🟢 Low

### Severity Guidelines:
- **🔴 Critical**: App is broken, data loss, security vulnerability
- **🟠 High**: Major feature doesn't work, significant usability issue
- **🟡 Medium**: Minor feature broken, workaround available
- **🟢 Low**: Cosmetic issue, minor inconvenience

**Impact**: [How many users affected? How often does this happen?]

---

## Environment

**Browser**: Chrome 120.0 / Firefox 121.0 / Safari 17.0 / Edge 120.0
**OS**: Windows 11 / macOS 14 / Linux Ubuntu 22.04
**Device**: Desktop / Mobile / Tablet
**Screen Size**: 1920x1080 / 375x667 / etc.
**Network**: WiFi / 3G / 4G

**App Version**:
- Frontend: [check package.json version]
- Backend: [check from /health endpoint]

---

## Steps to Reproduce

1. [First step with exact details]
2. [Second step]
3. [Third step]
4. [Continue...]

**Example**:
1. Login with test account (test@example.com)
2. Navigate to Practice page
3. Click "Start Practice"
4. Complete first exercise correctly
5. Click submit button
6. Observe that button stays in disabled state

---

## Expected Behavior

[What should happen?]

**Example**: Button should submit the answer, show feedback, and enable navigation to the next exercise.

---

## Actual Behavior

[What actually happens?]

**Example**: Button remains grayed out and clicking has no effect. Console shows error: "Cannot read property 'validate' of undefined"

---

## Visual Evidence

### Screenshots
- [ ] Screenshot attached: `screenshots/bug-001-screenshot.png`
- [ ] Video recording attached: `recordings/bug-001-video.mp4`
- [ ] Console errors captured: `logs/bug-001-console.txt`

**Screenshot Guidelines**:
- Capture full browser window
- Include address bar showing URL
- Circle or annotate issue if not obvious
- Include console if errors present

---

## Console Errors

```
[Paste any console errors here]

Example:
Uncaught TypeError: Cannot read properties of undefined (reading 'validate')
    at handleSubmit (ExerciseForm.tsx:45)
    at onClick (Button.tsx:12)
```

---

## Network Activity

**Failed Requests**:
- [ ] No network issues
- [ ] Request URL: [e.g., POST /api/exercises/submit]
- [ ] Status Code: [e.g., 500, 404]
- [ ] Response: [error message]

---

## Additional Context

**User Flow**: [Where in the user journey did this occur?]
**Data State**: [Relevant user data, session info, etc.]
**Workaround**: [Is there a way to work around this?]
**First Occurrence**: [First time seeing this or happens repeatedly?]
**Related Issues**: [Links to similar bugs if any]

---

## Debugging Information

### For Developers

**Suspected Cause**: [Your hypothesis about what's causing this]

**Affected Components**:
- Frontend: [e.g., src/components/practice/ExerciseForm.tsx:45]
- Backend: [e.g., api/routes/exercises.py:123]
- Database: [e.g., exercises table]

**Possible Solutions**: [Ideas for fixing]

---

## Testing Notes

**Reproducibility**:
- [ ] Happens every time
- [ ] Happens sometimes (intermittent)
- [ ] Happened once (cannot reproduce)

**Tested Workarounds**:
- [ ] Refreshing page
- [ ] Logging out and back in
- [ ] Clearing cache
- [ ] Different browser
- [ ] Different account

**Results**: [What happened when you tried workarounds?]

---

## Resolution

**Fixed In Version**: [Version number when fixed]
**Fix Description**: [How was it fixed?]
**Verified By**: [Who verified the fix?]
**Verification Date**: [Date tested]
**Regression Test**: [Did you re-test to ensure it's fixed?]

---

## Example Bug Reports

### Example 1: Critical Bug

```
Bug ID: BUG-001
Date Found: 2025-10-24
Status: 🔴 Open

Summary: User progress lost after logout

Severity: 🔴 Critical
Impact: All users affected, data loss occurs

Environment:
- Browser: Chrome 120.0
- OS: macOS 14
- Device: Desktop

Steps to Reproduce:
1. Login as new user
2. Complete 5 practice exercises
3. Verify XP shows on dashboard (e.g., 500 XP)
4. Logout
5. Login again
6. Check dashboard

Expected: Progress shows 500 XP and 5 exercises completed
Actual: Progress reset to 0 XP, 0 exercises

Console Errors:
POST /api/progress 500 Internal Server Error
{"detail": "User not found"}

Suspected Cause: Session not persisting user_id correctly
```

### Example 2: Medium Bug

```
Bug ID: BUG-012
Date Found: 2025-10-24
Status: 🟡 Open

Summary: Chart tooltip cuts off on mobile

Severity: 🟡 Medium
Impact: Mobile users only, doesn't prevent usage

Environment:
- Browser: Safari iOS 17
- Device: iPhone 12
- Screen: 375x667

Steps to Reproduce:
1. Login on mobile device
2. Navigate to Dashboard
3. Tap on accuracy chart
4. Observe tooltip

Expected: Full tooltip visible within viewport
Actual: Tooltip extends beyond screen edge, partially hidden

Workaround: Rotate to landscape to see full tooltip

Suspected Cause: Chart library (Recharts) not responsive
Component: src/components/dashboard/AccuracyChart.tsx
```

### Example 3: Low Priority Bug

```
Bug ID: BUG-023
Date Found: 2025-10-24
Status: 🟢 Open

Summary: Button hover color slightly off-brand

Severity: 🟢 Low
Impact: Visual inconsistency only

Environment: All browsers

Expected: Button hover color should be #3B82F6 (primary-600)
Actual: Button hover color is #2563EB (primary-700)

Component: src/components/ui/Button.tsx:23
Fix: Update Tailwind class from hover:bg-primary-700 to hover:bg-primary-600
```

---

## Bug Tracking Sheet

Maintain a simple spreadsheet or markdown table to track all bugs:

| ID | Date | Summary | Severity | Status | Assigned | Fixed In |
|----|------|---------|----------|--------|----------|----------|
| BUG-001 | 10/24 | Progress lost on logout | 🔴 Critical | 🔴 Open | - | - |
| BUG-002 | 10/24 | Form validation missing | 🟠 High | 🟡 In Progress | Dev | - |
| BUG-003 | 10/24 | Tooltip cuts off mobile | 🟡 Medium | 🔴 Open | - | - |
| BUG-004 | 10/24 | Button color off-brand | 🟢 Low | 🟢 Fixed | - | v1.2.1 |

---

## Tips for Effective Bug Reporting

1. **Be Specific**: Vague reports are hard to fix
2. **One Bug Per Report**: Don't combine multiple issues
3. **Include Evidence**: Screenshots are worth a thousand words
4. **Test Reproducibility**: Can you make it happen again?
5. **Check for Duplicates**: Search existing bugs first
6. **Update Status**: Keep the status current
7. **Be Objective**: Report facts, not frustrations
8. **Include Workarounds**: Help other testers continue
9. **Follow Up**: Verify fixes when implemented
10. **Thank Developers**: Bug fixing is hard work!

---

## Folder Structure for Bug Documentation

```
docs/testing/bugs/
├── README.md (this file explains the system)
├── open/
│   ├── BUG-001-progress-lost.md
│   ├── BUG-002-form-validation.md
│   └── BUG-003-mobile-tooltip.md
├── in-progress/
│   └── BUG-002-form-validation.md
├── fixed/
│   ├── BUG-004-button-color.md
│   └── BUG-005-login-redirect.md
├── wont-fix/
│   └── BUG-010-edge-case.md
└── screenshots/
    ├── bug-001-screenshot.png
    ├── bug-002-screenshot.png
    └── bug-003-video.mp4
```

Move bugs between folders as their status changes.

---

Happy bug hunting! Remember: Every bug you find makes the app better!
