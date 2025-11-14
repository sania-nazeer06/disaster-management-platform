# 🚀 DISASTER MANAGEMENT APP - STARTUP GUIDE

## Quick Start (2 Steps!)

### Step 1: Start Backend Server (Flask)
```powershell
# Open Terminal 1 in VS Code
cd "c:\Users\sania\SIH\Backend Python\SEP"
python app.py
```

**Wait until you see:**
```
✓ Using SQLite database for development
 * Running on http://127.0.0.1:5000
 * Debugger is active!
```

### Step 2: Start Frontend (React)
```powershell
# Open Terminal 2 in VS Code
cd "c:\Users\sania\SIH\Backend Python\SEP\frontend"
npm start
```

**Wait until you see:**
```
Compiled successfully!
Local: http://localhost:3000
```

---

## ✅ Verify Everything is Working

### Test 1: Backend API
Open browser: http://localhost:5000/safe_zones
**Expected:** JSON array with 49 safe zones

### Test 2: Frontend
Open browser: http://localhost:3000
**Expected:** Login page loads

### Test 3: Registration
1. Click "Create Account"
2. Fill in details:
   - Name: Test Faculty
   - Email: faculty1@test.com
   - Password: password123
   - Role: Faculty
3. Click "Register"
**Expected:** Redirected to login page with success message

### Test 4: Login
1. Email: faculty1@test.com
2. Password: password123
3. Click "Login"
**Expected:** Dashboard loads with welcome message

---

## 🐛 Troubleshooting

### Problem: "Registration failed"
**Solution:**
1. Check if Flask server is running (Terminal 1)
2. Verify URL in browser dev tools: should call http://localhost:5000/auth/register
3. Check Flask terminal for error messages

### Problem: "Emergency contacts not loading"
**Cause:** Flask server not running
**Solution:**
```powershell
# In Terminal 1
python app.py
```

### Problem: "Safe zones showing 0"
**Solution:**
```powershell
# Delete database and restart
Remove-Item instance\disaster_app.db -Force
python app.py
```
The server will recreate DB with 49 safe zones automatically.

### Problem: "Loading..." never finishes
**Cause:** React can't reach Flask server
**Check:**
1. Flask running on port 5000? → `python app.py`
2. React running on port 3000? → `npm start`
3. Check browser console (F12) for CORS errors

### Problem: Port 3000 already in use
**Solution:**
```powershell
# Kill existing React process
Get-Process node | Stop-Process -Force
npm start
```

### Problem: Port 5000 already in use
**Solution:**
```powershell
# Kill existing Flask process
Get-Process python | Where-Object {$_.Path -like '*SEP*'} | Stop-Process -Force
python app.py
```

---

## 📊 Database Status

**Type:** SQLite (Local file)
**Location:** `instance/disaster_app.db`
**Status:** Auto-created on first run

**Seeded Data:**
- ✅ 49 Safe Zones (all Indian states)
- ✅ 5 Emergency Contacts
- ⏳ 0 Users (register to create)
- ⏳ 0 Modules (faculty creates via UI)

**To Reset Database:**
```powershell
Remove-Item instance\disaster_app.db -Force
python app.py
```

---

## 🎯 First-Time Usage Flow

### For Faculty:
1. Register → Role: Faculty
2. Login
3. Go to "Manage Content"
4. Create Module with quiz (use JSON format from FACULTY_QUIZ_GUIDE.md)
5. Students can now take your quiz!

### For Students:
1. Register → Role: Student
2. Login  
3. Explore Safe Zones (mark favorites)
4. Take Modules/Quizzes
5. View Progress
6. Earn points!

---

## 🔧 Enhanced Features (Just Added!)

### Better Error Messages
- ✅ "Cannot connect to server" instead of generic errors
- ✅ Retry buttons on failed requests
- ✅ Loading indicators on all pages
- ✅ Clear error displays with solutions

### Improved UX
- ✅ Safe zone count displayed: "All Safe Zones (49)"
- ✅ Loading states prevent laggy feel
- ✅ Error boundaries catch crashes
- ✅ Logout button visible in Navbar
- ✅ Empty states show helpful messages

---

## 📁 Project Structure

```
SEP/
├── app.py                    # Flask backend (START THIS FIRST!)
├── models.py                 # Database models
├── instance/
│   └── disaster_app.db      # SQLite database (auto-created)
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.js      # Main dashboard (enhanced!)
│   │   │   ├── SafeZones.js      # Map with 49 zones (enhanced!)
│   │   │   ├── Register.js       # Registration (better errors!)
│   │   │   ├── Login.js          # Login (better errors!)
│   │   │   ├── Modules.js        # Quiz system
│   │   │   └── ManageContent.js  # Faculty content creation
│   │   ├── components/
│   │   │   └── Navbar.js         # Navigation with logout
│   │   └── services/
│   │       └── api.js            # API client
│   └── package.json
├── DATABASE_SUMMARY.md       # Complete DB documentation
└── FACULTY_QUIZ_GUIDE.md     # How to create quizzes

```

---

## 🌐 API Endpoints (All Working!)

### Auth
- POST /auth/register - Create account
- POST /auth/login - Sign in

### Safe Zones
- GET /safe_zones - List all 49 zones
- POST /safe_zones/:id/mark - Mark as favorite
- GET /safe_zones/marked - Get user's marked zones

### Modules
- GET /modules - List all quizzes
- POST /modules - Create quiz (faculty only)
- POST /modules/:id/attempt - Submit quiz answers

### Emergency Contacts
- GET /emergency-contacts - List all contacts

### Progress
- GET /progress/user/:id - Get student progress
- POST /progress - Update progress

---

## ✨ What's Fixed

1. ✅ **Registration Error** - Better error messages guide users
2. ✅ **Logout Button** - Always visible in Navbar
3. ✅ **Emergency Contacts Loading** - Error handling + retry button
4. ✅ **Safe Zones Reset** - Fresh DB with all 49 zones
5. ✅ **Loading Lag** - Proper loading states prevent confusion
6. ✅ **Error Messages** - Clear, actionable error messages

---

## 📞 Support

**If you see errors:**
1. Check both terminals (Flask + React)
2. Read error messages carefully
3. Try the troubleshooting steps above
4. Check browser console (F12) for frontend errors

**Common Success Indicators:**
- Flask: "✓ Seeded 49 region-wise safe zones across India"
- React: "Compiled successfully!"
- Browser: Pages load without "Loading..." stuck

---

## 🎓 Faculty Quiz Creation

See `FACULTY_QUIZ_GUIDE.md` for complete instructions on creating quizzes in the correct JSON format.

**Quick Example:**
```json
[
  {
    "question": "What to do during earthquake?",
    "options": ["Run outside", "Drop, Cover, Hold On", "Use elevator"],
    "correctIndex": 1
  }
]
```

---

**Your app is ready! Start both servers and begin using the platform! 🚀**
