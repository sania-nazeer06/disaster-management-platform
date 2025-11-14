import sqlite3

conn = sqlite3.connect('instance/disaster_app.db')
cursor = conn.cursor()

cursor.execute('SELECT COUNT(*) FROM safe_zones')
count = cursor.fetchone()[0]
print(f'\n🗺️  Total Safe Zones in Database: {count}')

cursor.execute('SELECT id, name, latitude, longitude, description FROM safe_zones ORDER BY id')
zones = cursor.fetchall()

print('\nAll Safe Zones:')
print('='*100)

for z in zones:
    zone_id, name, lat, lng, desc = z
    desc_short = desc[:50] + '...' if desc and len(desc) > 50 else desc
    print(f'{zone_id:3d}. {name:35s} | Lat: {lat:8.4f}, Lng: {lng:8.4f} | {desc_short}')

print('='*100)
print(f'\n✅ Found {count} safe zones in the database\n')

conn.close()
