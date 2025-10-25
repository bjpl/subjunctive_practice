# Quick Start Guide - User Testing

**Ready to start testing in 15 minutes? Follow this guide.**

---

## ⚡ Super Quick Setup (15 minutes)

### Step 1: Start Backend (5 min)

```bash
# Terminal 1 - Backend
cd backend

# Activate virtual environment (create if needed)
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies (first time only)
pip install -r requirements.txt

# Quick setup with SQLite (no PostgreSQL needed for testing)
cat > .env << EOL
APP_NAME=Spanish Subjunctive Practice
ENVIRONMENT=development
DEBUG=true
SECRET_KEY=your-super-secret-key-change-in-production-$(openssl rand -hex 32)
DATABASE_URL=sqlite:///./test.db
CORS_ORIGINS=http://localhost:3000
EOL

# Initialize database
python scripts/init_db.py

# Start server
uvicorn main:app --reload --port 8000
```

✅ Backend running at `http://localhost:8000`
✅ API docs at `http://localhost:8000/api/docs`

### Step 2: Start Frontend (5 min)

```bash
# Terminal 2 - Frontend
cd frontend

# Install dependencies (first time only)
npm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start development server
npm run dev
```

✅ Frontend running at `http://localhost:3000`

### Step 3: Start Testing! (5 min)

1. Open browser to `http://localhost:3000`
2. Create test account
3. Complete one practice exercise
4. Check dashboard

**You're now ready for full testing!**

---

## 🎯 Your First Testing Session (30 min)

### Session 1: New User Journey

**Time**: 30 minutes
**Goal**: Experience the app as a brand new user

**Quick Checklist**:
- [ ] Register new account
- [ ] Complete 5 practice exercises
- [ ] View dashboard statistics
- [ ] Change one setting
- [ ] Logout and login again
- [ ] Document any issues found

**What to Look For**:
- Is registration clear and easy?
- Do exercises make sense?
- Is feedback helpful?
- Does progress tracking work?
- Any errors in browser console?

---

## 📱 Critical Test Points

Test these **must-work** features first:

### 1. Authentication (10 min)
```
✓ Can register
✓ Can login
✓ Can logout
✓ Session persists on refresh
```

### 2. Practice Flow (15 min)
```
✓ Can start practice
✓ Can submit answers
✓ Feedback shows correctly
✓ Session completes
✓ XP awarded
```

### 3. Progress Tracking (5 min)
```
✓ Dashboard shows stats
✓ Level/XP updates
✓ Accuracy calculates
```

---

## 🐛 Reporting Bugs Fast

When you find an issue:

**Quick Bug Template**:
```
WHAT: [One-line description]
WHEN: [What were you doing?]
EXPECTED: [What should happen?]
ACTUAL: [What actually happened?]
ERROR: [Any console errors?]
```

**Example**:
```
WHAT: Submit button doesn't work
WHEN: Completing second exercise
EXPECTED: Answer submits, shows feedback
ACTUAL: Button click does nothing
ERROR: TypeError: Cannot read property 'validate'
```

Save to: `docs/testing/bugs/open/BUG-001-[description].md`

---

## 🔧 Troubleshooting Quick Fixes

### Backend won't start
```bash
# Check if port 8000 in use
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or use different port
uvicorn main:app --reload --port 8001
```

### Frontend won't start
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check if port 3000 in use
npm run dev -- -p 3001
```

### Database errors
```bash
# Reset database
rm test.db  # (or delete SQLite file)
python scripts/init_db.py
```

### CORS errors
```bash
# Ensure .env has:
CORS_ORIGINS=http://localhost:3000

# Restart backend after changing .env
```

---

## 📚 Testing Resources at a Glance

**Full Guides**:
- `USER_TESTING_GUIDE.md` - Complete testing methodology
- `TEST_SCENARIOS.md` - 9 detailed user scenarios
- `TESTING_CHECKLIST.md` - 93-point comprehensive checklist
- `BUG_REPORT_TEMPLATE.md` - Detailed bug documentation

**Start Here**:
1. This file (QUICK_START.md) ← You are here
2. Complete Scenario 1 from TEST_SCENARIOS.md
3. Use TESTING_CHECKLIST.md to track coverage

---

## 🎪 Test Accounts to Create

Create these accounts for different test scenarios:

| Email | Role | Purpose |
|-------|------|---------|
| new@test.com | New user | Fresh experience, 0 progress |
| beginner@test.com | Beginner | 1-2 sessions, Level 2 |
| active@test.com | Active | 10+ sessions, Level 5 |
| advanced@test.com | Advanced | High level, many achievements |

---

## 📊 Testing Checklist - Essential Only

**Phase 1: Does it work?** (30 min)
- [ ] Register ✓
- [ ] Login ✓
- [ ] Practice (5 exercises) ✓
- [ ] Dashboard shows progress ✓
- [ ] Logout ✓

**Phase 2: Does it work well?** (30 min)
- [ ] Mobile view ✓
- [ ] Settings save ✓
- [ ] Achievements unlock ✓
- [ ] Error handling ✓

**Phase 3: Edge cases** (30 min)
- [ ] Invalid inputs handled ✓
- [ ] Network errors graceful ✓
- [ ] Keyboard navigation ✓

---

## ⏱️ Time-Boxed Testing Plans

### 30-Minute Quick Test
1. Register + Login (5 min)
2. Complete practice session (15 min)
3. Explore dashboard (5 min)
4. Document findings (5 min)

### 1-Hour Standard Test
1. New user scenario from TEST_SCENARIOS.md (30 min)
2. Mobile testing (15 min)
3. Settings testing (10 min)
4. Document bugs (5 min)

### 2-Hour Comprehensive Test
1. Two full scenarios (60 min)
2. Accessibility testing (30 min)
3. Edge cases (20 min)
4. Document and prioritize bugs (10 min)

---

## 🚦 What to Test First (Priority Order)

**🔴 Critical - Test First**
1. Login/Register
2. Practice exercise flow
3. Progress saving

**🟡 Important - Test Second**
4. Dashboard stats
5. Mobile view
6. Settings

**🟢 Nice to Have - Test Third**
7. Achievements
8. Advanced analytics
9. Accessibility features

---

## 💡 Pro Tips

1. **Keep Console Open**: Catch errors immediately
2. **Test on Real Mobile**: Emulators miss touch issues
3. **Document As You Go**: Don't wait until end of session
4. **Try to Break It**: Don't just follow happy paths
5. **Fresh Browser**: Use incognito to test new user experience
6. **Screenshot Everything**: Visual proof is valuable
7. **Note Even Small Issues**: Polish matters

---

## 📈 Track Your Progress

**Testing Session Log**:
```
Session 1: [Date] - 30min - Auth & Practice - 2 bugs found ✓
Session 2: [Date] - 45min - Mobile view - 1 bug found ✓
Session 3: [Date] - 30min - Settings - 0 bugs ✓
```

**Coverage Tracker**:
```
Authentication:     ████████░░ 80%
Practice Flow:      ██████░░░░ 60%
Dashboard:          ████░░░░░░ 40%
Mobile:             ██░░░░░░░░ 20%
Accessibility:      ░░░░░░░░░░  0%
```

---

## ✅ Ready to Go!

**You now have**:
✓ Backend running
✓ Frontend running
✓ Test account created
✓ Bug reporting template
✓ Testing plan

**Next steps**:
1. Open `http://localhost:3000`
2. Follow "Session 1: New User Journey" above
3. Document any issues in `docs/testing/bugs/`
4. After first session, move to TEST_SCENARIOS.md

**Happy Testing! 🚀**

---

## 🆘 Need Help?

- Backend not working? Check `/backend/README.md`
- Frontend issues? Check `/frontend/README.md`
- Database problems? Check `/docs/database/`
- General setup? Check `/docs/development/SETUP.md`

**Remember**: Every bug you find makes the app better!
