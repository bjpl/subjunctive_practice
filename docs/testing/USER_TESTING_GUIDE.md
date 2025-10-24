# User Testing Guide - Spanish Subjunctive Practice App

## Overview
This guide will help you systematically test the Spanish Subjunctive Practice application to identify bugs, usability issues, and areas for improvement.

## Pre-Testing Setup

### 1. Environment Setup

#### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment (if not exists)
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and configure:
# - DATABASE_URL (can use SQLite for testing: sqlite:///./test.db)
# - SECRET_KEY (generate a random string)
# - ANTHROPIC_API_KEY (optional, for AI features)

# Initialize database
python scripts/init_db.py

# Run backend server
uvicorn main:app --reload --port 8000
```

Backend will be available at: `http://localhost:8000`
API docs at: `http://localhost:8000/api/docs`

#### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local and set:
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Run frontend development server
npm run dev
```

Frontend will be available at: `http://localhost:3000`

### 2. Create Test Accounts

Create multiple test accounts to simulate different user scenarios:
- **New User**: Fresh account with no progress
- **Beginner User**: Account with 1-2 completed sessions
- **Active User**: Account with 10+ sessions, some achievements
- **Advanced User**: Account with high level, many achievements

### 3. Testing Tools Setup

#### Browser DevTools
- Keep browser console open to catch JavaScript errors
- Use Network tab to monitor API calls
- Test in multiple browsers: Chrome, Firefox, Safari, Edge

#### Mobile Testing
- Use browser DevTools device emulation
- Test on actual mobile devices if available
- Test in both portrait and landscape orientations

#### Accessibility Testing
- Install browser extension: WAVE or axe DevTools
- Test keyboard navigation (no mouse)
- Test with screen reader if possible

### 4. Testing Environment Checklist

Before starting, verify:
- [ ] Backend server running without errors
- [ ] Frontend server running without errors
- [ ] Database initialized with seed data
- [ ] API docs accessible at /api/docs
- [ ] Browser console open
- [ ] Network monitoring enabled
- [ ] Test accounts created

## Testing Methodology

### Testing Approach
1. **Exploratory Testing**: Navigate freely, try different combinations
2. **Scenario-Based Testing**: Follow specific user scenarios (see TEST_SCENARIOS.md)
3. **Regression Testing**: Re-test areas after finding bugs
4. **Edge Case Testing**: Try unusual inputs, boundary conditions
5. **Performance Testing**: Note slow loading, lag, or freezes

### What to Look For

#### Functionality Issues
- Features not working as expected
- Error messages appearing unexpectedly
- Data not saving or loading correctly
- Incorrect calculations (XP, accuracy, etc.)

#### Usability Issues
- Confusing navigation or UI
- Unclear instructions or labels
- Difficulty finding features
- Frustrating workflows

#### Visual Issues
- Layout problems (overlapping, misaligned elements)
- Text too small or hard to read
- Colors with poor contrast
- Responsive design issues on different screen sizes

#### Performance Issues
- Slow page loads (>3 seconds)
- Laggy interactions
- Browser freezes or crashes
- High memory usage

#### Accessibility Issues
- Cannot navigate with keyboard only
- Screen reader issues
- Missing alt text on images
- Insufficient color contrast

## Testing Workflow

### Session Structure
Each testing session should be 30-60 minutes focused on specific areas.

**Session Template:**
1. **Warm-up** (5 min): Quick navigation through app
2. **Focused Testing** (40 min): Work through specific scenarios
3. **Exploratory** (10 min): Try unexpected things
4. **Documentation** (5 min): Record findings immediately

### Recording Findings

For each issue found, document:
1. **What happened**: Describe the issue
2. **Expected behavior**: What should have happened
3. **Steps to reproduce**: Exact steps to recreate issue
4. **Severity**: Critical / High / Medium / Low
5. **Screenshots/Videos**: Visual proof when relevant
6. **Environment**: Browser, device, OS

Use the BUG_REPORT_TEMPLATE.md for consistent documentation.

## Feature Testing Priority

### Priority 1 - Core Functionality (Must Work)
- User registration and login
- Exercise loading and display
- Answer submission and validation
- Progress tracking and XP calculation
- Session completion

### Priority 2 - Key Features (Should Work Well)
- Dashboard statistics and charts
- Achievement system
- Streak tracking
- Settings management
- Password reset

### Priority 3 - Enhanced Features (Nice to Have)
- AI-powered feedback (if Claude API configured)
- Advanced analytics
- Notifications
- Theme switching
- Export functionality

## Browser Testing Matrix

Test in these environments (prioritize based on your target users):

| Browser | Desktop | Mobile | Priority |
|---------|---------|---------|----------|
| Chrome | ✓ | ✓ | High |
| Firefox | ✓ | - | Medium |
| Safari | ✓ | ✓ | High |
| Edge | ✓ | - | Low |
| Mobile Chrome | - | ✓ | High |
| Mobile Safari | - | ✓ | High |

## Common Testing Pitfalls to Avoid

1. **Testing Too Fast**: Take time to observe behavior
2. **Skipping Error States**: Test with invalid inputs
3. **Ignoring Console**: Always check for JavaScript errors
4. **Testing Only Happy Paths**: Try to break things
5. **Not Documenting Immediately**: Write down issues as you find them
6. **Testing While Logged In Only**: Test logged-out experience too
7. **Using Only One Account**: Test with different user states
8. **Ignoring Mobile**: Mobile users are critical

## Daily Testing Routine

### Quick Daily Checks (15 min)
- [ ] Login/logout works
- [ ] Complete one practice exercise
- [ ] Check dashboard loads correctly
- [ ] Verify no console errors
- [ ] Test one new feature or area

### Weekly Deep Dives (1-2 hours)
- [ ] Complete full user journey scenarios
- [ ] Test in different browsers
- [ ] Mobile device testing
- [ ] Accessibility audit
- [ ] Review and triage all bugs found

## Tracking Progress

Keep a testing log with:
- Date and time
- Areas tested
- Issues found (with IDs/links)
- Time spent
- Coverage achieved

Example:
```
2025-10-24 | 45 min | Authentication Flow | 3 bugs found | Chrome Desktop
2025-10-24 | 30 min | Practice Session | 1 usability issue | Mobile Safari
```

## When to Stop Testing

You've achieved good coverage when:
- All Priority 1 features tested on primary browser
- All Priority 2 features tested at least once
- Mobile experience tested on actual devices
- Keyboard navigation tested
- At least 3 different user scenarios completed
- No critical bugs remain unfixed

## Getting Help

If you encounter setup issues:
1. Check logs in terminal where backend/frontend running
2. Review `/docs/troubleshooting/` documentation
3. Check `/docs/development/SETUP.md`
4. Verify all environment variables are set correctly

## Next Steps

1. Read through TESTING_CHECKLIST.md
2. Review TEST_SCENARIOS.md for guided test cases
3. Set up your testing environment
4. Start with Scenario 1: New User Registration
5. Document findings using BUG_REPORT_TEMPLATE.md

Happy testing!
