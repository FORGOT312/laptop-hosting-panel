"""
System Monitor - мониторинг ресурсов системы
"""

import psutil
import platform
from datetime import datetime, timedelta
from typing import Dict, List, Any

class SystemMonitor:
    """Класс для мониторинга системных ресурсов"""
    
    def __init__(self):
        self.boot_time = datetime.fromtimestamp(psutil.boot_time())
    
    def get_uptime(self) -> str:
        """Получить время работы системы"""
        uptime = datetime.now() - self.boot_time
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m {seconds}s"
    
    def get_cpu_info(self) -> Dict[str, Any]:
        """Получить информацию о CPU"""
        cpu_percent = psutil.cpu_percent(interval=1, percpu=False)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        return {
            'usage': cpu_percent,
            'cores': cpu_count,
            'frequency': {
                'current': cpu_freq.current if cpu_freq else 0,
                'min': cpu_freq.min if cpu_freq else 0,
                'max': cpu_freq.max if cpu_freq else 0
            }
        }
    
    def get_memory_info(self) -> Dict[str, Any]:
        """Получить информацию о памяти"""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            'total': mem.total,
            'used': mem.used,
            'free': mem.free,
            'available': mem.available,
            'percent': mem.percent,
            'swap': {
                'total': swap.total,
                'used': swap.used,
                'free': swap.free,
                'percent': swap.percent
            }
        }
    
    def get_disk_info(self) -> List[Dict[str, Any]]:
        """Получить информацию о дисках"""
        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                })
            except PermissionError:
                continue
        return disks
    
    def get_network_info(self) -> Dict[str, Any]:
        """Получить информацию о сети"""
        net_io = psutil.net_io_counters()
        
        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv,
            'errin': net_io.errin,
            'errout': net_io.errout,
            'dropin': net_io.dropin,
            'dropout': net_io.dropout
        }
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Получить полную статистику системы"""
        return {
            'timestamp': datetime.now().isoformat(),
            'uptime': self.get_uptime(),
            'platform': {
                'system': platform.system(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor()
            },
            'cpu': self.get_cpu_info(),
            'memory': self.get_memory_info(),
            'disks': self.get_disk_info(),
            'network': self.get_network_info()
        }
    
    def get_processes(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Получить список процессов"""
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']):
            try:
                pinfo = proc.info
                processes.append({
                    'pid': pinfo['pid'],
                    'name': pinfo['name'],
                    'username': pinfo['username'],
                    'cpu_percent': pinfo['cpu_percent'],
                    'memory_percent': pinfo['memory_percent'],
                    'status': pinfo['status']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Сортировка по использованию CPU
        processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
        
        return processes[:limit]
    
    def format_bytes(self, bytes: int) -> str:
        """Форматирование байтов в читаемый формат"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} PB"
