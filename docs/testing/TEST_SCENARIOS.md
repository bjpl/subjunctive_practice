# User Testing Scenarios

## How to Use This Document

Each scenario represents a realistic user journey through the application. Follow the steps exactly as written, noting any issues, confusion, or friction points along the way.

**For each scenario:**
1. Start with a fresh session (clear browser data or use incognito)
2. Follow steps sequentially
3. Note expected vs actual behavior
4. Document any issues immediately
5. Rate overall experience (1-5 stars)

---

## Scenario 1: New User First Experience

**User Profile**: Maria, 25, wants to improve Spanish for work
**Goal**: Create account and complete first practice session
**Estimated Time**: 15-20 minutes

### Steps:

1. **Navigate to app**
   - Open `http://localhost:3000`
   - Observe landing page
   - Expected: Clear value proposition, obvious CTA to get started

2. **Registration**
   - Click "Sign Up" or "Get Started"
   - Fill registration form:
     - Email: maria.test@example.com
     - Password: TestPass123!
     - Confirm password: TestPass123!
   - Submit form
   - Expected: Account created, redirected to dashboard or onboarding

3. **First Dashboard View**
   - Observe dashboard as new user
   - Expected:
     - Level 1, 0 XP
     - No exercises completed
     - Empty statistics
     - Clear next steps / CTA to start practicing

4. **Start First Practice Session**
   - Find and click "Start Practice" or similar button
   - Select difficulty (or accept default)
   - Expected: Clear difficulty descriptions, appropriate default

5. **Complete Exercise**
   - Read first exercise
   - Submit an answer (correct)
   - Expected:
     - Immediate feedback
     - Explanation of correct answer
     - XP awarded
     - Option to continue

6. **Try Incorrect Answer**
   - Continue to next exercise
   - Submit wrong answer
   - Expected:
     - Clear feedback on why it's wrong
     - Helpful explanation
     - Option to try again or see correct answer

7. **Finish Session**
   - Complete at least 5 exercises
   - Finish session
   - Expected:
     - Summary of performance
     - XP gained displayed
     - Level progress shown
     - Encouragement to continue

8. **Review Dashboard**
   - Return to dashboard
   - Expected:
     - Updated statistics
     - XP and level reflect session
     - Exercise count updated
     - Accuracy calculated correctly

### Success Criteria:
- [ ] Registration completed without confusion
- [ ] First exercise understood clearly
- [ ] Feedback was helpful and clear
- [ ] Progress tracking feels motivating
- [ ] User feels encouraged to return

### Questions to Consider:
- Was it clear what the app does?
- Was registration straightforward?
- Did you understand how to use the practice interface?
- Was the difficulty appropriate?
- Did you feel accomplished after the session?

---

## Scenario 2: Returning User Building Streak

**User Profile**: Carlos, 30, practicing daily for 2 weeks
**Goal**: Maintain streak and reach next level
**Estimated Time**: 20 minutes

### Steps:

1. **Login**
   - Navigate to app
   - Login with existing account
   - Expected: Immediate access to dashboard, session restored if applicable

2. **Review Progress**
   - Check dashboard statistics
   - Look for current streak
   - Check progress to next level
   - Expected: Clear display of streak, XP needed for level up

3. **Check Weak Areas**
   - Find weak areas or recommendations section
   - Expected: Identification of exercise types with lower accuracy

4. **Practice Session (Targeting Weakness)**
   - Start practice session
   - Select difficulty based on current level
   - Complete 10 exercises
   - Focus on recommended weak areas if possible
   - Expected: Mix of exercise types, appropriate difficulty

5. **Level Up (if applicable)**
   - Complete enough exercises to level up
   - Expected:
     - Celebration animation or notification
     - Level badge or achievement unlocked
     - Encouraging message

6. **Unlock Achievement**
   - Continue practicing until achievement unlocked (e.g., "10 in a row")
   - Expected:
     - Achievement notification
     - Badge displayed in achievements gallery
     - Progress toward next achievement shown

7. **Review Session Stats**
   - Check detailed statistics
   - Expected:
     - Accuracy by exercise type
     - Time spent
     - XP earned
     - Streak status updated

8. **Logout**
   - Logout from account
   - Expected: Clean logout, no data leaks

### Success Criteria:
- [ ] Streak tracking works correctly
- [ ] Level progression feels achievable
- [ ] Weak area identification is accurate
- [ ] Achievement system is motivating
- [ ] Statistics are accurate and meaningful

---

## Scenario 3: Mobile Learning Session

**User Profile**: Ana, 22, studying during commute on phone
**Goal**: Complete quick practice session on mobile
**Estimated Time**: 10 minutes

### Steps:

1. **Open on Mobile Device**
   - Navigate to app on mobile browser or use browser DevTools mobile emulation
   - Login
   - Expected: Responsive layout, readable text, easy navigation

2. **Navigate with Touch**
   - Explore dashboard using touch
   - Scroll through statistics
   - Expected: Smooth scrolling, appropriately sized touch targets

3. **Start Practice (Portrait Mode)**
   - Start practice session
   - Complete 3-5 exercises in portrait orientation
   - Expected:
     - Exercise text is readable
     - Input fields are easy to tap
     - Submit buttons are accessible
     - Keyboard doesn't obscure content

4. **Rotate to Landscape**
   - Rotate device to landscape
   - Continue practice
   - Expected: Layout adapts gracefully, no content cut off

5. **Test Keyboard**
   - Type answers using mobile keyboard
   - Expected:
     - Keyboard appears automatically for inputs
     - Special Spanish characters accessible
     - Form doesn't resize awkwardly

6. **Review Stats on Mobile**
   - Navigate to dashboard
   - View charts and statistics
   - Expected:
     - Charts render correctly
     - Interactive elements work with touch
     - Text is legible

### Success Criteria:
- [ ] All features accessible on mobile
- [ ] Touch targets are appropriately sized (min 44x44px)
- [ ] Text is readable without zooming
- [ ] Layout adapts to both orientations
- [ ] Keyboard interaction is smooth

---

## Scenario 4: Settings and Customization

**User Profile**: Luis, 35, wants to customize learning experience
**Goal**: Adjust settings and preferences
**Estimated Time**: 10 minutes

### Steps:

1. **Navigate to Settings**
   - Login
   - Find and click Settings/Profile
   - Expected: Easy to find, clear navigation

2. **Update Profile**
   - Change display name
   - Update email (if allowed)
   - Save changes
   - Expected: Validation, success confirmation, changes persist

3. **Adjust Practice Preferences**
   - Find practice settings
   - Change:
     - Default difficulty level
     - Session length
     - Notification preferences
   - Save changes
   - Expected: Clear options, changes take effect immediately

4. **Change Theme**
   - Toggle between light/dark mode (if available)
   - Expected: Theme switches smoothly, readable in both modes

5. **Change Password**
   - Navigate to password change
   - Enter current password
   - Enter new password
   - Confirm new password
   - Submit
   - Expected:
     - Validation (password strength)
     - Success message
     - Can login with new password

6. **Test Persistence**
   - Logout and login again
   - Check if settings persisted
   - Expected: All changes saved

### Success Criteria:
- [ ] All settings are discoverable
- [ ] Changes save correctly
- [ ] Validation prevents invalid inputs
- [ ] Password change works securely
- [ ] Settings persist across sessions

---

## Scenario 5: Intensive Practice Marathon

**User Profile**: Sofia, 28, preparing for exam, wants intensive practice
**Goal**: Complete multiple practice sessions in succession
**Estimated Time**: 30 minutes

### Steps:

1. **Login**
   - Start on dashboard
   - Note current XP and level

2. **Session 1 - Easy Level**
   - Complete 15 exercises at Easy difficulty
   - Note time taken
   - Check accuracy

3. **Session 2 - Medium Level**
   - Immediately start another session
   - Increase to Medium difficulty
   - Complete 15 exercises
   - Expected: Different exercises, no repeats

4. **Session 3 - Hard Level**
   - Continue to Hard difficulty
   - Complete 15 exercises
   - Expected: Noticeably more challenging

5. **Monitor Progress**
   - After each session, check:
     - XP accumulation
     - Accuracy trends
     - Level progress
     - Achievement unlocks
   - Expected: Accurate calculations, smooth progression

6. **Check for Fatigue/Errors**
   - Note any:
     - Performance degradation
     - Browser slowness
     - Memory issues
     - Repeated exercises

7. **Review Comprehensive Stats**
   - View overall statistics
   - Check charts for today's activity
   - Expected: All sessions recorded, accurate metrics

### Success Criteria:
- [ ] App handles multiple consecutive sessions
- [ ] No performance degradation
- [ ] Exercise variety maintained
- [ ] Accurate XP and progress tracking
- [ ] No memory leaks or slowdowns

---

## Scenario 6: Keyboard Navigation (Accessibility)

**User Profile**: Pedro, 40, prefers keyboard navigation
**Goal**: Complete full user journey using only keyboard
**Estimated Time**: 15 minutes

**Equipment**: Keyboard only, no mouse

### Steps:

1. **Navigate to Login**
   - Use Tab to navigate
   - Press Enter to activate links
   - Expected: Visible focus indicators, logical tab order

2. **Login Using Keyboard**
   - Tab through form fields
   - Type credentials
   - Submit with Enter or spacebar
   - Expected: Can complete entire form without mouse

3. **Dashboard Navigation**
   - Tab through dashboard elements
   - Access different sections using keyboard
   - Expected: All interactive elements reachable, skip links available

4. **Start Practice Session**
   - Navigate to practice button
   - Activate with keyboard
   - Expected: Practice interface accessible

5. **Complete Exercises with Keyboard**
   - Tab to input field
   - Type answer
   - Tab to submit button
   - Press Enter to submit
   - Navigate feedback
   - Continue to next exercise
   - Expected: Complete workflow possible without mouse

6. **Access Settings**
   - Navigate to settings
   - Change preferences
   - Save using keyboard
   - Expected: All settings adjustable via keyboard

7. **Logout**
   - Navigate to logout
   - Activate with keyboard
   - Expected: Clean logout

### Success Criteria:
- [ ] All functionality accessible via keyboard
- [ ] Focus indicators always visible
- [ ] Logical tab order throughout app
- [ ] No keyboard traps
- [ ] Can complete full user journey

---

## Scenario 7: Error Handling and Edge Cases

**User Profile**: Test user deliberately trying to break things
**Goal**: Test error handling and validation
**Estimated Time**: 20 minutes

### Steps:

1. **Invalid Registration**
   - Try registering with:
     - Invalid email format
     - Password too short
     - Mismatched password confirmation
     - Already existing email
   - Expected: Clear error messages, form validation

2. **Invalid Login**
   - Try logging in with:
     - Wrong password
     - Non-existent email
     - Empty fields
   - Expected: Appropriate error messages, no system errors revealed

3. **Network Simulation**
   - Open browser DevTools
   - Simulate slow 3G network
   - Try to complete practice session
   - Expected: Loading states shown, graceful handling

4. **Session Timeout**
   - Login
   - Wait for token to expire (or manually expire in DevTools)
   - Try to interact with app
   - Expected: Redirect to login with message, no data loss

5. **Rapid Clicking**
   - Click submit buttons multiple times rapidly
   - Expected: No duplicate submissions, loading states prevent multiple clicks

6. **Invalid Input in Exercises**
   - Submit empty answers
   - Submit very long strings
   - Submit special characters
   - Expected: Validation, helpful error messages

7. **Browser Back Button**
   - Complete exercise
   - Hit browser back button
   - Navigate forward again
   - Expected: State maintained, no errors

8. **Local Storage Clearing**
   - Clear browser local storage while logged in
   - Try to interact
   - Expected: Graceful handling, re-authentication if needed

### Success Criteria:
- [ ] All edge cases handled gracefully
- [ ] No uncaught errors in console
- [ ] Helpful error messages
- [ ] No data corruption
- [ ] App remains stable

---

## Scenario 8: Analytics and Progress Tracking

**User Profile**: Emma, 27, data-driven learner tracking progress
**Goal**: Use analytics to identify areas for improvement
**Estimated Time**: 15 minutes

### Steps:

1. **Login**
   - Access dashboard

2. **Review Overall Statistics**
   - Find overall accuracy percentage
   - Check total exercises completed
   - View current level and XP
   - Expected: Clear, accurate numbers

3. **Analyze Performance by Exercise Type**
   - Find breakdown by exercise type
   - Identify strongest and weakest types
   - Expected: Accurate percentages for each type

4. **Study Heatmap**
   - View study heatmap/calendar
   - Check consecutive days practiced
   - Expected: Accurate representation of practice days

5. **Review Recent Activity**
   - Check list of recent sessions
   - View details of past sessions
   - Expected: Chronological list, accurate session data

6. **Check Achievements Progress**
   - View achievements gallery
   - Check progress on incomplete achievements
   - Expected: Clear progress indicators, locked/unlocked states

7. **Identify Weak Areas**
   - Find weak areas or recommendations
   - Expected: Actionable suggestions based on data

8. **Test Data Accuracy**
   - Complete a new practice session
   - Return to dashboard
   - Verify all statistics updated correctly
   - Expected: Real-time or near-real-time updates

### Success Criteria:
- [ ] All statistics are accurate
- [ ] Charts render correctly
- [ ] Data visualizations are helpful
- [ ] Weak areas correctly identified
- [ ] Progress tracking motivates continued use

---

## Scenario 9: Multi-Device Sync

**User Profile**: Roberto, 32, uses app on phone and computer
**Goal**: Verify progress syncs across devices
**Estimated Time**: 15 minutes

### Steps:

1. **Device 1 (Desktop) - Initial Session**
   - Login on desktop browser
   - Complete 5 exercises
   - Note current XP, level, and exercises completed
   - Stay logged in

2. **Device 2 (Mobile) - Login**
   - Open app on mobile device or different browser
   - Login with same account
   - Expected: Dashboard shows same progress as desktop

3. **Device 2 - Practice Session**
   - Complete 5 more exercises on mobile
   - Note new XP and progress
   - Stay logged in

4. **Device 1 - Refresh**
   - Return to desktop
   - Refresh page
   - Expected: Progress from mobile session now visible

5. **Device 1 - Settings Change**
   - Change a preference in settings
   - Save

6. **Device 2 - Check Settings**
   - Navigate to settings on mobile
   - Expected: Setting change reflected

7. **Concurrent Usage**
   - Try to use both devices simultaneously
   - Expected: No conflicts, latest update wins

### Success Criteria:
- [ ] Progress syncs across devices
- [ ] Settings sync across devices
- [ ] No data loss
- [ ] Conflicts handled gracefully
- [ ] Real-time or near-real-time sync

---

## Post-Scenario Evaluation

After completing each scenario, rate the following (1-5 scale):

**Functionality**: Did everything work as expected?
**Usability**: Was it easy and intuitive to use?
**Performance**: Was the app fast and responsive?
**Visual Design**: Did it look good and professional?
**Overall Experience**: Would you recommend this app?

**Comments**: Any additional observations or feedback

---

## Creating Your Own Scenarios

As you test, you may want to create custom scenarios. Use this template:

**Scenario Name**: [Descriptive title]
**User Profile**: [Name, age, goal/motivation]
**Goal**: [What user wants to accomplish]
**Estimated Time**: [How long it should take]

**Steps**:
1. [First action]
   - Expected: [What should happen]
2. [Second action]
   - Expected: [What should happen]
[...]

**Success Criteria**:
- [ ] [Key metric 1]
- [ ] [Key metric 2]

---

## Tips for Effective Scenario Testing

1. **Take Your Time**: Don't rush through steps
2. **Think Aloud**: Verbalize your thought process as you go
3. **Note Confusion**: Any moment of "where do I click?" is worth noting
4. **Compare Expectations**: Always note if reality differs from expectations
5. **Screen Record**: Consider recording sessions for later review
6. **Fresh Perspective**: Take breaks between scenarios
7. **Document Immediately**: Write down issues as soon as you find them

Happy testing!
