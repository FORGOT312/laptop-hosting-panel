"""
Database models and initialization
"""

import sqlite3
import os
from typing import Optional

def init_db(db_path: str = './data/panel.db'):
    """Инициализация базы данных"""
    # Создание директории для БД
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Подключение к БД
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Таблица серверов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servers (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            command TEXT NOT NULL,
            working_dir TEXT NOT NULL,
            port INTEGER,
            auto_start BOOLEAN DEFAULT 0,
            user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Таблица логов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            server_id TEXT,
            level TEXT,
            message TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (server_id) REFERENCES servers(id)
        )
    ''')
    
    # Таблица статистики
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            server_id TEXT,
            cpu_usage REAL,
            memory_usage REAL,
            network_in INTEGER,
            network_out INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (server_id) REFERENCES servers(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print(f'✅ Database initialized at {db_path}')

def get_db_connection(db_path: str = './data/panel.db'):
    """Получить соединение с БД"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

class User:
    """Модель пользователя"""
    
    @staticmethod
    def create(username: str, password: str, email: Optional[str] = None, role: str = 'user'):
        """Создать пользователя"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)',
                (username, password, email, role)
            )
            conn.commit()
            user_id = cursor.lastrowid
            return user_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_by_username(username: str):
        """Получить пользователя по имени"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        conn.close()
        return dict(user) if user else None
    
    @staticmethod
    def update_last_login(username: str):
        """Обновить время последнего входа"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE username = ?',
            (username,)
        )
        conn.commit()
        conn.close()

class ServerLog:
    """Модель лога сервера"""
    
    @staticmethod
    def add(server_id: str, level: str, message: str):
        """Добавить запись в лог"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO logs (server_id, level, message) VALUES (?, ?, ?)',
            (server_id, level, message)
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_logs(server_id: str, limit: int = 100):
        """Получить логи сервера"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT * FROM logs WHERE server_id = ? ORDER BY timestamp DESC LIMIT ?',
            (server_id, limit)
        )
        logs = cursor.fetchall()
        
        conn.close()
        return [dict(log) for log in logs]

class ServerStats:
    """Модель статистики сервера"""
    
    @staticmethod
    def add(server_id: str, cpu_usage: float, memory_usage: float, 
            network_in: int, network_out: int):
        """Добавить статистику"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            '''INSERT INTO statistics 
            (server_id, cpu_usage, memory_usage, network_in, network_out) 
            VALUES (?, ?, ?, ?, ?)''',
            (server_id, cpu_usage, memory_usage, network_in, network_out)
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_stats(server_id: str, hours: int = 24):
        """Получить статистику за период"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            '''SELECT * FROM statistics 
            WHERE server_id = ? 
            AND timestamp > datetime('now', '-' || ? || ' hours')
            ORDER BY timestamp DESC''',
            (server_id, hours)
        )
        stats = cursor.fetchall()
        
        conn.close()
        return [dict(stat) for stat in stats]
