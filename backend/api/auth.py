"""
API endpoints для аутентификации
"""

from flask import Blueprint, jsonify, request, session
import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from functools import wraps

auth_bp = Blueprint('auth', __name__)

# Временное хранилище пользователей (в продакшене использовать БД)
USERS = {
    'admin': {
        'password': bcrypt.hashpw('admin'.encode(), bcrypt.gensalt()).decode(),
        'role': 'admin'
    }
}

SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')

def token_required(f):
    """Декоратор для проверки токена"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = data['username']
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

@auth_bp.route('/login', methods=['POST'])
def login():
    """Вход в систему"""
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    user = USERS.get(username)
    
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Проверка пароля
    if not bcrypt.checkpw(password.encode(), user['password'].encode()):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Генерация токена
    token = jwt.encode({
        'username': username,
        'role': user['role'],
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, SECRET_KEY, algorithm='HS256')
    
    return jsonify({
        'token': token,
        'username': username,
        'role': user['role']
    })

@auth_bp.route('/register', methods=['POST'])
def register():
    """Регистрация нового пользователя"""
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    if username in USERS:
        return jsonify({'error': 'User already exists'}), 409
    
    # Хеширование пароля
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    USERS[username] = {
        'password': hashed_password.decode(),
        'role': 'user'
    }
    
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/verify', methods=['GET'])
@token_required
def verify_token(current_user):
    """Проверка токена"""
    return jsonify({
        'valid': True,
        'username': current_user
    })

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Выход из системы"""
    # В случае с JWT токены хранятся на клиенте
    # Клиент просто удаляет токен
    return jsonify({'message': 'Logged out successfully'})
