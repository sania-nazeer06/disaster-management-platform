"""
Script to fix JWT identity format in app.py
Changes from: identity.get('id') and identity.get('role')
To: identity (for user_id) and User.query.get(identity).role (for role checks)
"""

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all occurrences
replacements = [
    # For ID retrieval
    ("uid = identity.get('id')", "uid = identity"),
    ("sender_id = identity.get('id')", "sender_id = identity"),
    ("user_id = data.get('user_id', identity.get('id'))", "user_id = data.get('user_id', identity)"),
    ("created_by=identity.get('id')", "created_by=identity"),
    ("log_activity(identity.get('id'),", "log_activity(identity,"),
    
    # For role checks - need to fetch user first
    ("identity = get_jwt_identity()\n        if identity.get('role') not in ('faculty', 'admin'):",
     "identity = get_jwt_identity()\n        user = User.query.get(identity)\n        if user.role not in ('faculty', 'admin'):"),
    
    ("identity = get_jwt_identity()\n        if identity.get('role') != 'admin':",
     "identity = get_jwt_identity()\n        user = User.query.get(identity)\n        if user.role != 'admin':"),
]

for old, new in replacements:
    content = content.replace(old, new)

# Write back
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Fixed all JWT identity references in app.py")
print("Now restart the backend server!")
