# 🛡️ Disaster Preparedness PlatformDisaster Management Education Backend (Flask)



A comprehensive disaster management and preparedness platform with **55+ region-wise safe zones across India**, educational modules, emergency contacts, and role-based access control.This repository contains a simple Flask backend for a disaster management education app. It provides APIs for managing safe zones, disaster educational content, user authentication with roles, messaging, and student progress tracking. MySQL is used as the database.



## 🌟 Key FeaturesFiles added:

- app.py - Main Flask application with routes and initialization.

### 🗺️ Region-Wise Safe Zones  - models.py - SQLAlchemy models for users, safe_zones, disasters, messages, and progress.

- **55+ Safe Zones** covering all Indian states and Union Territories- requirements.txt - Python packages required.

- Interactive map with real-time location tracking- .env.example - Example environment variables file.

- Students can mark visited zones for progress tracking- schema.sql - SQL to create the database and tables.



**Coverage by Region:**Setup (Windows PowerShell):

- **North India (12 zones)**: Delhi, Chandigarh, Jaipur, Lucknow, Amritsar, Shimla, Dehradun, etc.1) Create and activate venv:

- **South India (14 zones)**: Mumbai, Bengaluru, Chennai, Hyderabad, Kochi, Mysuru, etc.   python -m venv .venv

- **East India (9 zones)**: Kolkata, Bhubaneswar, Patna, Ranchi, Guwahati, etc.   .\.venv\Scripts\Activate.ps1

- **West India (6 zones)**: Ahmedabad, Surat, Indore, Bhopal, Goa

- **Northeast India (4 zones)**: Shillong, Aizawl, Itanagar, Gangtok2) Install dependencies:

   pip install -r requirements.txt

### 📚 Educational Modules

- Interactive disaster preparedness modules with images3) Copy .env.example to .env and edit DB values and secrets.

- **15-question intermediate-level quizzes** (high school/college level)

- **Points-based gamification** (150 points per module)4) Create DB and tables by running the SQL in schema.sql using your MySQL client.

- Achievement tracking and leaderboards

- Example: Earthquake Preparedness module covering Richter scale, safety procedures, emergency kits5) Run the app:

   python app.py

### 🚨 Emergency Contacts

- Quick access to emergency services on all dashboardsAPI summary (JSON responses):

- **Ambulance**: 102- POST /auth/register — register a user (body: name, email, password, role)

- **Police**: 100- POST /auth/login — login (body: email, password) -> returns JWT access_token

- **Fire**: 101- GET /safe_zones — list safe zones

- **NDRF**: +91-011-2436-1234- POST /safe_zones — create (protected: faculty/admin)

- **Red Cross**- GET /safe_zones/<id>

- PUT /safe_zones/<id> — update (protected: faculty/admin)

### 👥 Role-Based Access- DELETE /safe_zones/<id> — delete (protected: faculty/admin)

- **Students**: View zones, take quizzes, track progress, earn points- GET /disasters — list disasters

- **Faculty**: Manage content, create quizzes, view student progress- POST /disasters — create (protected: faculty/admin)

- **Admin**: Full analytics, user management, platform monitoring- GET /disasters/<id>

- PUT /disasters/<id> — update (protected)

### 🎨 Modern UI/UX- DELETE /disasters/<id> — delete (protected)

- **Material-UI** components with colorful, modern design- POST /messages — send message (protected)

- Gradient emergency contact cards- GET /messages/inbox — view messages for logged-in user

- Responsive design for mobile and desktop- GET /messages/sent — messages sent by logged-in user

- Interactive maps using React Leaflet- POST /progress — create or update progress (protected)

- GET /progress/user/<user_id> — view progress for a user (protected)

## 🚀 Quick Start

Notes:

### Backend Setup- For production, secure secrets, add input validation, pagination, and unit tests.


```bash
# Navigate to project directory
cd "Backend Python/SEP"

# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure database (.env file)
# Copy .env.example to .env and configure:
DATABASE_URL=postgresql://username:password@host:port/database_name
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

# Run backend
python app.py
# Server starts at http://127.0.0.1:5000
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
# App opens at http://localhost:3000
```

## 📊 Database Configuration

### PostgreSQL (Recommended for Production)

Set `DATABASE_URL` in `.env`:
```
DATABASE_URL=postgresql://username:password@host:port/database_name
```

**Free PostgreSQL Providers:**
- **Render** - https://render.com (Free tier available)
- **Supabase** - https://supabase.com (Free PostgreSQL + extras)
- **Railway** - https://railway.app (Easy deployment)
- **Heroku** - https://heroku.com (PostgreSQL add-on)

### MySQL (Alternative)

Set in `.env`:
```
USE_MYSQL=true
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your-password
DB_NAME=disaster_db
```

### SQLite (Development Only)

No configuration needed - used automatically if DATABASE_URL is not set.

## 🔌 API Endpoints

**Full documentation**: Open `API_DOCUMENTATION.html` in your browser

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token

### Safe Zones (55+ locations)
- `GET /safe_zones` - Get all safe zones
- `POST /safe_zones/:id/mark` - Mark zone as visited 🔒
- `GET /safe_zones/marked` - Get user's marked zones 🔒

### Modules & Quizzes
- `GET /modules` - Get all educational modules
- `POST /modules/:id/attempt` - Submit quiz (15 questions) 🔒
  - Returns score %, points earned, achievements

### Emergency Contacts
- `GET /emergency-contacts` - Get all emergency contacts

### Admin Analytics
- `GET /analytics/overview` - Platform statistics 🔒 (Admin)
- `GET /users` - All users 🔒 (Admin)
- `GET /users/students` - All students 🔒 (Faculty/Admin)

🔒 = Requires JWT authentication

## 🗺️ Safe Zones by State

| State | Number of Zones | Major Cities |
|-------|----------------|--------------|
| Delhi | 2 | Connaught Place, Dwarka |
| Maharashtra | 4 | Mumbai (2), Pune, Nagpur |
| Karnataka | 3 | Bengaluru (2), Mysuru |
| Tamil Nadu | 3 | Chennai (2), Coimbatore |
| Uttar Pradesh | 3 | Lucknow, Varanasi, Agra |
| West Bengal | 3 | Kolkata (2), Darjeeling |
| Telangana | 2 | Hyderabad (2) |
| Gujarat | 3 | Ahmedabad, Surat, Vadodara |
| Rajasthan | 3 | Jaipur, Jodhpur, Udaipur |
| And 20+ more states | 29+ zones | Full India coverage |

## 🛠️ Technology Stack

### Backend
- Flask 2.3.3
- SQLAlchemy ORM
- Flask-JWT-Extended
- PostgreSQL/MySQL/SQLite
- Bcrypt password hashing

### Frontend
- React 18.2.0
- Material-UI (MUI)
- React Router
- Axios
- React Leaflet (maps)
- Inter Google Font

## 📱 User Roles & Features

### Student Dashboard
✅ View 55+ safe zones on map  
✅ Mark zones as visited  
✅ Take 15-question quizzes  
✅ Earn points (150 per module)  
✅ Track achievements  
✅ Access emergency contacts  
✅ Send/receive messages  

### Faculty Dashboard
✅ All student features  
✅ Create educational modules  
✅ Design custom quizzes  
✅ View student progress  
✅ Manage safe zones  
✅ Add emergency contacts  

### Admin Dashboard
✅ All faculty features  
✅ Platform analytics  
✅ User management  
✅ Monitor drill participations  
✅ Calculate preparedness scores  
✅ System-wide monitoring  

## 📈 Database Schema

10 interconnected tables:

- `users` - User accounts (student/faculty/admin)
- `safe_zones` - **55+ region-wise safe zones**
- `user_safe_zones` - Student zone visit tracking
- `modules` - Educational content with quizzes
- `user_achievements` - Quiz scores and points
- `emergency_contacts` - Emergency service info
- `disasters` - Disaster types
- `messages` - User messaging
- `drills` - Disaster preparedness drills
- `alerts` - Emergency alerts

## 🎯 Gamification Features

- **Points System**: 150 points per module quiz
- **Achievement Tracking**: Automatically created on quiz completion
- **Leaderboard**: Compare scores with other students
- **Progress Monitoring**: Track learning journey
- **Zone Marking**: Build personal safe zone knowledge

## 🔐 Security

- JWT-based authentication
- Bcrypt password hashing
- Role-based access control (RBAC)
- Protected API endpoints
- CORS configuration
- Environment variable management

## 🚀 Deployment Guide

### Option 1: Render (Backend) + Vercel (Frontend)

**Backend on Render:**
1. Push code to GitHub
2. Create Web Service on Render.com
3. Add PostgreSQL database (free tier)
4. Set environment variables
5. Deploy!

**Frontend on Vercel:**
1. Push frontend to GitHub
2. Import to Vercel.com
3. Set `REACT_APP_API_URL`
4. Deploy!

### Option 2: Railway (Full Stack)

1. Push to GitHub
2. Deploy backend + PostgreSQL on Railway
3. Deploy frontend separately or use same Railway project
4. Connect services

## 📞 API Documentation

**Complete API Reference**: Open `API_DOCUMENTATION.html` in any browser for:
- All endpoint details
- Request/response examples
- Database schema
- Setup instructions
- Technology stack
- Code examples

## 🤝 Integration Flow

1. **Backend** connects to **PostgreSQL** database
2. **Database** stores all users, zones, modules, scores
3. **Frontend** calls **Backend API** endpoints
4. **JWT tokens** secure authenticated routes
5. **Real-time updates** reflect in all dashboards

## 📝 Sample Data Included

On first run, the app automatically seeds:
- ✅ **55+ safe zones** across all Indian states
- ✅ **5 emergency contacts** (Ambulance, Police, Fire, NDRF, Red Cross)
- ✅ **1 sample module** (Earthquake Preparedness with 15 questions)
- ✅ Ready to register users and start using!

## 🎓 Educational Module Example

**Earthquake Preparedness & Safety**
- 15 intermediate-level questions
- Topics: Richter scale, safety procedures, emergency kits, Indian emergency numbers
- 150 points total
- Covers: Drop/Cover/Hold On, Triangle of Life theory, aftershock expectations

## 📬 Contact & Support

For questions, check `API_DOCUMENTATION.html` or review this README.

---

**Built for Smart India Hackathon** - Comprehensive disaster preparedness platform with region-wise coverage across India 🇮🇳

**License**: MIT
