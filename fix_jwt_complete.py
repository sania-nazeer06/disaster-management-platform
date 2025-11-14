"""
Complete JWT fix - replaces all identity.get() references in app.py
"""

# Read the file
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Count occurrences before
before_id = content.count("identity.get('id')")
before_role = content.count("identity.get('role')")
print(f"Before fix:")
print(f"  identity.get('id'): {before_id} occurrences")
print(f"  identity.get('role'): {before_role} occurrences")

# Replace all identity.get('id') with identity
content = content.replace("identity.get('id')", "identity")

# Replace all role checks - need to fetch user first
# Pattern 1: Simple role check in if statements
old_pattern1 = """identity = get_jwt_identity()
        if identity.get('role') not in ('faculty', 'admin'):"""
new_pattern1 = """identity = get_jwt_identity()
        user = User.query.get(identity)
        if user.role not in ('faculty', 'admin'):"""

old_pattern2 = """identity = get_jwt_identity()
        if identity.get('role') not in ('student',):"""
new_pattern2 = """identity = get_jwt_identity()
        user = User.query.get(identity)
        if user.role not in ('student',):"""

old_pattern3 = """identity = get_jwt_identity()
        if identity.get('role') != 'admin':"""
new_pattern3 = """identity = get_jwt_identity()
        user = User.query.get(identity)
        if user.role != 'admin':"""

# Apply replacements
content = content.replace(old_pattern1, new_pattern1)
content = content.replace(old_pattern2, new_pattern2)
content = content.replace(old_pattern3, new_pattern3)

# Write back
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Count occurrences after
after_id = content.count("identity.get('id')")
after_role = content.count("identity.get('role')")
print(f"\nAfter fix:")
print(f"  identity.get('id'): {after_id} occurrences")
print(f"  identity.get('role'): {after_role} occurrences")
print(f"\n✅ JWT identity references updated!")
print(f"   - Replaced {before_id - after_id} identity.get('id') calls")
print(f"   - Replaced {before_role - after_role} identity.get('role') calls")
