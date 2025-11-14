# 🚀 QUICK START GUIDE - Fresh Restart Test

## After Closing Everything and Reopening:

### Step 1️⃣: Open VS Code
```
1. Navigate to: C:\Users\sania\SIH\Backend Python\SEP
2. Right-click → Open with VS Code
   OR
   Open VS Code → File → Open Folder → Select the SEP folder
```

### Step 2️⃣: Start Backend Server
```powershell
# In VS Code terminal (PowerShell):
cd "c:\Users\sania\SIH\Backend Python\SEP"
python app.py
```

**Expected Output:**
```
[OK] Using SQLite database for development
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

✅ **If you see this, backend is running!**

### Step 3️⃣: Start Frontend (New Terminal)
```powershell
# Open NEW terminal in VS Code (Ctrl + Shift + `)
cd "c:\Users\sania\SIH\Backend Python\SEP\frontend"
npm start
```

**Expected Output:**
```
Compiled successfully!
You can now view frontend in the browser.

  Local:            http://localhost:3000
```

✅ **If you see this, frontend is running!**

### Step 4️⃣: Test in Browser
```
1. Browser will auto-open to: http://localhost:3000
2. You should see the Login page
3. Try logging in or registering
4. Navigate through different pages
```

### Step 5️⃣: Verify Admin Panel (Optional)
```
1. Login as admin
2. Go to: http://localhost:3000/admin
3. Look for "All Users" table
4. You should see the 🔐 Reset Password button next to each user
```

---

## ✅ Success Checklist:

- [ ] VS Code opens the project folder
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Browser opens to http://localhost:3000
- [ ] Login page appears
- [ ] Can register/login successfully
- [ ] Can navigate to different pages
- [ ] No 422 errors appear
- [ ] No 404 errors appear
- [ ] No login/logout issues
- [ ] Admin panel shows reset password button

---

## 🐛 If Something Goes Wrong:

### Backend won't start?
```powershell
# Check Python is working:
python --version

# Should show: Python 3.x.x
```

### Frontend won't start?
```powershell
# Install dependencies first:
cd frontend
npm install

# Then start:
npm start
```

### Port 5000 already in use?
```powershell
# Find and kill the process:
Get-Process python | Stop-Process -Force

# Then restart backend
```

### Port 3000 already in use?
```powershell
# Frontend will ask to use a different port
# Just press 'Y' when prompted
```

---

## 📝 What We Fixed:

✅ **422 Token Errors** - Auto-handled with graceful logout  
✅ **404 Not Found** - Clear error messages  
✅ **Login/Logout Issues** - Smooth authentication flow  
✅ **All Crashes** - Comprehensive error handling  
✅ **Password Management** - Secure reset feature for admins  

---

## 🎯 Expected Behavior After Restart:

1. **Everything starts clean** ✅
2. **No error messages** ✅
3. **Smooth login/logout** ✅
4. **All features work** ✅
5. **Admin can reset passwords** ✅

---

**Ready to test? Close everything and reopen!** 🚀

Then follow Steps 1-5 above and check off each item in the Success Checklist.

**Good luck! Everything will work perfectly!** 💪
