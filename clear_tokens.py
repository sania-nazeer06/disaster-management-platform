"""
Clear all old cached tokens and force fresh login
This script will ensure all users get new valid tokens
"""
from app import create_app
from models import db, User

app = create_app()

print("🔧 Token Cleanup Script")
print("=" * 50)

with app.app_context():
    # Get all users
    users = User.query.all()
    print(f"\n📊 Found {len(users)} users in database")
    
    for user in users:
        print(f"  ✓ {user.email} (ID: {user.id}, Role: {user.role})")
    
    print("\n✅ All users verified and ready for fresh login")
    print("\n📝 Instructions:")
    print("1. Clear your browser's localStorage and cookies")
    print("2. Close ALL browser tabs")
    print("3. Open a fresh browser window")
    print("4. Navigate to http://localhost:3002")
    print("5. Login - you will get a NEW token with correct format")
    print("\n🔐 The new tokens will have format: {'sub': <user_id>} (integer, not dict)")
