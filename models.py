from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('student', 'faculty', 'admin'), nullable=False, default='student')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role
        }

class SafeZone(db.Model):
    __tablename__ = 'safe_zones'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Numeric(10,7), nullable=False)
    longitude = db.Column(db.Numeric(10,7), nullable=False)
    description = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'lat': float(self.latitude),
            'lng': float(self.longitude),
            'description': self.description
        }

class Disaster(db.Model):
    __tablename__ = 'disasters'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    disaster_type = db.Column(db.String(100), nullable=False)
    info = db.Column(db.Text, nullable=False)
    video_link = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'disaster_type': self.disaster_type,
            'info': self.info,
            'video_link': self.video_link
        }

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    message_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'message_text': self.message_text,
            'timestamp': self.timestamp.isoformat()
        }

class Progress(db.Model):
    __tablename__ = 'progress'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    module_name = db.Column(db.String(255), nullable=False)
    quiz_score = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)
    user_answers = db.Column(db.Text)  # JSON array of user's answers
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id', ondelete='CASCADE'))  # Link to module

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'module_name': self.module_name,
            'quiz_score': self.quiz_score,
            'completed': self.completed,
            'user_answers': self.user_answers,
            'module_id': self.module_id
        }

# New models for additional features

class Module(db.Model):
    __tablename__ = 'modules'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))
    difficulty = db.Column(db.String(20), default='beginner')
    points = db.Column(db.Integer, default=100)
    quiz_questions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'content': self.content,
            'difficulty': self.difficulty,
            'points': self.points,
            'quiz_questions': self.quiz_questions,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Drill(db.Model):
    __tablename__ = 'drills'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    drill_type = db.Column(db.String(100))
    steps = db.Column(db.Text, nullable=False)
    duration_minutes = db.Column(db.Integer, default=15)
    scheduled_date = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'drill_type': self.drill_type,
            'steps': self.steps,
            'duration_minutes': self.duration_minutes,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'created_by': self.created_by
        }

class DrillParticipation(db.Model):
    __tablename__ = 'drill_participation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    drill_id = db.Column(db.Integer, db.ForeignKey('drills.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Float, default=0.0)
    completion_time = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'drill_id': self.drill_id,
            'user_id': self.user_id,
            'completed': self.completed,
            'score': self.score,
            'completion_time': self.completion_time.isoformat() if self.completion_time else None
        }

class Alert(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    alert_type = db.Column(db.String(50))
    severity = db.Column(db.String(20), default='medium')
    region = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    radius_km = db.Column(db.Float, default=10.0)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'region': self.region,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'radius_km': self.radius_km,
            'active': self.active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_by': self.created_by
        }

class EmergencyContact(db.Model):
    __tablename__ = 'emergency_contacts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    organization = db.Column(db.String(200))
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    category = db.Column(db.String(50))
    region = db.Column(db.String(100))
    available_24_7 = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'organization': self.organization,
            'phone': self.phone,
            'email': self.email,
            'category': self.category,
            'region': self.region,
            'available_24_7': self.available_24_7
        }


class UserSafeZone(db.Model):
    __tablename__ = 'user_safe_zones'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    zone_id = db.Column(db.Integer, db.ForeignKey('safe_zones.id', ondelete='CASCADE'), nullable=False)
    marked_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'zone_id': self.zone_id,
            'marked_at': self.marked_at.isoformat() if self.marked_at else None
        }

class UserAchievement(db.Model):
    __tablename__ = 'user_achievements'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    achievement_type = db.Column(db.String(100))
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    points = db.Column(db.Integer, default=0)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'achievement_type': self.achievement_type,
            'title': self.title,
            'description': self.description,
            'points': self.points,
            'earned_at': self.earned_at.isoformat() if self.earned_at else None
        }


class RecentActivity(db.Model):
    __tablename__ = 'recent_activities'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # 'module', 'message', 'safe_zone', 'drill'
    description = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='activities')
    
    def to_dict(self):
        user_name = 'Unknown'
        try:
            if self.user:
                user_name = self.user.name
        except:
            pass
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'activity_type': self.activity_type,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user_name': user_name
        }


