import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
import bcrypt
from datetime import timedelta, datetime
from models import db, User, SafeZone, Disaster, Message, Progress, Module, Drill, DrillParticipation, Alert, EmergencyContact, UserAchievement, UserSafeZone, RecentActivity
import json

# Load environment variables from .env
load_dotenv()


def create_app():
    app = Flask(__name__)
    
    # Log every single request
    @app.before_request
    def log_request():
        print(f"\n========== REQUEST ==========")
        print(f"PATH: {request.path}")
        print(f"METHOD: {request.method}")
        print(f"HEADERS: {dict(request.headers)}")
        print(f"============================\n")
    
    # Load config from environment
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret')
    
    # Database configuration - reads from .env file
    # Priority: PostgreSQL (DATABASE_URL) > MySQL (USE_MYSQL) > SQLite (default)
    database_url = os.environ.get('DATABASE_URL')
    use_mysql = os.environ.get('USE_MYSQL', 'false').lower() == 'true'
    
    if database_url:
        # PostgreSQL from DATABASE_URL (e.g., from Render, Heroku, etc.)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        print(f"[OK] Using PostgreSQL database from DATABASE_URL")
    elif use_mysql:
        db_host = os.environ.get('DB_HOST', 'localhost')
        db_port = os.environ.get('DB_PORT', '3306')
        db_name = os.environ.get('DB_NAME', 'disaster_db')
        db_user = os.environ.get('DB_USER', 'root')
        db_password = os.environ.get('DB_PASSWORD', '')
        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        print(f"[OK] Using MySQL database: {db_name}")
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///disaster_app.db'
        print("[OK] Using SQLite database for development")
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)  # Extended to 30 days
    app.config['JWT_IDENTITY_CLAIM'] = 'sub'
    app.config['JWT_TOKEN_LOCATION'] = ['headers']

    CORS(app)
    db.init_app(app)
    jwt = JWTManager(app)
    
    # JWT error handlers with enhanced logging
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        # Log details for debugging expired tokens
        try:
            print(f"[JWT][EXPIRED] path={request.path} method={request.method} header={jwt_header} payload={jwt_payload}")
        except Exception:
            print("[JWT][EXPIRED] could not print jwt details")
        return jsonify({
            'success': False, 
            'message': 'Token has expired. Please log in again.', 
            'error': 'token_expired',
            'code': 'TOKEN_EXPIRED'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        # Log details for debugging invalid tokens
        try:
            print(f"[JWT][INVALID] path={request.path} method={request.method} error={error}")
            print(f"[JWT][INVALID] headers={dict(request.headers)}")
        except Exception:
            print("[JWT][INVALID] could not print jwt details")
        return jsonify({
            'success': False, 
            'message': 'Invalid token. Please log in again.', 
            'error': 'invalid_token',
            'code': 'TOKEN_INVALID'
        }), 422
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        try:
            print(f"[JWT][MISSING] path={request.path} method={request.method} error={error}")
        except Exception:
            print("[JWT][MISSING] could not print jwt details")
        return jsonify({
            'success': False, 
            'message': 'Authorization token is missing. Please log in.', 
            'error': 'missing_token',
            'code': 'TOKEN_MISSING'
        }), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        try:
            print(f"[JWT][REVOKED] path={request.path} method={request.method}")
        except Exception:
            print("[JWT][REVOKED] could not print jwt details")
        return jsonify({
            'success': False,
            'message': 'Token has been revoked. Please log in again.',
            'error': 'token_revoked',
            'code': 'TOKEN_REVOKED'
        }), 401

    @app.errorhandler(404)
    def not_found(e):
        print(f"[404 ERROR] path={request.path} method={request.method}")
        return jsonify({
            'success': False, 
            'message': f'Endpoint not found: {request.path}',
            'error': 'not_found'
        }), 404

    @app.errorhandler(500)
    def server_error(e):
        print(f"[500 ERROR] {e}")
        return jsonify({
            'success': False, 
            'message': 'Internal server error. Please try again later.',
            'error': 'server_error'
        }), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        # Log the exception
        print(f"[EXCEPTION] {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Return JSON instead of HTML for HTTP errors
        if hasattr(e, 'code'):
            return jsonify({
                'success': False,
                'message': str(e),
                'error': 'http_error'
            }), e.code
        
        return jsonify({
            'success': False,
            'message': 'An unexpected error occurred',
            'error': 'internal_error'
        }), 500

    # Helper function to get current user from JWT token
    def get_current_user():
        """Get current user from JWT token with validation"""
        try:
            identity = get_jwt_identity()
            if not identity:
                return None
            # Convert string identity to int for database lookup
            user = User.query.get(int(identity))
            if not user:
                print(f"[WARNING] Token identity {identity} not found in database")
            return user
        except Exception as e:
            print(f"[ERROR] get_current_user: {e}")
            return None

    # Helper function to validate user role
    def require_role(*roles):
        """Decorator to require specific roles for an endpoint"""
        from functools import wraps
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                user = get_current_user()
                if not user:
                    return jsonify({
                        'success': False, 
                        'message': 'User not found'
                    }), 404
                if user.role not in roles:
                    return jsonify({
                        'success': False, 
                        'message': f'Access forbidden. Required role: {", ".join(roles)}'
                    }), 403
                return f(*args, **kwargs)
            return decorated_function
        return decorator

    # --- Auth ---
    @app.route('/auth/register', methods=['POST'])
    def register():
        data = request.get_json() or {}
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'student')
        if not all([name, email, password]):
            return jsonify({'success': False, 'message': 'name, email and password required'}), 400
        if role not in ('student', 'faculty', 'admin'):
            return jsonify({'success': False, 'message': 'invalid role'}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'email already registered'}), 400
        pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User(name=name, email=email, password_hash=pw_hash, role=role)
        db.session.add(user)
        db.session.commit()
        return jsonify({'success': True, 'user': user.to_dict()}), 201

    @app.route('/auth/login', methods=['POST'])
    def login():
        try:
            data = request.get_json() or {}
            email = data.get('email')
            password = data.get('password')
            
            if not all([email, password]):
                return jsonify({
                    'success': False, 
                    'message': 'Email and password are required'
                }), 400
            
            user = User.query.filter_by(email=email).first()
            if not user:
                return jsonify({
                    'success': False, 
                    'message': 'Invalid email or password'
                }), 401
            
            if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                return jsonify({
                    'success': False, 
                    'message': 'Invalid email or password'
                }), 401
            
            # Use simple user ID as identity - MUST BE STRING!
            access_token = create_access_token(identity=str(user.id))
            
            print(f"[LOGIN SUCCESS] user={user.email} id={user.id} role={user.role}")
            
            return jsonify({
                'success': True, 
                'access_token': access_token, 
                'user': user.to_dict()
            })
        except Exception as e:
            print(f"[LOGIN ERROR] {e}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'success': False, 
                'message': 'Login failed. Please try again.'
            }), 500

    @app.route('/auth/validate-token', methods=['GET'])
    @jwt_required()
    def validate_token():
        """Validate if the current token is valid and return user info"""
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user:
                return jsonify({
                    'success': False,
                    'valid': False,
                    'message': 'User not found'
                }), 404
            
            return jsonify({
                'success': True,
                'valid': True,
                'user': user.to_dict()
            }), 200
        except Exception as e:
            print(f"[TOKEN VALIDATION ERROR] {e}")
            return jsonify({
                'success': False,
                'valid': False,
                'message': 'Token validation failed'
            }), 401

    @app.route('/debug/token', methods=['GET'])
    @jwt_required()
    def debug_token():
        """Debug endpoint: returns the decoded JWT claims and identity for the current token.
        Use this to confirm the token on the client matches what the server sees.
        """
        try:
            identity = get_jwt_identity()
            claims = get_jwt()
            user = User.query.get(int(identity))
            
            if not user:
                return jsonify({
                    'success': False, 
                    'message': 'User not found for token',
                    'valid': False
                }), 404
            
            return jsonify({
                'success': True, 
                'valid': True,
                'identity': identity, 
                'claims': claims,
                'user': user.to_dict()
            })
        except Exception as e:
            print(f"[DEBUG TOKEN ERROR] {e}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'success': False, 
                'message': 'Failed to decode token',
                'valid': False
            }), 500

    # --- Safe Zones CRUD ---
    @app.route('/safe_zones', methods=['GET'])
    def list_safe_zones():
        zones = SafeZone.query.all()
        return jsonify([z.to_dict() for z in zones])

    @app.route('/safe_zones', methods=['POST'])
    @jwt_required()
    def create_safe_zone():
        identity = get_jwt_identity()
        user = User.query.get(int(identity))
        # only faculty or admin can create
        if user.role not in ('faculty', 'admin'):
            return jsonify({'success': False, 'message': 'forbidden'}), 403
        data = request.get_json() or {}
        try:
            zone = SafeZone(
                name=data['name'],
                latitude=data['latitude'],
                longitude=data['longitude'],
                description=data.get('description')
            )
            db.session.add(zone)
            db.session.commit()
            return jsonify({'success': True, 'zone': zone.to_dict()}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 400

    @app.route('/safe_zones/<int:zone_id>', methods=['GET'])
    def get_safe_zone(zone_id):
        z = SafeZone.query.get(zone_id)
        if not z:
            return jsonify({'success': False, 'message': 'not found'}), 404
        return jsonify({'success': True, 'zone': z.to_dict()})

    @app.route('/safe_zones/<int:zone_id>', methods=['PUT'])
    @jwt_required()
    def update_safe_zone(zone_id):
        identity = get_jwt_identity()
        user = User.query.get(int(identity))
        if user.role not in ('faculty', 'admin'):
            return jsonify({'success': False, 'message': 'forbidden'}), 403
        data = request.get_json() or {}
        z = SafeZone.query.get(zone_id)
        if not z:
            return jsonify({'success': False, 'message': 'not found'}), 404
        z.name = data.get('name', z.name)
        z.latitude = data.get('latitude', z.latitude)
        z.longitude = data.get('longitude', z.longitude)
        z.description = data.get('description', z.description)
        db.session.commit()
        return jsonify({'success': True, 'zone': z.to_dict()})

    @app.route('/safe_zones/<int:zone_id>', methods=['DELETE'])
    @jwt_required()
    def delete_safe_zone(zone_id):
        identity = get_jwt_identity()
        user = User.query.get(int(identity))
        if user.role not in ('faculty', 'admin'):
            return jsonify({'success': False, 'message': 'forbidden'}), 403
        z = SafeZone.query.get(zone_id)
        if not z:
            return jsonify({'success': False, 'message': 'not found'}), 404
        db.session.delete(z)
        db.session.commit()
        return jsonify({'success': True, 'message': 'deleted'})

    # --- User Safe Zone Marking ---
    @app.route('/safe_zones/<int:zone_id>/mark', methods=['POST'])
    @jwt_required()
    def mark_safe_zone(zone_id):
        identity = get_jwt_identity()
        uid = int(identity)
        zone = SafeZone.query.get(zone_id)
        if not zone:
            return jsonify({'success': False, 'message': 'zone not found'}), 404
        existing = UserSafeZone.query.filter_by(user_id=uid, zone_id=zone_id).first()
        if existing:
            return jsonify({'success': True, 'marked': existing.to_dict()})
        usz = UserSafeZone(user_id=uid, zone_id=zone_id)
        db.session.add(usz)
        db.session.commit()
        
        # Log activity (non-critical)
        try:
            log_activity(uid, 'safe_zone', f"Marked safe zone: {zone.name}")
        except Exception as e:
            print(f"Failed to log activity: {e}")
        
        return jsonify({'success': True, 'marked': usz.to_dict()}), 201

    @app.route('/safe_zones/<int:zone_id>/mark', methods=['DELETE'])
    @jwt_required()
    def unmark_safe_zone(zone_id):
        identity = get_jwt_identity()
        uid = int(identity)
        existing = UserSafeZone.query.filter_by(user_id=uid, zone_id=zone_id).first()
        if not existing:
            return jsonify({'success': False, 'message': 'not marked'}), 404
        db.session.delete(existing)
        db.session.commit()
        return jsonify({'success': True, 'message': 'unmarked'})

    @app.route('/safe_zones/marked', methods=['GET'])
    @jwt_required()
    def get_marked_zones():
        identity = get_jwt_identity()
        uid = int(identity)
        marked = UserSafeZone.query.filter_by(user_id=uid).all()
        zones = []
        for m in marked:
            z = SafeZone.query.get(m.zone_id)
            if z:
                zd = z.to_dict()
                zd['marked_at'] = m.marked_at.isoformat() if m.marked_at else None
                zones.append(zd)
        return jsonify(zones)

    # --- Disasters CRUD ---
    @app.route('/disasters', methods=['GET'])
    def list_disasters():
        items = Disaster.query.all()
        return jsonify([i.to_dict() for i in items])

    @app.route('/disasters', methods=['POST'])
    @jwt_required()
    def create_disaster():
        identity = get_jwt_identity()
        user = User.query.get(int(identity))
        if user.role not in ('faculty', 'admin'):
            return jsonify({'success': False, 'message': 'forbidden'}), 403
        data = request.get_json() or {}
        try:
            d = Disaster(disaster_type=data['disaster_type'], info=data['info'], video_link=data.get('video_link'))
            db.session.add(d)
            db.session.commit()
            return jsonify({'success': True, 'disaster': d.to_dict()}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 400

    @app.route('/disasters/<int:d_id>', methods=['GET'])
    def get_disaster(d_id):
        d = Disaster.query.get(d_id)
        if not d:
            return jsonify({'success': False, 'message': 'not found'}), 404
        return jsonify({'success': True, 'disaster': d.to_dict()})

    @app.route('/disasters/<int:d_id>', methods=['PUT'])
    @jwt_required()
    def update_disaster(d_id):
        identity = get_jwt_identity()
        user = User.query.get(int(identity))
        if user.role not in ('faculty', 'admin'):
            return jsonify({'success': False, 'message': 'forbidden'}), 403
        d = Disaster.query.get(d_id)
        if not d:
            return jsonify({'success': False, 'message': 'not found'}), 404
        data = request.get_json() or {}
        d.disaster_type = data.get('disaster_type', d.disaster_type)
        d.info = data.get('info', d.info)
        d.video_link = data.get('video_link', d.video_link)
        db.session.commit()
        return jsonify({'success': True, 'disaster': d.to_dict()})

    @app.route('/disasters/<int:d_id>', methods=['DELETE'])
    @jwt_required()
    def delete_disaster(d_id):
        identity = get_jwt_identity()
        user = User.query.get(int(identity))
        if user.role not in ('faculty', 'admin'):
            return jsonify({'success': False, 'message': 'forbidden'}), 403
        d = Disaster.query.get(d_id)
        if not d:
            return jsonify({'success': False, 'message': 'not found'}), 404
        db.session.delete(d)
        db.session.commit()
        return jsonify({'success': True, 'message': 'deleted'})

    # --- Messaging ---
    @app.route('/messages', methods=['POST'])
    @jwt_required()
    def send_message():
        identity = get_jwt_identity()
        data = request.get_json() or {}
        sender_id = identity
        
        # Support both receiver_id and receiver_email
        receiver_id = data.get('receiver_id')
        receiver_email = data.get('receiver_email')
        text = data.get('message_text')
        
        if not text:
            return jsonify({'success': False, 'message': 'message_text required'}), 400
        
        # If email provided, look up user
        if receiver_email and not receiver_id:
            receiver = User.query.filter_by(email=receiver_email).first()
            if not receiver:
                return jsonify({'success': False, 'message': 'User with that email not found'}), 404
            receiver_id = receiver.id
        
        if not receiver_id:
            return jsonify({'success': False, 'message': 'receiver_id or receiver_email required'}), 400
            
        msg = Message(sender_id=sender_id, receiver_id=receiver_id, message_text=text)
        db.session.add(msg)
        db.session.commit()
        
        # Log activity (non-critical)
        try:
            receiver_user = User.query.get(receiver_id)
            log_activity(sender_id, 'message', f"Sent message to {receiver_user.email if receiver_user else 'user'}")
        except Exception as e:
            print(f"Failed to log activity: {e}")
        
        return jsonify({'success': True, 'message': msg.to_dict()}), 201

    @app.route('/messages/inbox', methods=['GET'])
    @jwt_required()
    def inbox():
        identity = get_jwt_identity()
        uid = int(identity)
        msgs = Message.query.filter_by(receiver_id=uid).order_by(Message.timestamp.desc()).all()
        # Include sender email
        result = []
        for m in msgs:
            msg_dict = m.to_dict()
            sender = User.query.get(m.sender_id)
            msg_dict['sender_email'] = sender.email if sender else None
            result.append(msg_dict)
        return jsonify(result)

    @app.route('/messages/sent', methods=['GET'])
    @jwt_required()
    def sent_messages():
        identity = get_jwt_identity()
        uid = int(identity)
        msgs = Message.query.filter_by(sender_id=uid).order_by(Message.timestamp.desc()).all()
        # Include receiver email
        result = []
        for m in msgs:
            msg_dict = m.to_dict()
            receiver = User.query.get(m.receiver_id)
            msg_dict['receiver_email'] = receiver.email if receiver else None
            result.append(msg_dict)
        return jsonify(result)

    @app.route('/messages/all', methods=['GET'])
    @jwt_required()
    def all_messages():
        identity = get_jwt_identity()
        user = User.query.get(int(identity))
        if user.role != 'admin':
            return jsonify({'success': False, 'message': 'admin only'}), 403
        msgs = Message.query.order_by(Message.timestamp.desc()).all()
        # Include sender and receiver emails
        result = []
        for m in msgs:
            msg_dict = m.to_dict()
            sender = User.query.get(m.sender_id)
            receiver = User.query.get(m.receiver_id)
            msg_dict['sender_email'] = sender.email if sender else None
            msg_dict['receiver_email'] = receiver.email if receiver else None
            result.append(msg_dict)
        return jsonify(result)

    # --- Progress tracking ---
    @app.route('/progress', methods=['POST'])
    @jwt_required()
    def create_or_update_progress():
        identity = get_jwt_identity()
        data = request.get_json() or {}
        user_id = data.get('user_id', identity)
        module_name = data.get('module_name')
        if not module_name:
            return jsonify({'success': False, 'message': 'module_name required'}), 400
        progress = Progress.query.filter_by(user_id=user_id, module_name=module_name).first()
        if not progress:
            progress = Progress(user_id=user_id, module_name=module_name, quiz_score=data.get('quiz_score', 0), completed=bool(data.get('completed', False)))
            db.session.add(progress)
        else:
            progress.quiz_score = data.get('quiz_score', progress.quiz_score)
            progress.completed = data.get('completed', progress.completed)
        db.session.commit()
        return jsonify({'success': True, 'progress': progress.to_dict()})

    @app.route('/progress/user/<int:user_id>', methods=['GET'])
    @jwt_required()
    def get_user_progress(user_id):
        items = Progress.query.filter_by(user_id=user_id).all()
        return jsonify([i.to_dict() for i in items])

    # --- Learning Modules ---
    @app.route('/modules', methods=['GET'])
    def list_modules():
        modules = Module.query.all()
        return jsonify([m.to_dict() for m in modules])

    @app.route('/modules/<int:m_id>', methods=['GET'])
    def get_module(m_id):
        module = Module.query.get(m_id)
        if not module:
            return jsonify({'success': False, 'message': 'not found'}), 404
        return jsonify(module.to_dict())

    @app.route('/modules', methods=['POST'])
    @jwt_required()
    def create_module():
        identity = get_jwt_identity()
        user = User.query.get(int(identity))
        if user.role not in ('faculty', 'admin'):
            return jsonify({'success': False, 'message': 'forbidden'}), 403
        data = request.get_json() or {}
        module = Module(
            title=data['title'],
            description=data.get('description'),
            content=data['content'],
            difficulty=data.get('difficulty', 'beginner'),
            points=data.get('points', 100),
            quiz_questions=json.dumps(data.get('quiz_questions', []))
        )
        db.session.add(module)
        db.session.commit()
        
        # Log activity (non-critical)
        try:
            log_activity(identity, 'module', f"Created module: {module.title}")
        except Exception as e:
            print(f"Failed to log activity: {e}")
        
        return jsonify({'success': True, 'module': module.to_dict()}), 201

    @app.route('/modules/<int:m_id>', methods=['PUT'])
    @jwt_required()
    def update_module(m_id):
        identity = get_jwt_identity()
        user = User.query.get(int(identity))
        if user.role not in ('faculty', 'admin'):
            return jsonify({'success': False, 'message': 'forbidden'}), 403
        module = Module.query.get(m_id)
        if not module:
            return jsonify({'success': False, 'message': 'not found'}), 404
        data = request.get_json() or {}
        module.title = data.get('title', module.title)
        module.description = data.get('description', module.description)
        module.content = data.get('content', module.content)
        module.difficulty = data.get('difficulty', module.difficulty)
        module.points = data.get('points', module.points)
        if 'quiz_questions' in data:
            module.quiz_questions = json.dumps(data['quiz_questions'])
        db.session.commit()
        return jsonify({'success': True, 'module': module.to_dict()})

    @app.route('/modules/<int:m_id>', methods=['DELETE'])
    @jwt_required()
    def delete_module(m_id):
        identity = get_jwt_identity()
        user = User.query.get(int(identity))
        if user.role not in ('faculty', 'admin'):
            return jsonify({'success': False, 'message': 'forbidden'}), 403
        module = Module.query.get(m_id)
        if not module:
            return jsonify({'success': False, 'message': 'not found'}), 404
        db.session.delete(module)
        db.session.commit()
        return jsonify({'success': True, 'message': 'deleted'})

    @app.route('/modules/<int:m_id>/attempt', methods=['POST'])
    @jwt_required()
    def attempt_module(m_id):
        identity = get_jwt_identity()
        uid = int(identity)
        module = Module.query.get(m_id)
        if not module:
            return jsonify({'success': False, 'message': 'module not found'}), 404
        data = request.get_json() or {}
        answers = data.get('answers', [])
        # module.quiz_questions stored as JSON list of {question, options, correctIndex}
        try:
            qlist = json.loads(module.quiz_questions or '[]')
        except Exception:
            qlist = []
        score = 0
        total = len(qlist)
        for i, q in enumerate(qlist):
            correct = q.get('correctIndex')
            ans = answers[i] if i < len(answers) else None
            if ans is not None and int(ans) == int(correct):
                score += 1

        percent = int((score / total) * 100) if total > 0 else 0
        points_earned = int(module.points * (score / total)) if total > 0 else 0

        # create achievement record and update progress
        ach = UserAchievement(user_id=uid, achievement_type='module_completion', title=f'Completed {module.title}', description=f'Score {percent}%', points=points_earned)
        db.session.add(ach)
        progress = Progress.query.filter_by(user_id=uid, module_name=module.title).first()
        if not progress:
            progress = Progress(user_id=uid, module_name=module.title, quiz_score=percent, completed=(percent>=50), user_answers=json.dumps(answers), module_id=m_id)
            db.session.add(progress)
        else:
            progress.quiz_score = percent
            progress.completed = progress.completed or (percent>=50)
            progress.user_answers = json.dumps(answers)
            progress.module_id = m_id

        # Log quiz completion to recent activity
        log_activity(uid, 'quiz', f"Completed quiz: {module.title} - Score: {percent}%")

        db.session.commit()
        return jsonify({'success': True, 'score': percent, 'points': points_earned, 'correct': score, 'total': total})

    @app.route('/modules/<int:m_id>/results', methods=['GET'])
    @jwt_required()
    def get_module_results(m_id):
        identity = get_jwt_identity()
        user = User.query.get(int(identity))
        module = Module.query.get(m_id)
        if not module:
            return jsonify({'success': False, 'message': 'module not found'}), 404
        
        # Admin and faculty can view any results, students can only view their own completed results
        if user.role in ('admin', 'faculty'):
            # Get all progress records for this module
            all_progress = Progress.query.filter_by(module_id=m_id).all()
            results = []
            for prog in all_progress:
                student = User.query.get(prog.user_id)
                results.append({
                    'user_id': prog.user_id,
                    'user_name': student.name if student else 'Unknown',
                    'user_email': student.email if student else 'Unknown',
                    'score': prog.quiz_score,
                    'completed': prog.completed,
                    'user_answers': json.loads(prog.user_answers) if prog.user_answers else []
                })
            return jsonify({
                'success': True, 
                'module': module.to_dict(),
                'quiz_questions': json.loads(module.quiz_questions or '[]'),
                'results': results,
                'is_admin_or_faculty': True
            })
        else:
            # Student - only their own results if completed
            progress = Progress.query.filter_by(user_id=int(identity), module_id=m_id).first()
            if not progress or not progress.completed:
                return jsonify({'success': False, 'message': 'You have not completed this quiz yet'}), 403
            
            return jsonify({
                'success': True,
                'module': module.to_dict(),
                'quiz_questions': json.loads(module.quiz_questions or '[]'),
                'user_answers': json.loads(progress.user_answers) if progress.user_answers else [],
                'score': progress.quiz_score,
                'is_admin_or_faculty': False
            })

    # --- Virtual Drills ---
    @app.route('/drills', methods=['GET'])
    def list_drills():
        drills = Drill.query.all()
        return jsonify([d.to_dict() for d in drills])

    @app.route('/drills/<int:d_id>', methods=['GET'])
    def get_drill(d_id):
        drill = Drill.query.get(d_id)
        if not drill:
            return jsonify({'success': False, 'message': 'not found'}), 404
        return jsonify(drill.to_dict())

    @app.route('/drills', methods=['POST'])
    @jwt_required()
    def create_drill():
        identity = get_jwt_identity()
        user = User.query.get(int(identity))
        if user.role not in ('faculty', 'admin'):
            return jsonify({'success': False, 'message': 'forbidden'}), 403
        data = request.get_json() or {}
        drill = Drill(
            title=data['title'],
            description=data.get('description'),
            drill_type=data.get('drill_type'),
            steps=json.dumps(data.get('steps', [])),
            duration_minutes=data.get('duration_minutes', 15),
            scheduled_date=datetime.fromisoformat(data['scheduled_date']) if data.get('scheduled_date') else None,
            created_by=identity
        )
        db.session.add(drill)
        db.session.commit()
        return jsonify({'success': True, 'drill': drill.to_dict()}), 201

    @app.route('/drills/<int:d_id>/participate', methods=['POST'])
    @jwt_required()
    def participate_in_drill(d_id):
        identity = get_jwt_identity()
        data = request.get_json() or {}
        drill = Drill.query.get(d_id)
        participation = DrillParticipation(
            drill_id=d_id,
            user_id=int(identity),
            completed=data.get('completed', False),
            score=data.get('score', 0.0),
            completion_time=datetime.utcnow() if data.get('completed') else None
        )
        db.session.add(participation)
        db.session.commit()
        
        # Log activity if completed (non-critical)
        try:
            if data.get('completed'):
                log_activity(identity, 'drill', f"Completed drill: {drill.title if drill else 'Unknown'}")
        except Exception as e:
            print(f"Failed to log activity: {e}")
        
        return jsonify({'success': True, 'participation': participation.to_dict()}), 201

    @app.route('/drills/my-participation', methods=['GET'])
    @jwt_required()
    def get_my_drill_participation():
        identity = get_jwt_identity()
        participations = DrillParticipation.query.filter_by(user_id=int(identity)).all()
        # Return both full participation data and a list of completed drill IDs
        completed_drill_ids = [p.drill_id for p in participations if p.completed]
        return jsonify({
            'participations': [p.to_dict() for p in participations],
            'drill_ids': completed_drill_ids
        })

    # --- Alerts ---
    @app.route('/alerts', methods=['GET'])
    def list_alerts():
        active = request.args.get('active', 'true').lower() == 'true'
        query = Alert.query.filter_by(active=True) if active else Alert.query
        alerts = query.order_by(Alert.created_at.desc()).all()
        return jsonify([a.to_dict() for a in alerts])

    @app.route('/alerts/<int:a_id>', methods=['GET'])
    def get_alert(a_id):
        alert = Alert.query.get(a_id)
        if not alert:
            return jsonify({'success': False, 'message': 'not found'}), 404
        return jsonify(alert.to_dict())

    @app.route('/alerts', methods=['POST'])
    @jwt_required()
    def create_alert():
        identity = get_jwt_identity()
        user = User.query.get(int(identity))
        if user.role not in ('faculty', 'admin'):
            return jsonify({'success': False, 'message': 'forbidden'}), 403
        data = request.get_json() or {}
        alert = Alert(
            title=data['title'],
            message=data['message'],
            alert_type=data.get('alert_type', 'info'),
            severity=data.get('severity', 'medium'),
            region=data.get('region'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            radius_km=data.get('radius_km', 10.0),
            expires_at=datetime.fromisoformat(data['expires_at']) if data.get('expires_at') else None,
            created_by=identity
        )
        db.session.add(alert)
        db.session.commit()
        return jsonify({'success': True, 'alert': alert.to_dict()}), 201

    @app.route('/alerts/<int:a_id>', methods=['PUT'])
    @jwt_required()
    def update_alert(a_id):
        identity = get_jwt_identity()
        user = User.query.get(int(identity))
        if user.role not in ('faculty', 'admin'):
            return jsonify({'success': False, 'message': 'forbidden'}), 403
        alert = Alert.query.get(a_id)
        if not alert:
            return jsonify({'success': False, 'message': 'not found'}), 404
        data = request.get_json() or {}
        alert.active = data.get('active', alert.active)
        db.session.commit()
        return jsonify({'success': True, 'alert': alert.to_dict()})

    @app.route('/alerts/<int:a_id>', methods=['DELETE'])
    @jwt_required()
    def delete_alert(a_id):
        identity = get_jwt_identity()
        user = User.query.get(int(identity))
        if user.role not in ('faculty', 'admin'):
            return jsonify({'success': False, 'message': 'forbidden'}), 403
        alert = Alert.query.get(a_id)
        if not alert:
            return jsonify({'success': False, 'message': 'not found'}), 404
        db.session.delete(alert)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Alert deleted'})

    # --- Emergency Contacts ---
    @app.route('/emergency-contacts', methods=['GET'])
    def list_emergency_contacts():
        category = request.args.get('category')
        region = request.args.get('region')
        query = EmergencyContact.query
        if category:
            query = query.filter_by(category=category)
        if region:
            query = query.filter_by(region=region)
        contacts = query.all()
        return jsonify([c.to_dict() for c in contacts])

    @app.route('/emergency-contacts', methods=['POST'])
    @jwt_required()
    def create_emergency_contact():
        identity = get_jwt_identity()
        user = User.query.get(int(identity))
        if user.role not in ('faculty', 'admin'):
            return jsonify({'success': False, 'message': 'forbidden'}), 403
        data = request.get_json() or {}
        contact = EmergencyContact(
            name=data['name'],
            organization=data.get('organization'),
            phone=data['phone'],
            email=data.get('email'),
            category=data.get('category'),
            region=data.get('region'),
            available_24_7=data.get('available_24_7', True)
        )
        db.session.add(contact)
        db.session.commit()
        return jsonify({'success': True, 'contact': contact.to_dict()}), 201

    # --- User Achievements & Gamification ---
    @app.route('/achievements/my', methods=['GET'])
    @jwt_required()
    def get_my_achievements():
        identity = get_jwt_identity()
        achievements = UserAchievement.query.filter_by(user_id=int(identity)).all()
        return jsonify([a.to_dict() for a in achievements])

    @app.route('/leaderboard', methods=['GET'])
    def get_leaderboard():
        # Calculate total points per user from achievements
        from sqlalchemy import func
        leaderboard = db.session.query(
            User.id,
            User.name,
            func.sum(UserAchievement.points).label('total_points')
        ).join(UserAchievement, User.id == UserAchievement.user_id)\
         .group_by(User.id, User.name)\
         .order_by(func.sum(UserAchievement.points).desc())\
         .limit(100)\
         .all()
        
        return jsonify([{
            'user_id': user_id,
            'name': name,
            'total_points': int(total_points) if total_points else 0
        } for user_id, name, total_points in leaderboard])

    # --- Analytics Dashboard (Admin) ---
    @app.route('/analytics/overview', methods=['GET'])
    @jwt_required()
    def get_analytics_overview():
        identity = get_jwt_identity()
        print(f"[ANALYTICS] identity={identity} type={type(identity)}")
        user = User.query.get(int(identity))
        print(f"[ANALYTICS] user={user} role={user.role if user else None}")
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        if user.role != 'admin':
            return jsonify({'success': False, 'message': 'admin only'}), 403
        
        total_users = User.query.count()
        total_students = User.query.filter_by(role='student').count()
        total_modules = Module.query.count()
        total_drills = Drill.query.count()
        total_drill_participations = DrillParticipation.query.filter_by(completed=True).count()
        active_alerts = Alert.query.filter_by(active=True).count()
        
        # Enhanced preparedness score calculation
        # Components: Quizzes (40%), Drills (30%), Safe Zones (20%), Messages (10%)
        
        if total_students > 0:
            # 1. Quiz completion (40%)
            students_with_progress = db.session.query(Progress.user_id)\
                .join(User, User.id == Progress.user_id)\
                .filter(User.role == 'student')\
                .distinct().count()
            quiz_score = (students_with_progress / total_students) * 40
            
            # 2. Drill completion (30%)
            students_with_drills = db.session.query(DrillParticipation.user_id)\
                .join(User, User.id == DrillParticipation.user_id)\
                .filter(User.role == 'student')\
                .filter(DrillParticipation.completed == True)\
                .distinct().count()
            drill_score = (students_with_drills / total_students) * 30
            
            # 3. Safe zone knowledge (20%)
            students_with_safezones = db.session.query(UserSafeZone.user_id)\
                .join(User, User.id == UserSafeZone.user_id)\
                .filter(User.role == 'student')\
                .distinct().count()
            safezone_score = (students_with_safezones / total_students) * 20
            
            # 4. Communication/messages (10%)
            students_with_messages = db.session.query(Message.sender_id)\
                .join(User, User.id == Message.sender_id)\
                .filter(User.role == 'student')\
                .distinct().count()
            message_score = (students_with_messages / total_students) * 10
            
            preparedness_score = quiz_score + drill_score + safezone_score + message_score
        else:
            preparedness_score = 0
        
        return jsonify({
            'total_users': total_users,
            'total_students': total_students,
            'total_modules': total_modules,
            'total_drills': total_drills,
            'drill_participations': total_drill_participations,
            'active_alerts': active_alerts,
            'preparedness_score': round(preparedness_score, 2)
        })

    # --- User listings for faculty/admin ---
    @app.route('/users', methods=['GET'])
    @jwt_required()
    def list_users():
        identity = get_jwt_identity()
        print(f"[LIST USERS] identity={identity} type={type(identity)}")
        user = User.query.get(int(identity))
        print(f"[LIST USERS] user={user} role={user.role if user else None}")
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        if user.role != 'admin':
            return jsonify({'success': False, 'message': 'admin only'}), 403
        users = User.query.all()
        return jsonify([u.to_dict() for u in users])

    @app.route('/users/students', methods=['GET'])
    @jwt_required()
    def list_students():
        identity = get_jwt_identity()
        print(f"[LIST STUDENTS] identity={identity} type={type(identity)}")
        user = User.query.get(int(identity))
        print(f"[LIST STUDENTS] user={user} role={user.role if user else None}")
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        if user.role not in ('faculty', 'admin'):
            return jsonify({'success': False, 'message': 'forbidden'}), 403
        users = User.query.filter_by(role='student').all()
        return jsonify([u.to_dict() for u in users])

    @app.route('/users/faculty', methods=['GET'])
    @jwt_required()
    def list_faculty():
        identity = get_jwt_identity()
        user = User.query.get(int(identity))
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        if user.role != 'admin':
            return jsonify({'success': False, 'message': 'admin only'}), 403
        users = User.query.filter_by(role='faculty').all()
        return jsonify([u.to_dict() for u in users])

    @app.route('/users/<int:user_id>', methods=['DELETE'])
    @jwt_required()
    def delete_user(user_id):
        identity = get_jwt_identity()
        user = User.query.get(int(identity))
        if user.role != 'admin':
            return jsonify({'success': False, 'message': 'admin only'}), 403
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'message': 'user not found'}), 404
        # Don't allow deleting yourself
        if user.id == identity:
            return jsonify({'success': False, 'message': 'cannot delete yourself'}), 400
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True, 'message': 'user deleted'})

    @app.route('/users/<int:user_id>/reset-password', methods=['POST'])
    @jwt_required()
    def admin_reset_password(user_id):
        """Admin endpoint to reset a user's password"""
        try:
            identity = get_jwt_identity()
            admin = User.query.get(int(identity))
            
            if not admin or admin.role != 'admin':
                return jsonify({
                    'success': False, 
                    'message': 'Admin access required'
                }), 403
            
            user = User.query.get(user_id)
            if not user:
                return jsonify({
                    'success': False, 
                    'message': 'User not found'
                }), 404
            
            data = request.get_json() or {}
            new_password = data.get('new_password')
            
            if not new_password or len(new_password) < 6:
                return jsonify({
                    'success': False, 
                    'message': 'New password must be at least 6 characters'
                }), 400
            
            # Hash the new password
            pw_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user.password_hash = pw_hash
            db.session.commit()
            
            print(f"[ADMIN ACTION] Admin {admin.email} reset password for user {user.email}")
            
            return jsonify({
                'success': True, 
                'message': f'Password reset successfully for {user.email}'
            })
        except Exception as e:
            print(f"[ERROR] Password reset failed: {e}")
            return jsonify({
                'success': False, 
                'message': 'Failed to reset password'
            }), 500

    # Helper function to log activities
    def log_activity(user_id, activity_type, description):
        try:
            activity = RecentActivity(
                user_id=user_id,
                activity_type=activity_type,
                description=description
            )
            db.session.add(activity)
            db.session.commit()
        except Exception as e:
            print(f"Error logging activity: {e}")
            db.session.rollback()

    @app.route('/activities/recent', methods=['GET'])
    @jwt_required()
    def get_recent_activities():
        try:
            print("[ACTIVITIES] Endpoint called")
            identity = get_jwt_identity()  # This is now a STRING
            print(f"[ACTIVITIES] JWT identity: {identity} type: {type(identity)}")
            
            user_id = int(identity)  # Convert string to int for database query
            user = User.query.get(user_id)
            print(f"[ACTIVITIES] User found: {user is not None}")
            
            if not user:
                return jsonify({'success': False, 'message': 'User not found'}), 404
            
            user_role = user.role
            print(f"[ACTIVITIES] User role: {user_role}")
            
            # Check if RecentActivity table exists
            try:
                # Admin can see all activities, others see only their own
                if user_role == 'admin':
                    activities = RecentActivity.query.order_by(RecentActivity.created_at.desc()).limit(20).all()
                else:
                    activities = RecentActivity.query.filter_by(user_id=user_id).order_by(RecentActivity.created_at.desc()).limit(10).all()
                
                print(f"[ACTIVITIES] Found {len(activities)} activities")
                return jsonify({'success': True, 'activities': [a.to_dict() for a in activities]})
            except Exception as db_error:
                # If table doesn't exist or query fails, return empty list
                print(f"[ACTIVITIES] Database error (table might not exist): {db_error}")
                return jsonify({'success': True, 'activities': []})
                
        except Exception as e:
            print(f"[ACTIVITIES ERROR] {e}")
            import traceback
            traceback.print_exc()
            return jsonify({'success': False, 'message': str(e)}), 500


    return app


if __name__ == '__main__':
    # create app and run
    app = create_app()
    # When running locally ensure the DB exists and tables can be created
    with app.app_context():
        db.create_all()
        # Seed initial safe zones for India and emergency contacts/modules if empty
        try:
            if SafeZone.query.count() == 0:
                # Comprehensive region-wise safe zones for all Indian states and major cities
                india_zones = [
                    # North India
                    ('Delhi - Connaught Place Safe Zone', 28.6139, 77.2090, 'Delhi'),
                    ('Delhi - Dwarka Safe Zone', 28.5921, 77.0460, 'Delhi'),
                    ('Chandigarh Safe Zone', 30.7333, 76.7794, 'Chandigarh'),
                    ('Jaipur - Pink City Safe Zone', 26.9124, 75.7873, 'Rajasthan'),
                    ('Jodhpur Safe Zone', 26.2389, 73.0243, 'Rajasthan'),
                    ('Udaipur Safe Zone', 24.5854, 73.7125, 'Rajasthan'),
                    ('Lucknow - Hazratganj Safe Zone', 26.8467, 80.9462, 'Uttar Pradesh'),
                    ('Varanasi Safe Zone', 25.3176, 82.9739, 'Uttar Pradesh'),
                    ('Agra - Taj Safe Zone', 27.1767, 78.0081, 'Uttar Pradesh'),
                    ('Amritsar - Golden Temple Safe Zone', 31.6340, 74.8723, 'Punjab'),
                    ('Shimla Safe Zone', 31.1048, 77.1734, 'Himachal Pradesh'),
                    ('Dehradun Safe Zone', 30.3165, 78.0322, 'Uttarakhand'),
                    
                    # South India
                    ('Mumbai - Marine Drive Safe Zone', 19.0760, 72.8777, 'Maharashtra'),
                    ('Mumbai - Bandra Safe Zone', 19.0596, 72.8295, 'Maharashtra'),
                    ('Pune - Shivajinagar Safe Zone', 18.5204, 73.8567, 'Maharashtra'),
                    ('Bengaluru - MG Road Safe Zone', 12.9716, 77.5946, 'Karnataka'),
                    ('Bengaluru - Electronic City Safe Zone', 12.8456, 77.6603, 'Karnataka'),
                    ('Mysuru Safe Zone', 12.2958, 76.6394, 'Karnataka'),
                    ('Chennai - Marina Beach Safe Zone', 13.0827, 80.2707, 'Tamil Nadu'),
                    ('Chennai - T Nagar Safe Zone', 13.0418, 80.2341, 'Tamil Nadu'),
                    ('Coimbatore Safe Zone', 11.0168, 76.9558, 'Tamil Nadu'),
                    ('Hyderabad - Charminar Safe Zone', 17.3850, 78.4867, 'Telangana'),
                    ('Hyderabad - Hi-Tech City Safe Zone', 17.4485, 78.3908, 'Telangana'),
                    ('Kochi Safe Zone', 9.9312, 76.2673, 'Kerala'),
                    ('Thiruvananthapuram Safe Zone', 8.5241, 76.9366, 'Kerala'),
                    ('Visakhapatnam Safe Zone', 17.6868, 83.2185, 'Andhra Pradesh'),
                    ('Vijayawada Safe Zone', 16.5062, 80.6480, 'Andhra Pradesh'),
                    
                    # East India
                    ('Kolkata - Park Street Safe Zone', 22.5726, 88.3639, 'West Bengal'),
                    ('Kolkata - Salt Lake Safe Zone', 22.5804, 88.4299, 'West Bengal'),
                    ('Darjeeling Safe Zone', 27.0360, 88.2627, 'West Bengal'),
                    ('Bhubaneswar Safe Zone', 20.2961, 85.8245, 'Odisha'),
                    ('Patna Safe Zone', 25.5941, 85.1376, 'Bihar'),
                    ('Ranchi Safe Zone', 23.3441, 85.3096, 'Jharkhand'),
                    ('Guwahati Safe Zone', 26.1445, 91.7362, 'Assam'),
                    ('Imphal Safe Zone', 24.8170, 93.9368, 'Manipur'),
                    ('Agartala Safe Zone', 23.8315, 91.2868, 'Tripura'),
                    
                    # West India
                    ('Ahmedabad - Sabarmati Safe Zone', 23.0225, 72.5714, 'Gujarat'),
                    ('Surat Safe Zone', 21.1702, 72.8311, 'Gujarat'),
                    ('Vadodara Safe Zone', 22.3072, 73.1812, 'Gujarat'),
                    ('Indore Safe Zone', 22.7196, 75.8577, 'Madhya Pradesh'),
                    ('Bhopal Safe Zone', 23.2599, 77.4126, 'Madhya Pradesh'),
                    ('Goa - Panaji Safe Zone', 15.4909, 73.8278, 'Goa'),
                    
                    # Central India
                    ('Nagpur Safe Zone', 21.1458, 79.0882, 'Maharashtra'),
                    ('Raipur Safe Zone', 21.2514, 81.6296, 'Chhattisgarh'),
                    ('Jabalpur Safe Zone', 23.1815, 79.9864, 'Madhya Pradesh'),
                    
                    # Northeast India
                    ('Shillong Safe Zone', 25.5788, 91.8933, 'Meghalaya'),
                    ('Aizawl Safe Zone', 23.7307, 92.7173, 'Mizoram'),
                    ('Itanagar Safe Zone', 27.0844, 93.6053, 'Arunachal Pradesh'),
                    ('Gangtok Safe Zone', 27.3389, 88.6065, 'Sikkim'),
                ]
                for name, lat, lng, state in india_zones:
                    z = SafeZone(
                        name=name, 
                        latitude=lat, 
                        longitude=lng, 
                        description=f'Designated disaster preparedness safe zone in {state}. Equipped with emergency supplies and shelter facilities.'
                    )
                    db.session.add(z)
                db.session.commit()
                print(f"[OK] Seeded {len(india_zones)} region-wise safe zones across India")

            if EmergencyContact.query.count() == 0:
                contacts = [
                    ('Ambulance', 'Ambulance Services', '102', '', 'medical', 'India', True),
                    ('Police', 'Local Police', '100', '', 'police', 'India', True),
                    ('Fire', 'Fire Department', '101', '', 'fire', 'India', True),
                    ('NDRF', 'National Disaster Response Force', '+91-011-2436-1234', '', 'rescue', 'India', True),
                    ('Local Red Cross', 'Red Cross', '+91-11-xxxx-xxxx', '', 'ngo', 'India', True)
                ]
                for name, org, phone, email, category, region, avail in contacts:
                    c = EmergencyContact(name=name, organization=org, phone=phone, email=email, category=category, region=region, available_24_7=avail)
                    db.session.add(c)
                db.session.commit()

            # Modules are created by faculty/admin through the UI
            # No auto-seeded modules
        except Exception as se:
            db.session.rollback()
            print('Seeding error:', se)
    app.run(host='0.0.0.0', port=5000, debug=True)
