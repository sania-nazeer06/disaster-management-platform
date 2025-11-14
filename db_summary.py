import sqlite3

conn = sqlite3.connect('instance/disaster_app.db')
cursor = conn.cursor()

print("\n" + "="*80)
print("DISASTER MANAGEMENT APP - DATABASE OVERVIEW")
print("="*80)

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print(f"\nTotal Tables: {len(tables)}")
print("-"*80)

# For each table, show count and structure
for table in tables:
    table_name = table[0]
    
    # Get row count
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    
    # Get column count
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    col_count = len(columns)
    
    status = "ACTIVE" if count > 0 else "EMPTY"
    print(f"{table_name:25s} | {count:6d} rows | {col_count:2d} columns | {status}")

print("-"*80)

# Summary statistics
cursor.execute("SELECT COUNT(*) FROM users")
user_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM safe_zones")
zone_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM modules")
module_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM emergency_contacts")
contact_count = cursor.fetchone()[0]

print(f"\nKEY STATISTICS:")
print(f"  Registered Users: {user_count}")
print(f"  Safe Zones: {zone_count}")
print(f"  Learning Modules: {module_count}")
print(f"  Emergency Contacts: {contact_count}")

print("\n" + "="*80)
print("DATABASE STATUS: OPERATIONAL")
print("DATABASE TYPE: SQLite")
print("DATABASE FILE: instance/disaster_app.db")
print("="*80 + "\n")

conn.close()
