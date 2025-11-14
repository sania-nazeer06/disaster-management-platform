"""
Script to update database with new tables
Run this after adding new models
"""
from app import create_app
from models import db

app = create_app()

with app.app_context():
    print("Creating new database tables...")
    db.create_all()
    print("✓ Database tables updated successfully!")
    print("You can now restart your Flask server.")
