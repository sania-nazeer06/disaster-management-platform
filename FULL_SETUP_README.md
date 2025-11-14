# Disaster Preparedness Education Platform - Full Stack Application

Complete disaster management education platform with Flask backend and React frontend.

## 📁 Project Structure

```
SEP/
├── frontend/                # React frontend application
│   ├── src/
│   │   ├── components/      # Reusable components (Navbar)
│   │   ├── context/         # Authentication context
│   │   ├── pages/           # Page components
│   │   ├── services/        # API service layer
│   │   └── App.js           # Main app component
│   ├── public/
│   └── package.json
├── app.py                   # Flask backend server
├── models.py                # Database models
├── schema.sql               # MySQL database schema
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── DATABASE_SETUP.md        # Database setup guide

```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+ and npm
- MySQL 8.0+ (optional - can use SQLite for testing)

### 1. Backend Setup

#### Install Python Dependencies

```powershell
# Navigate to project root
cd "C:\Users\sania\SIH\Backend Python\SEP"

# Create and activate virtual environment (if not already done)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

#### Configure Database

**Option A: Use SQLite (Quick Start)**
```powershell
# In .env file, set:
USE_MYSQL=false
```

**Option B: Use MySQL (Recommended for Production)**

1. Start MySQL server (XAMPP, standalone, etc.)

2. Create the database:
```sql
CREATE DATABASE disaster_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. Run the schema:
```sql
USE disaster_db;
SOURCE schema.sql;
```

4. Update `.env` file:
```env
USE_MYSQL=true
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=disaster_db
```

#### Start Backend Server

```powershell
python app.py
```

Server will run on `http://localhost:5000`

You should see:
```
✓ Using MySQL database: disaster_db
* Running on http://127.0.0.1:5000
```

### 2. Frontend Setup

#### Install Node Dependencies

Open a **new terminal** and run:

```powershell
cd "C:\Users\sania\SIH\Backend Python\SEP\frontend"

# Install dependencies
npm install
```

#### Start Frontend Development Server

```powershell
npm start
```

Frontend will run on `http://localhost:3000` and automatically open in your browser.

## 🎯 How to Use

### 1. Register a New Account

- Go to `http://localhost:3000/register`
- Fill in your details
- Choose your role: Student, Faculty, or Admin
- Click "Create Account"

### 2. Login

- Go to `http://localhost:3000/login`
- Enter your email and password
- You'll be redirected to the dashboard

### 3. Explore Features

#### For All Users:
- **Dashboard**: Overview and quick access to all features
- **Safe Zones**: View map and list of emergency shelters
- **Disasters**: Learn about different disaster types with videos
- **Messages**: Send and receive messages

#### For Students:
- **Progress**: Track quiz scores and module completion

#### For Faculty/Admin:
- **Add Safe Zones**: Create new safe zone markers on the map
- **Add Disaster Info**: Create educational content with YouTube videos
- **Manage Content**: Edit and delete existing information

## 🔑 Test Accounts

Create test accounts with different roles to test all features:

```
Student Account:
Email: student@test.com
Password: password123
Role: student

Faculty Account:
Email: faculty@test.com
Password: password123
Role: faculty

Admin Account:
Email: admin@test.com
Password: password123
Role: admin
```

## 📡 API Endpoints

### Authentication
- POST `/auth/register` - Register new user
- POST `/auth/login` - Login and get JWT token

### Safe Zones
- GET `/safe_zones` - List all safe zones (public)
- POST `/safe_zones` - Create safe zone (faculty/admin only)
- GET `/safe_zones/<id>` - Get single safe zone
- PUT `/safe_zones/<id>` - Update safe zone (faculty/admin only)
- DELETE `/safe_zones/<id>` - Delete safe zone (faculty/admin only)

### Disasters
- GET `/disasters` - List all disaster info (public)
- POST `/disasters` - Create disaster info (faculty/admin only)
- GET `/disasters/<id>` - Get single disaster
- PUT `/disasters/<id>` - Update disaster (faculty/admin only)
- DELETE `/disasters/<id>` - Delete disaster (faculty/admin only)

### Messages
- POST `/messages` - Send message (authenticated)
- GET `/messages/inbox` - Get received messages
- GET `/messages/sent` - Get sent messages

### Progress
- POST `/progress` - Create or update progress (authenticated)
- GET `/progress/user/<user_id>` - Get user progress

## 🛠️ Troubleshooting

### Backend Issues

**Port 5000 already in use:**
```powershell
# Find and kill process on port 5000
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process
```

**MySQL connection failed:**
- Check if MySQL server is running
- Verify credentials in `.env` file
- Test connection: `mysql -u root -p`

**Import errors:**
```powershell
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend Issues

**npm install fails:**
```powershell
# Clear cache and reinstall
npm cache clean --force
rm -r node_modules package-lock.json
npm install
```

**CORS errors:**
- Make sure backend is running on port 5000
- Check `proxy` setting in `frontend/package.json`

**Map not loading:**
- Check internet connection (needs OpenStreetMap tiles)
- Check browser console for errors

## 🔧 Development Tips

### Adding New Features

1. **Backend (Flask)**:
   - Add route in `app.py`
   - Update models if needed in `models.py`
   - Test with Postman or curl

2. **Frontend (React)**:
   - Add API function in `src/services/api.js`
   - Create/update page component in `src/pages/`
   - Add route in `src/App.js`

### Code Structure

**Backend**:
- `app.py` - Routes and business logic
- `models.py` - SQLAlchemy database models
- `schema.sql` - Database schema for MySQL

**Frontend**:
- `src/context/AuthContext.js` - Authentication state
- `src/services/api.js` - API calls to backend
- `src/pages/` - Page components
- `src/components/` - Reusable components

## 📦 Building for Production

### Backend

```powershell
# Use a production WSGI server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend

```powershell
cd frontend
npm run build

# Serve the build folder with any static server
```

## 🎨 Customization

### Change Theme Colors

Edit `frontend/src/index.css` and component CSS files.

### Add New Disaster Types

Faculty/Admin can add through the UI, or seed via SQL:

```sql
INSERT INTO disasters (disaster_type, info, video_link) 
VALUES ('Tsunami', 'Move to higher ground immediately...', 'https://youtube.com/...');
```

### Configure Map Center

Edit `frontend/src/pages/SafeZones.js`:
```javascript
center={[YOUR_LATITUDE, YOUR_LONGITUDE]}
```

## 📝 License

Educational project for disaster preparedness.

## 🆘 Support

For issues or questions:
1. Check `DATABASE_SETUP.md` for database help
2. Review error messages in terminal
3. Check browser console (F12) for frontend errors
4. Ensure both backend and frontend are running

---

**Made with ❤️ for disaster preparedness education**
