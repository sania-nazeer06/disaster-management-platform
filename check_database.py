"""
Check database contents
"""
from app import create_app
from models import db, User, Message, Progress, Module, Drill, SafeZone

app = create_app()

with app.app_context():
    print("\n=== DATABASE STATUS ===\n")
    
    # Check Users
    users = User.query.all()
    print(f"📊 Total Users: {len(users)}")
    for user in users:
        print(f"  - {user.email} ({user.role}) - {user.name}")
    
    # Check Messages
    messages = Message.query.all()
    print(f"\n📨 Total Messages: {len(messages)}")
    
    # Check Progress
    progress = Progress.query.all()
    print(f"📈 Total Progress Records: {len(progress)}")
    
    # Check Modules
    modules = Module.query.all()
    print(f"📚 Total Modules: {len(modules)}")
    
    # Check Drills
    drills = Drill.query.all()
    print(f"🚨 Total Drills: {len(drills)}")
    
    # Check Safe Zones
    zones = SafeZone.query.all()
    print(f"📍 Total Safe Zones: {len(zones)}")
    
    print("\n" + "="*50)
