# 🖥️ Laptop Hosting Panel

<div align="center">

**Превратите свой ноутбук в мощный хостинг-сервер!**

Веб-панель для управления серверами, приложениями и сервисами через WSL на Windows.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Быстрый старт](#-быстрый-старт) • [Возможности](#-возможности) • [Документация](docs/README.md) • [API](#-api)

</div>

---

## 📸 Скриншот

```
┌─────────────────────────────────────────────────────────────┐
│  🖥️ Laptop Hosting Panel                   [+ Создать сервер]│
├─────────────────────────────────────────────────────────────┤
│  CPU: 45.2%    │  Memory: 6.2GB/16GB  │  Network: 1.2MB/s  │
├─────────────────────────────────────────────────────────────┤
│  📦 Minecraft Server               [Запущен] ⚡              │
│  CPU: 35% │ RAM: 2.1GB │ Uptime: 2h 15m │ Port: 25565      │
│  [Стоп] [Рестарт] [Консоль] [Удалить]                      │
├─────────────────────────────────────────────────────────────┤
│  📦 Discord Bot                    [Остановлен] ⭕          │
│  [Старт] [Консоль] [Удалить]                               │
└─────────────────────────────────────────────────────────────┘
```

## ✨ Возможности

### 🎮 Управление серверами
- ✅ Запуск/остановка/перезапуск одним кликом
- ✅ Поддержка **любых** приложений (Minecraft, Node.js, Python, Discord боты...)
- ✅ Автозапуск при старте системы
- ✅ Группировка и организация серверов

### 📊 Мониторинг в реальном времени
- ✅ CPU, RAM, диск, сеть для всей системы
- ✅ Индивидуальная статистика каждого сервера
- ✅ История использования ресурсов
- ✅ Графики и визуализация

### 🖥️ Интерактивная консоль
- ✅ Просмотр вывода сервера в реальном времени
- ✅ Отправка команд напрямую в stdin процесса
- ✅ Цветной вывод и прокрутка
- ✅ Поиск по логам

### 🔐 Безопасность
- ✅ JWT аутентификация
- ✅ Роли пользователей (admin, user)
- ✅ Изоляция серверов
- ✅ Логирование всех действий

### 🌐 Современный интерфейс
- ✅ Адаптивный дизайн (работает на телефоне!)
- ✅ Тёмная тема
- ✅ WebSocket для real-time обновлений
- ✅ Никаких перезагрузок страницы

## 🚀 Быстрый старт

### Предварительные требования

- Windows 10/11 с WSL2
- Ubuntu 22.04 в WSL
- Python 3.8+
- 2GB+ свободной RAM

### Автоматическая установка (рекомендуется)

```bash
# 1. Откройте WSL терминал
wsl

# 2. Склонируйте репозиторий
git clone https://github.com/yourusername/laptop-hosting-panel.git
cd laptop-hosting-panel

# 3. Запустите установщик
chmod +x install.sh
./install.sh

# 4. Готово! Панель запустится автоматически
```

### Ручная установка

```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py

# Frontend (в новом терминале)
cd frontend
python3 -m http.server 3000
```

### Первый запуск

1. Откройте `http://localhost:3000` в браузере
2. Войдите (логин: `admin`, пароль: `admin`)
3. Нажмите **"Создать сервер"**
4. Заполните форму и запустите!

Подробнее: [QUICKSTART.md](QUICKSTART.md)

## 📚 Примеры использования

### Minecraft Server

```bash
# 1. Создайте сервер через интерфейс:
Название: My Minecraft Server
Команда: java -Xmx2G -jar server.jar nogui
Директория: /home/user/minecraft
Порт: 25565

# 2. Нажмите "Старт"
# 3. Подключайтесь: localhost:25565
```

### Node.js приложение

```bash
Название: Web API
Команда: node index.js
Директория: /home/user/my-api
Порт: 3000
```

### Python скрипт

```bash
Название: Data Processor
Команда: python3 main.py
Директория: /home/user/scripts
Порт: (пусто)
```

### Discord Bot

```bash
Название: My Bot
Команда: python3 bot.py
Директория: /home/user/discord-bot
Порт: (пусто)
```

## 🔌 API

### Серверы

```bash
# Список серверов
GET /api/servers

# Создать сервер
POST /api/servers
{
  "name": "Server Name",
  "command": "start command",
  "working_dir": "/path/to/dir",
  "port": 8080
}

# Управление
POST /api/servers/{id}/start
POST /api/servers/{id}/stop
POST /api/servers/{id}/restart

# Консоль
POST /api/servers/{id}/command
GET /api/servers/{id}/console
```

### Система

```bash
# Статистика
GET /api/system/stats

# Процессы
GET /api/system/processes
```

Полная документация API: [docs/README.md](docs/README.md)

## 📁 Структура проекта

```
laptop-hosting-panel/
├── backend/                 # Python Backend
│   ├── api/                # API endpoints
│   │   ├── auth.py        # Аутентификация
│   │   └── servers.py     # Управление серверами
│   ├── core/              # Бизнес-логика
│   │   ├── server_manager.py    # Менеджер серверов
│   │   └── system_monitor.py    # Мониторинг системы
│   ├── models/            # Модели данных
│   │   └── database.py    # SQLite БД
│   ├── app.py            # Главный файл
│   └── requirements.txt   # Зависимости
├── frontend/              # HTML/JS Frontend
│   └── index.html        # Веб-интерфейс
├── docs/                 # Документация
│   └── README.md         # Полная документация
├── install.sh            # Установщик
├── QUICKSTART.md         # Быстрый старт
└── README.md             # Этот файл
```

## 🛠️ Конфигурация

### Переменные окружения (backend/.env)

```bash
SECRET_KEY=your-secret-key
DATABASE_PATH=./data/panel.db
HOST=0.0.0.0
PORT=5000
DEBUG=True
```

### Автозапуск при входе в Windows

Создайте `start-panel.bat`:

```batch
@echo off
wsl -d Ubuntu bash -c "cd /path/to/backend && source venv/bin/activate && python app.py"
```

Поместите в: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`

## 🔒 Безопасность

⚠️ **Важно для продакшена:**

1. Измените `SECRET_KEY` в `.env`
2. Смените пароль admin
3. Настройте firewall
4. Используйте HTTPS (nginx + SSL)
5. Ограничьте доступ к API

## 🐛 Решение проблем

### Backend не запускается

```bash
# Проверьте порт
sudo lsof -i :5000

# Проверьте логи
tail -f backend/logs/app.log
```

### WebSocket не подключается

- Убедитесь что backend запущен на порту 5000
- Откройте консоль браузера (F12)
- Проверьте CORS настройки

### Сервер не стартует

```bash
# Проверьте права на директорию
ls -la /path/to/server

# Проверьте команду запуска
curl http://localhost:5000/api/servers/{ID}
```

Больше решений: [docs/README.md#troubleshooting](docs/README.md)

## 🚀 Расширенные возможности

### Темы оформления
- [ ] Светлая тема
- [ ] Кастомизация цветов
- [ ] Компактный режим

### Мониторинг
- [x] Системная статистика
- [x] Статистика серверов
- [ ] Алерты и уведомления
- [ ] Email/Telegram уведомления

### Управление
- [x] Базовые операции
- [ ] Планировщик задач (cron)
- [ ] Резервное копирование
- [ ] Snapshot/Restore

### Интеграции
- [ ] Docker контейнеры
- [ ] GitHub webhooks
- [ ] CI/CD пайплайны

## 🤝 Участие в разработке

Мы приветствуем ваш вклад!

1. Fork проекта
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📝 Roadmap

- [x] v1.0 - Базовая функциональность
- [x] Управление серверами
- [x] Мониторинг ресурсов
- [x] Интерактивная консоль
- [ ] v1.1 - Улучшения UI
  - [ ] Графики использования
  - [ ] Темы оформления
  - [ ] Мобильное приложение
- [ ] v1.2 - Автоматизация
  - [ ] Планировщик задач
  - [ ] Автобэкапы
  - [ ] Email уведомления
- [ ] v2.0 - Enterprise функции
  - [ ] Multi-user support
  - [ ] Docker интеграция
  - [ ] API ключи

## 📄 Лицензия

MIT License - свободное использование и модификация

## 🙏 Благодарности

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Socket.IO](https://socket.io/) - Real-time engine
- [psutil](https://github.com/giampaolo/psutil) - System monitoring
- Все участники проекта!

## 💬 Поддержка

- 📧 Email: support@example.com
- 💬 Discord: [Присоединяйтесь](https://discord.gg/...)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/laptop-hosting-panel/issues)

---

<div align="center">

**⭐ Если проект вам понравился, поставьте звезду на GitHub! ⭐**

Сделано с ❤️ для управления серверами на домашнем ноутбуке

[⬆ Вернуться наверх](#-laptop-hosting-panel)

</div>

# laptop-hosting-panel
hosting panel 

