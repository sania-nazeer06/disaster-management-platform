from app import create_app
from models import db, User

app = create_app()
with app.app_context():
    user = User.query.get(20)
    if user:
        print(f"✅ User 20 exists: {user.name} ({user.email}) - Role: {user.role}")
    else:
        print("❌ User 20 not found")
        
    # List all users
    all_users = User.query.all()
    print(f"\n📋 Total users: {len(all_users)}")
    for u in all_users[:5]:
        print(f"  - ID {u.id}: {u.name} ({u.email}) - {u.role}")
