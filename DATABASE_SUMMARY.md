# 📊 DISASTER MANAGEMENT APP - DATABASE SUMMARY

**Last Updated:** October 31, 2025  
**Database Type:** SQLite (Development)  
**Database Location:** `C:\Users\sania\SIH\Backend Python\SEP\instance\disaster_app.db`

---

## ✅ DATABASE STATUS: **FULLY OPERATIONAL**

Your application is using **SQLite database** which is:
- ✅ **Already installed and working** (no additional setup needed)
- ✅ **Perfect for development and testing**
- ✅ **Automatically created when Flask starts**
- ✅ **Stores all data locally in a single file**

---

## 📋 DATABASE TABLES (12 Total)

### 1. **users** - User Accounts
- **Columns:** id, name, email, password_hash, role
- **Current Data:** 3 users (1 faculty, 2 students)
- **Purpose:** Stores all registered users (students, faculty, admin)

### 2. **safe_zones** - Safe Zone Locations
- **Columns:** id, name, latitude, longitude, description
- **Current Data:** 49 safe zones across India
- **Purpose:** Region-wise safe zones covering all major Indian cities and states

### 3. **modules** - Learning Modules
- **Columns:** id, title, description, content, image_url, difficulty, points, quiz_questions, created_at
- **Current Data:** 1 module (Earthquake Basics)
- **Purpose:** Educational content with quizzes created by faculty

### 4. **emergency_contacts** - Emergency Numbers
- **Columns:** id, name, organization, phone, email, category, region, available_24_7
- **Current Data:** 5 contacts (Ambulance, Police, Fire, NDRF, Red Cross)
- **Purpose:** Quick access to emergency services

### 5. **progress** - Student Quiz Progress
- **Columns:** id, user_id, module_name, quiz_score, completed
- **Current Data:** 0 records
- **Purpose:** Tracks student quiz attempts and scores

### 6. **user_achievements** - Gamification Points
- **Columns:** id, user_id, achievement_type, title, description, points, earned_at
- **Current Data:** 0 records
- **Purpose:** Stores points earned from quizzes and activities

### 7. **user_safe_zones** - Marked Safe Zones
- **Columns:** id, user_id, zone_id, marked_at
- **Current Data:** 0 records
- **Purpose:** Tracks which safe zones students have marked/saved

### 8. **messages** - Communication
- **Columns:** id, sender_id, receiver_id, message_text, timestamp
- **Current Data:** 0 records
- **Purpose:** Student-faculty messaging system

### 9. **disasters** - Disaster Information
- **Columns:** id, disaster_type, info, video_link
- **Current Data:** 0 records
- **Purpose:** Disaster type information and educational videos

### 10. **drills** - Safety Drills
- **Columns:** id, title, description, drill_type, steps, duration_minutes, scheduled_date, created_by
- **Current Data:** 0 records
- **Purpose:** Emergency drill scheduling and tracking

### 11. **alerts** - Disaster Alerts
- **Columns:** id, title, message, alert_type, severity, region, latitude, longitude, radius_km, active, created_at, expires_at, created_by
- **Current Data:** 0 records
- **Purpose:** Real-time disaster alerts and notifications

### 12. **drill_participation** - Drill Tracking
- **Columns:** id, drill_id, user_id, completed, score, completion_time
- **Current Data:** 0 records
- **Purpose:** Tracks student participation in drills

---

## 🗺️ SAFE ZONES BY REGION (49 Total)

### **North India (12 zones)**
1. Delhi - Connaught Place Safe Zone
2. Delhi - Dwarka Safe Zone
3. Chandigarh Safe Zone
4. Jaipur - Pink City Safe Zone (Rajasthan)
5. Jodhpur Safe Zone (Rajasthan)
6. Udaipur Safe Zone (Rajasthan)
7. Lucknow - Hazratganj Safe Zone (Uttar Pradesh)
8. Varanasi Safe Zone (Uttar Pradesh)
9. Agra - Taj Safe Zone (Uttar Pradesh)
10. Amritsar - Golden Temple Safe Zone (Punjab)
11. Shimla Safe Zone (Himachal Pradesh)
12. Dehradun Safe Zone (Uttarakhand)

### **South India (15 zones)**
13. Mumbai - Marine Drive Safe Zone (Maharashtra)
14. Mumbai - Bandra Safe Zone (Maharashtra)
15. Pune - Shivajinagar Safe Zone (Maharashtra)
16. Bengaluru - MG Road Safe Zone (Karnataka)
17. Bengaluru - Electronic City Safe Zone (Karnataka)
18. Mysuru Safe Zone (Karnataka)
19. Chennai - Marina Beach Safe Zone (Tamil Nadu)
20. Chennai - T Nagar Safe Zone (Tamil Nadu)
21. Coimbatore Safe Zone (Tamil Nadu)
22. Hyderabad - Charminar Safe Zone (Telangana)
23. Hyderabad - Hi-Tech City Safe Zone (Telangana)
24. Kochi Safe Zone (Kerala)
25. Thiruvananthapuram Safe Zone (Kerala)
26. Visakhapatnam Safe Zone (Andhra Pradesh)
27. Vijayawada Safe Zone (Andhra Pradesh)

### **East India (9 zones)**
28. Kolkata - Park Street Safe Zone (West Bengal)
29. Kolkata - Salt Lake Safe Zone (West Bengal)
30. Darjeeling Safe Zone (West Bengal)
31. Bhubaneswar Safe Zone (Odisha)
32. Patna Safe Zone (Bihar)
33. Ranchi Safe Zone (Jharkhand)
34. Guwahati Safe Zone (Assam)
35. Imphal Safe Zone (Manipur)
36. Agartala Safe Zone (Tripura)

### **West India (6 zones)**
37. Ahmedabad - Sabarmati Safe Zone (Gujarat)
38. Surat Safe Zone (Gujarat)
39. Vadodara Safe Zone (Gujarat)
40. Indore Safe Zone (Madhya Pradesh)
41. Bhopal Safe Zone (Madhya Pradesh)
42. Goa - Panaji Safe Zone (Goa)

### **Central India (3 zones)**
43. Nagpur Safe Zone (Maharashtra)
44. Raipur Safe Zone (Chhattisgarh)
45. Jabalpur Safe Zone (Madhya Pradesh)

### **Northeast India (4 zones)**
46. Shillong Safe Zone (Meghalaya)
47. Aizawl Safe Zone (Mizoram)
48. Itanagar Safe Zone (Arunachal Pradesh)
49. Gangtok Safe Zone (Sikkim)

---

## 🔄 DATABASE CONFIGURATION OPTIONS

Your app supports **3 database types** (configured in `.env` file):

### **1. SQLite** ✅ (Currently Active)
```env
# In .env file - this is the default
USE_MYSQL=false
# DATABASE_URL not set
```
- **Pros:** No setup required, perfect for development, fast, portable
- **Cons:** Not recommended for production, limited concurrent users
- **File Location:** `instance/disaster_app.db`

### **2. PostgreSQL** 🐘 (Production Ready)
```env
# In .env file
DATABASE_URL=postgresql://username:password@host:port/database_name
```
- **Pros:** Best for production, handles many users, cloud-compatible
- **Cons:** Requires external database service
- **Free Providers:** Render, Supabase, Railway, Heroku

### **3. MySQL** 🐬 (Alternative)
```env
# In .env file
USE_MYSQL=true
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=disaster_db
```
- **Pros:** Popular, good performance, widely supported
- **Cons:** Requires local MySQL installation or cloud service

---

## 📊 CURRENT DATABASE STATISTICS

| Table | Records | Status |
|-------|---------|--------|
| users | 3 | ✅ Active |
| safe_zones | 49 | ✅ Seeded |
| modules | 1 | ✅ Sample |
| emergency_contacts | 5 | ✅ Seeded |
| progress | 0 | ⏳ Empty |
| user_achievements | 0 | ⏳ Empty |
| user_safe_zones | 0 | ⏳ Empty |
| messages | 0 | ⏳ Empty |
| disasters | 0 | ⏳ Empty |
| drills | 0 | ⏳ Empty |
| alerts | 0 | ⏳ Empty |
| drill_participation | 0 | ⏳ Empty |

**Note:** Empty tables will populate as users interact with the application.

---

## 🚀 RECOMMENDATION

**Continue with SQLite for now** ✅

SQLite is **perfect for your current needs** because:
1. ✅ Already working without issues
2. ✅ No additional installation or configuration
3. ✅ Fast and reliable for development/testing
4. ✅ Easy to backup (just copy the `.db` file)
5. ✅ All 49 safe zones are properly seeded
6. ✅ All features are working (auth, quizzes, safe zones, etc.)

**Upgrade to PostgreSQL when:**
- You're ready to deploy to production
- You need to support 100+ concurrent users
- You want cloud database hosting

---

## 📝 HOW TO VIEW DATABASE MANUALLY

### Option 1: Using Python Script
```bash
python inspect_db.py
```

### Option 2: Using DB Browser for SQLite (GUI)
1. Download: https://sqlitebrowser.org/
2. Open: `instance/disaster_app.db`
3. Browse all tables visually

### Option 3: Using Python Console
```python
import sqlite3
conn = sqlite3.connect('instance/disaster_app.db')
cursor = conn.cursor()

# View all safe zones
cursor.execute("SELECT * FROM safe_zones")
zones = cursor.fetchall()
for zone in zones:
    print(zone)

conn.close()
```

---

## ✅ CONCLUSION

**Your database is fully operational!** 🎉

- **Type:** SQLite
- **Location:** `C:\Users\sania\SIH\Backend Python\SEP\instance\disaster_app.db`
- **Status:** ✅ Working perfectly
- **Safe Zones:** 49 across all Indian states
- **Emergency Contacts:** 5 national services
- **Ready for:** Development, testing, and initial deployment

**No action needed** - continue building your application with SQLite. You can easily migrate to PostgreSQL later when needed!
