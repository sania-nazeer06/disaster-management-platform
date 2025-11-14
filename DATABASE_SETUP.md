# Database Setup Guide

## Option 1: Use SQLite (Quick Start - Already Working)

The app is currently configured to use SQLite by default. No additional setup needed!

Just run: `python app.py`

## Option 2: Use MySQL (Production Setup)

### Step 1: Install MySQL

If you don't have MySQL installed:
- Download from: https://dev.mysql.com/downloads/installer/
- Or use XAMPP/WAMP which includes MySQL

### Step 2: Start MySQL Server

- If using XAMPP: Start Apache and MySQL from XAMPP Control Panel
- If using standalone MySQL: It should auto-start as a service

### Step 3: Create the Database

Open MySQL command line or MySQL Workbench and run:

```sql
CREATE DATABASE IF NOT EXISTS disaster_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE disaster_db;
```

### Step 4: Run the Schema File

From MySQL command line:
```sql
SOURCE schema.sql;
```

Or copy-paste the contents of `schema.sql` into MySQL Workbench and execute.

This will create all 5 tables:
- users
- safe_zones
- disasters
- messages
- progress

### Step 5: Update .env File

Edit `.env` and set:

```env
USE_MYSQL=true
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password_here
DB_NAME=disaster_db
```

### Step 6: Test the Connection

Run the Flask app:
```
python app.py
```

You should see: `✓ Using MySQL database: disaster_db`

## Verify Tables Were Created

In MySQL:
```sql
USE disaster_db;
SHOW TABLES;
DESCRIBE users;
```

You should see all 5 tables listed.

## If You Already Have a Database

If you created a database with 2 tables already:

1. **Option A**: Drop those tables and run `schema.sql` to create all 5 required tables
2. **Option B**: Tell me which 2 tables you have, and I'll create a migration script to add the missing 3 tables

Run this to see your current tables:
```sql
SHOW TABLES;
```
