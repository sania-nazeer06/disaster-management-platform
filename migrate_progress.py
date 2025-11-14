"""
Add user_answers and module_id columns to Progress table
"""
from app import create_app
from models import db

app = create_app()

with app.app_context():
    # Add new columns if they don't exist
    with db.engine.connect() as conn:
        try:
            # Try to add user_answers column
            conn.execute(db.text("ALTER TABLE progress ADD COLUMN user_answers TEXT"))
            conn.commit()
            print("✅ Added user_answers column to progress table")
        except Exception as e:
            if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                print("ℹ️  user_answers column already exists")
            else:
                print(f"⚠️  Error adding user_answers: {e}")
        
        try:
            # Try to add module_id column
            conn.execute(db.text("ALTER TABLE progress ADD COLUMN module_id INTEGER"))
            conn.commit()
            print("✅ Added module_id column to progress table")
        except Exception as e:
            if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                print("ℹ️  module_id column already exists")
            else:
                print(f"⚠️  Error adding module_id: {e}")

print("\n✅ Migration complete!")
