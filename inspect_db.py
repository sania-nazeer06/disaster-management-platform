import sqlite3
import json

def inspect_database():
    conn = sqlite3.connect('instance/disaster_app.db')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("\n" + "="*80)
    print("DATABASE INSPECTION - disaster_app.db")
    print("="*80)
    
    print(f"\n📊 Found {len(tables)} tables:")
    for table in tables:
        print(f"   ✓ {table[0]}")
    
    print("\n" + "="*80)
    
    # For each table, show structure and sample data
    for table in tables:
        table_name = table[0]
        print(f"\n🗃️  TABLE: {table_name}")
        print("-"*80)
        
        # Get table schema
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        print(f"\n   COLUMNS ({len(columns)}):")
        for col in columns:
            col_id, col_name, col_type, not_null, default, pk = col
            pk_marker = " [PRIMARY KEY]" if pk else ""
            null_marker = " NOT NULL" if not_null else ""
            print(f"     • {col_name}: {col_type}{pk_marker}{null_marker}")
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"\n   📈 TOTAL ROWS: {count}")
        
        # Show sample data (first 5 rows)
        if count > 0:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
            rows = cursor.fetchall()
            col_names = [col[1] for col in columns]
            
            print(f"\n   📋 SAMPLE DATA (showing {min(count, 5)} of {count} rows):")
            for idx, row in enumerate(rows, 1):
                print(f"\n      Row {idx}:")
                for col_name, value in zip(col_names, row):
                    # Format JSON fields nicely
                    if col_name in ['quiz_questions', 'image_urls'] and value:
                        try:
                            formatted = json.dumps(json.loads(value), indent=8)
                            print(f"        {col_name}: {formatted}")
                        except:
                            print(f"        {col_name}: {value}")
                    else:
                        # Truncate long strings
                        if isinstance(value, str) and len(value) > 100:
                            print(f"        {col_name}: {value[:100]}...")
                        else:
                            print(f"        {col_name}: {value}")
        
        print("\n" + "-"*80)
    
    conn.close()
    
    print("\n" + "="*80)
    print("✅ Database inspection complete!")
    print("="*80 + "\n")

if __name__ == "__main__":
    inspect_database()
