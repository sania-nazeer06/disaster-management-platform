"""
Create a test user for login
"""
from app import create_app
from models import db, User
import bcrypt

app = create_app()

with app.app_context():
    # Check if student@test.com exists
    existing = User.query.filter_by(email='student@test.com').first()
    if existing:
        print(f"User exists: {existing.email}")
        # Update password
        pw_hash = bcrypt.hashpw('test123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        existing.password_hash = pw_hash
        db.session.commit()
        print("✓ Password reset to: test123")
    else:
        # Create new user
        pw_hash = bcrypt.hashpw('test123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User(name='Test Student', email='student@test.com', password_hash=pw_hash, role='student')
        db.session.add(user)
        db.session.commit()
        print("✓ Created new user: student@test.com / test123")
    
    # Also create admin and faculty if they don't exist
    if not User.query.filter_by(email='admin@test.com').first():
        pw_hash = bcrypt.hashpw('test123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin = User(name='Test Admin', email='admin@test.com', password_hash=pw_hash, role='admin')
        db.session.add(admin)
        db.session.commit()
        print("✓ Created admin@test.com / test123")
    
    if not User.query.filter_by(email='faculty@test.com').first():
        pw_hash = bcrypt.hashpw('test123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        faculty = User(name='Test Faculty', email='faculty@test.com', password_hash=pw_hash, role='faculty')
        db.session.add(faculty)
        db.session.commit()
        print("✓ Created faculty@test.com / test123")
    
    print("\n✅ All test users ready!")
    print("Login with:")
    print("  student@test.com / test123")
    print("  faculty@test.com / test123")
    print("  admin@test.com / test123")
