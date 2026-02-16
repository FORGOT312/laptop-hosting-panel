#!/usr/bin/env python3
"""
Laptop Hosting Panel - Backend Server
Управление серверами и приложениями через веб-интерфейс
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import json
from datetime import datetime
from dotenv import load_dotenv

from core.server_manager import ServerManager
from core.system_monitor import SystemMonitor
from api.auth import auth_bp
from api.servers import servers_bp
from models.database import init_db

# Загрузка переменных окружения
load_dotenv()

# Инициализация Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DATABASE_PATH'] = os.getenv('DATABASE_PATH', './data/panel.db')

# CORS для разработки
CORS(app, resources={r"/api/*": {"origins": "*"}})

# WebSocket для real-time обновлений
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Инициализация менеджеров
server_manager = ServerManager()
system_monitor = SystemMonitor()

# Инициализация БД
init_db(app.config['DATABASE_PATH'])

# Регистрация blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(servers_bp, url_prefix='/api/servers')

# === ОСНОВНЫЕ МАРШРУТЫ ===

@app.route('/')
def index():
    """Главная страница API"""
    return jsonify({
        'name': 'Laptop Hosting Panel API',
        'version': '1.0.0',
        'status': 'running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/health')
def health():
    """Проверка здоровья системы"""
    return jsonify({
        'status': 'healthy',
        'uptime': system_monitor.get_uptime(),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/system/stats')
def system_stats():
    """Получить статистику системы"""
    try:
        stats = system_monitor.get_system_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/processes')
def list_processes():
    """Список всех процессов"""
    try:
        processes = system_monitor.get_processes()
        return jsonify(processes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# === WEBSOCKET СОБЫТИЯ ===

@socketio.on('connect')
def handle_connect():
    """Клиент подключился"""
    print(f'Client connected: {request.sid}')
    emit('connection_response', {'status': 'connected'})

@socketio.on('disconnect')
def handle_disconnect():
    """Клиент отключился"""
    print(f'Client disconnected: {request.sid}')

@socketio.on('subscribe_stats')
def handle_subscribe_stats():
    """Подписка на обновления статистики"""
    print(f'Client {request.sid} subscribed to stats')
    # Отправляем начальные данные
    stats = system_monitor.get_system_stats()
    emit('stats_update', stats)

@socketio.on('subscribe_console')
def handle_subscribe_console(data):
    """Подписка на консоль сервера"""
    server_id = data.get('server_id')
    if server_id:
        print(f'Client {request.sid} subscribed to console of server {server_id}')
        # TODO: Подключить к выводу консоли сервера

@socketio.on('send_command')
def handle_command(data):
    """Отправка команды в консоль сервера"""
    server_id = data.get('server_id')
    command = data.get('command')
    
    if not server_id or not command:
        emit('command_error', {'error': 'Missing server_id or command'})
        return
    
    try:
        result = server_manager.send_command(server_id, command)
        emit('command_sent', {'server_id': server_id, 'command': command, 'result': result})
    except Exception as e:
        emit('command_error', {'error': str(e)})

# === ФОНОВЫЕ ЗАДАЧИ ===

def broadcast_stats():
    """Рассылка статистики всем подключенным клиентам"""
    while True:
        socketio.sleep(2)  # Обновление каждые 2 секунды
        try:
            stats = system_monitor.get_system_stats()
            socketio.emit('stats_update', stats, broadcast=True)
        except Exception as e:
            print(f'Error broadcasting stats: {e}')

# Запуск фоновой задачи
socketio.start_background_task(broadcast_stats)

# === ОБРАБОТЧИКИ ОШИБОК ===

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Создание необходимых директорий
    os.makedirs('./data', exist_ok=True)
    os.makedirs('./logs', exist_ok=True)
    os.makedirs('./servers', exist_ok=True)
    
    # Запуск сервера
    print('🚀 Starting Laptop Hosting Panel...')
    print('📡 Backend running on http://localhost:5000')
    print('🔌 WebSocket available on ws://localhost:5000')
    
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=True,
        allow_unsafe_werkzeug=True
    )
