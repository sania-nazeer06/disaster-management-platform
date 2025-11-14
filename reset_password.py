"""
Reset password for student@test.com
"""
from app import create_app
from models import db, User
import bcrypt

app = create_app()

with app.app_context():
    user = User.query.filter_by(email='student@test.com').first()
    if user:
        # Set password to exactly 'test123'
        pw_hash = bcrypt.hashpw('test123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.password_hash = pw_hash
        db.session.commit()
        print(f"✅ Password reset for {user.email}")
        print(f"   Email: student@test.com")
        print(f"   Password: test123")
        print(f"   User ID: {user.id}")
        print(f"   Role: {user.role}")
        
        # Test the password
        test_result = bcrypt.checkpw('test123'.encode('utf-8'), user.password_hash.encode('utf-8'))
        print(f"   Password test: {'✅ WORKS' if test_result else '❌ FAILED'}")
    else:
        print("❌ User not found!")
