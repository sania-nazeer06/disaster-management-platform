"""
Test script to debug JWT token issue
"""
from app import create_app
from models import db, User
from flask_jwt_extended import create_access_token
import json

app = create_app()

with app.app_context():
    # Get user 20
    user = User.query.get(20)
    if not user:
        print("❌ User 20 not found!")
        exit(1)
    
    print(f"✅ User found: {user.name} ({user.email}) - ID: {user.id}")
    
    # Create token
    token = create_access_token(identity=user.id)
    print(f"\n📝 Token created (first 80 chars): {token[:80]}...")
    
    # Decode token to see payload
    import jwt
    secret = app.config['JWT_SECRET_KEY']
    decoded = jwt.decode(token, secret, algorithms=["HS256"])
    print(f"\n🔍 Decoded token payload:")
    print(json.dumps(decoded, indent=2))
    
    # Check 'sub' claim
    sub = decoded.get('sub')
    print(f"\n✓ 'sub' claim type: {type(sub)}")
    print(f"✓ 'sub' claim value: {sub}")
    
    if isinstance(sub, dict):
        print("❌ ERROR: 'sub' is a dictionary! Should be a number.")
    elif isinstance(sub, int):
        print("✅ GOOD: 'sub' is an integer")
        
        # Verify user exists
        test_user = User.query.get(sub)
        if test_user:
            print(f"✅ User {sub} exists: {test_user.name}")
        else:
            print(f"❌ User {sub} NOT FOUND in database!")
    else:
        print(f"⚠️  'sub' is type {type(sub)}, value: {sub}")
