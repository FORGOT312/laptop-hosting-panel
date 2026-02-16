"""
Server Manager - управление серверами/приложениями
"""

import subprocess
import os
import signal
import psutil
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import threading
import queue

class ServerManager:
    """Класс для управления серверами"""
    
    def __init__(self, servers_dir: str = './servers'):
        self.servers_dir = servers_dir
        self.servers: Dict[str, 'Server'] = {}
        self.load_servers()
    
    def load_servers(self):
        """Загрузить серверы из конфигурации"""
        config_file = os.path.join(self.servers_dir, 'servers.json')
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                data = json.load(f)
                for server_data in data:
                    server = Server.from_dict(server_data)
                    self.servers[server.id] = server
    
    def save_servers(self):
        """Сохранить серверы в конфигурацию"""
        os.makedirs(self.servers_dir, exist_ok=True)
        config_file = os.path.join(self.servers_dir, 'servers.json')
        
        data = [server.to_dict() for server in self.servers.values()]
        with open(config_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def create_server(self, name: str, command: str, working_dir: str, 
                     port: int = None, auto_start: bool = False) -> 'Server':
        """Создать новый сервер"""
        server_id = self._generate_id(name)
        
        server = Server(
            id=server_id,
            name=name,
            command=command,
            working_dir=working_dir,
            port=port,
            auto_start=auto_start
        )
        
        self.servers[server_id] = server
        self.save_servers()
        
        return server
    
    def get_server(self, server_id: str) -> Optional['Server']:
        """Получить сервер по ID"""
        return self.servers.get(server_id)
    
    def list_servers(self) -> List[Dict[str, Any]]:
        """Получить список всех серверов"""
        return [server.to_dict() for server in self.servers.values()]
    
    def delete_server(self, server_id: str) -> bool:
        """Удалить сервер"""
        server = self.get_server(server_id)
        if not server:
            return False
        
        if server.is_running():
            server.stop()
        
        del self.servers[server_id]
        self.save_servers()
        return True
    
    def start_server(self, server_id: str) -> bool:
        """Запустить сервер"""
        server = self.get_server(server_id)
        if server:
            return server.start()
        return False
    
    def stop_server(self, server_id: str) -> bool:
        """Остановить сервер"""
        server = self.get_server(server_id)
        if server:
            return server.stop()
        return False
    
    def restart_server(self, server_id: str) -> bool:
        """Перезапустить сервер"""
        server = self.get_server(server_id)
        if server:
            return server.restart()
        return False
    
    def send_command(self, server_id: str, command: str) -> bool:
        """Отправить команду в консоль сервера"""
        server = self.get_server(server_id)
        if server:
            return server.send_command(command)
        return False
    
    def get_console_output(self, server_id: str, lines: int = 100) -> List[str]:
        """Получить последние строки консоли"""
        server = self.get_server(server_id)
        if server:
            return server.get_console_output(lines)
        return []
    
    def _generate_id(self, name: str) -> str:
        """Генерация уникального ID"""
        import hashlib
        import time
        
        base = f"{name}_{time.time()}"
        return hashlib.md5(base.encode()).hexdigest()[:16]


class Server:
    """Класс представляющий один сервер"""
    
    def __init__(self, id: str, name: str, command: str, working_dir: str,
                 port: int = None, auto_start: bool = False):
        self.id = id
        self.name = name
        self.command = command
        self.working_dir = working_dir
        self.port = port
        self.auto_start = auto_start
        
        self.process: Optional[subprocess.Popen] = None
        self.pid: Optional[int] = None
        self.console_buffer: queue.Queue = queue.Queue(maxsize=1000)
        self.console_thread: Optional[threading.Thread] = None
        
        self.created_at = datetime.now()
        self.started_at: Optional[datetime] = None
    
    def start(self) -> bool:
        """Запустить сервер"""
        if self.is_running():
            return False
        
        try:
            # Создание рабочей директории
            os.makedirs(self.working_dir, exist_ok=True)
            
            # Запуск процесса
            self.process = subprocess.Popen(
                self.command,
                shell=True,
                cwd=self.working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                bufsize=1,
                universal_newlines=True
            )
            
            self.pid = self.process.pid
            self.started_at = datetime.now()
            
            # Запуск потока для чтения консоли
            self.console_thread = threading.Thread(target=self._read_console, daemon=True)
            self.console_thread.start()
            
            return True
            
        except Exception as e:
            print(f"Error starting server {self.name}: {e}")
            return False
    
    def stop(self, timeout: int = 10) -> bool:
        """Остановить сервер"""
        if not self.is_running():
            return False
        
        try:
            # Попытка graceful shutdown
            self.process.terminate()
            
            try:
                self.process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                # Принудительная остановка
                self.process.kill()
                self.process.wait()
            
            self.process = None
            self.pid = None
            self.started_at = None
            
            return True
            
        except Exception as e:
            print(f"Error stopping server {self.name}: {e}")
            return False
    
    def restart(self) -> bool:
        """Перезапустить сервер"""
        if self.is_running():
            if not self.stop():
                return False
        
        return self.start()
    
    def is_running(self) -> bool:
        """Проверить запущен ли сервер"""
        if self.process is None:
            return False
        
        return self.process.poll() is None
    
    def send_command(self, command: str) -> bool:
        """Отправить команду в stdin процесса"""
        if not self.is_running() or not self.process.stdin:
            return False
        
        try:
            self.process.stdin.write(f"{command}\n")
            self.process.stdin.flush()
            return True
        except Exception as e:
            print(f"Error sending command to {self.name}: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Получить статистику сервера"""
        if not self.is_running():
            return {
                'status': 'stopped',
                'cpu': 0,
                'memory': 0,
                'uptime': 0
            }
        
        try:
            proc = psutil.Process(self.pid)
            cpu_percent = proc.cpu_percent(interval=0.1)
            memory_info = proc.memory_info()
            uptime = (datetime.now() - self.started_at).total_seconds()
            
            return {
                'status': 'running',
                'cpu': cpu_percent,
                'memory': memory_info.rss,
                'memory_percent': proc.memory_percent(),
                'uptime': uptime,
                'threads': proc.num_threads()
            }
            
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return {
                'status': 'error',
                'cpu': 0,
                'memory': 0,
                'uptime': 0
            }
    
    def get_console_output(self, lines: int = 100) -> List[str]:
        """Получить последние строки консоли"""
        output = []
        temp_queue = queue.Queue()
        
        # Извлекаем все элементы
        while not self.console_buffer.empty():
            try:
                line = self.console_buffer.get_nowait()
                temp_queue.put(line)
                output.append(line)
            except queue.Empty:
                break
        
        # Возвращаем элементы обратно
        while not temp_queue.empty():
            self.console_buffer.put(temp_queue.get_nowait())
        
        return output[-lines:]
    
    def _read_console(self):
        """Поток для чтения вывода консоли"""
        if not self.process or not self.process.stdout:
            return
        
        for line in iter(self.process.stdout.readline, ''):
            if not line:
                break
            
            line = line.strip()
            
            # Добавляем в буфер
            try:
                self.console_buffer.put_nowait(line)
            except queue.Full:
                # Удаляем старую строку если буфер полон
                try:
                    self.console_buffer.get_nowait()
                    self.console_buffer.put_nowait(line)
                except queue.Empty:
                    pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь"""
        return {
            'id': self.id,
            'name': self.name,
            'command': self.command,
            'working_dir': self.working_dir,
            'port': self.port,
            'auto_start': self.auto_start,
            'is_running': self.is_running(),
            'stats': self.get_stats(),
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Server':
        """Создать из словаря"""
        return cls(
            id=data['id'],
            name=data['name'],
            command=data['command'],
            working_dir=data['working_dir'],
            port=data.get('port'),
            auto_start=data.get('auto_start', False)
        )
