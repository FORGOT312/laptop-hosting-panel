"""
API endpoints для управления серверами
"""

from flask import Blueprint, jsonify, request
from core.server_manager import ServerManager

servers_bp = Blueprint('servers', __name__)
server_manager = ServerManager()

@servers_bp.route('', methods=['GET'])
def list_servers():
    """Получить список всех серверов"""
    try:
        servers = server_manager.list_servers()
        return jsonify(servers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@servers_bp.route('/<server_id>', methods=['GET'])
def get_server(server_id):
    """Получить информацию о сервере"""
    server = server_manager.get_server(server_id)
    
    if not server:
        return jsonify({'error': 'Server not found'}), 404
    
    return jsonify(server.to_dict())

@servers_bp.route('', methods=['POST'])
def create_server():
    """Создать новый сервер"""
    data = request.get_json()
    
    required_fields = ['name', 'command', 'working_dir']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        server = server_manager.create_server(
            name=data['name'],
            command=data['command'],
            working_dir=data['working_dir'],
            port=data.get('port'),
            auto_start=data.get('auto_start', False)
        )
        
        return jsonify(server.to_dict()), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@servers_bp.route('/<server_id>', methods=['DELETE'])
def delete_server(server_id):
    """Удалить сервер"""
    success = server_manager.delete_server(server_id)
    
    if not success:
        return jsonify({'error': 'Server not found'}), 404
    
    return jsonify({'message': 'Server deleted successfully'})

@servers_bp.route('/<server_id>/start', methods=['POST'])
def start_server(server_id):
    """Запустить сервер"""
    success = server_manager.start_server(server_id)
    
    if not success:
        return jsonify({'error': 'Failed to start server'}), 500
    
    return jsonify({'message': 'Server started successfully'})

@servers_bp.route('/<server_id>/stop', methods=['POST'])
def stop_server(server_id):
    """Остановить сервер"""
    success = server_manager.stop_server(server_id)
    
    if not success:
        return jsonify({'error': 'Failed to stop server'}), 500
    
    return jsonify({'message': 'Server stopped successfully'})

@servers_bp.route('/<server_id>/restart', methods=['POST'])
def restart_server(server_id):
    """Перезапустить сервер"""
    success = server_manager.restart_server(server_id)
    
    if not success:
        return jsonify({'error': 'Failed to restart server'}), 500
    
    return jsonify({'message': 'Server restarted successfully'})

@servers_bp.route('/<server_id>/command', methods=['POST'])
def send_command(server_id):
    """Отправить команду в консоль сервера"""
    data = request.get_json()
    command = data.get('command')
    
    if not command:
        return jsonify({'error': 'Command is required'}), 400
    
    success = server_manager.send_command(server_id, command)
    
    if not success:
        return jsonify({'error': 'Failed to send command'}), 500
    
    return jsonify({'message': 'Command sent successfully'})

@servers_bp.route('/<server_id>/console', methods=['GET'])
def get_console(server_id):
    """Получить вывод консоли"""
    lines = request.args.get('lines', 100, type=int)
    
    output = server_manager.get_console_output(server_id, lines)
    
    return jsonify({'output': output})

@servers_bp.route('/<server_id>/stats', methods=['GET'])
def get_server_stats(server_id):
    """Получить статистику сервера"""
    server = server_manager.get_server(server_id)
    
    if not server:
        return jsonify({'error': 'Server not found'}), 404
    
    stats = server.get_stats()
    return jsonify(stats)
