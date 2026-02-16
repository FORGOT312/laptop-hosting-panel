# 🖥️ Laptop Hosting Panel

Веб-панель для управления серверами и приложениями на вашем ноутбуке через WSL.

## ✨ Возможности

- 🎮 **Управление серверами**: Запуск, остановка, перезапуск любых приложений
- 📊 **Мониторинг в реальном времени**: CPU, RAM, диск, сеть
- 🖥️ **Интерактивная консоль**: Отправка команд и просмотр вывода
- 📈 **Графики статистики**: Визуализация использования ресурсов
- 🔐 **Аутентификация**: Защита доступа к панели
- 🌐 **WebSocket**: Обновления в реальном времени
- 📱 **Адаптивный дизайн**: Работает на всех устройствах

## 🚀 Быстрый старт

### Требования

- Windows 10/11 с WSL2
- Ubuntu 22.04 в WSL
- Python 3.8+
- Node.js 16+ (для фронтенда)

### Установка Backend

1. **Откройте WSL терминал**:
```bash
# В Windows нажмите Win+R и введите: wsl
```

2. **Перейдите в директорию проекта**:
```bash
cd /mnt/c/Users/YOUR_USERNAME/laptop-hosting-panel
# или клонируйте репозиторий:
# git clone https://github.com/yourusername/laptop-hosting-panel.git
# cd laptop-hosting-panel
```

3. **Установите зависимости**:
```bash
cd backend

# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установите пакеты
pip install -r requirements.txt
```

4. **Настройте переменные окружения**:
```bash
cp .env.example .env
nano .env  # Отредактируйте настройки
```

5. **Запустите сервер**:
```bash
python app.py
```

Backend будет доступен на `http://localhost:5000`

### Установка Frontend (будет создан далее)

```bash
cd frontend
npm install
npm run dev
```

Frontend будет доступен на `http://localhost:3000`

## 📖 Использование

### Создание сервера

**Через API**:
```bash
curl -X POST http://localhost:5000/api/servers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Minecraft Server",
    "command": "java -Xmx2G -jar server.jar nogui",
    "working_dir": "./servers/minecraft",
    "port": 25565,
    "auto_start": false
  }'
```

**Через веб-интерфейс**:
1. Откройте `http://localhost:3000`
2. Войдите (логин: `admin`, пароль: `admin`)
3. Нажмите "Создать сервер"
4. Заполните форму и сохраните

### Управление сервером

#### Запуск
```bash
curl -X POST http://localhost:5000/api/servers/{SERVER_ID}/start
```

#### Остановка
```bash
curl -X POST http://localhost:5000/api/servers/{SERVER_ID}/stop
```

#### Перезапуск
```bash
curl -X POST http://localhost:5000/api/servers/{SERVER_ID}/restart
```

#### Отправка команды
```bash
curl -X POST http://localhost:5000/api/servers/{SERVER_ID}/command \
  -H "Content-Type: application/json" \
  -d '{"command": "say Hello World"}'
```

### Просмотр статистики

#### Системная статистика
```bash
curl http://localhost:5000/api/system/stats
```

#### Статистика сервера
```bash
curl http://localhost:5000/api/servers/{SERVER_ID}/stats
```

#### Вывод консоли
```bash
curl http://localhost:5000/api/servers/{SERVER_ID}/console?lines=100
```

## 🔌 API Reference

### Authentication

#### POST /api/auth/login
Вход в систему
```json
{
  "username": "admin",
  "password": "admin"
}
```

#### POST /api/auth/register
Регистрация нового пользователя

### Servers

#### GET /api/servers
Список всех серверов

#### POST /api/servers
Создать новый сервер

#### GET /api/servers/{id}
Информация о сервере

#### DELETE /api/servers/{id}
Удалить сервер

#### POST /api/servers/{id}/start
Запустить сервер

#### POST /api/servers/{id}/stop
Остановить сервер

#### POST /api/servers/{id}/restart
Перезапустить сервер

#### POST /api/servers/{id}/command
Отправить команду

#### GET /api/servers/{id}/console
Получить вывод консоли

#### GET /api/servers/{id}/stats
Статистика сервера

### System

#### GET /api/system/stats
Системная статистика

#### GET /api/system/processes
Список процессов

## 🎨 Примеры серверов

### Minecraft Server
```json
{
  "name": "Minecraft Survival",
  "command": "java -Xmx4G -Xms2G -jar server.jar nogui",
  "working_dir": "/home/user/servers/minecraft-survival",
  "port": 25565
}
```

### Node.js приложение
```json
{
  "name": "Web API",
  "command": "node index.js",
  "working_dir": "/home/user/apps/web-api",
  "port": 3000
}
```

### Python скрипт
```json
{
  "name": "Data Processor",
  "command": "python3 processor.py",
  "working_dir": "/home/user/scripts/processor",
  "port": null
}
```

### Discord бот
```json
{
  "name": "Discord Bot",
  "command": "python3 bot.py",
  "working_dir": "/home/user/bots/discord-bot",
  "port": null
}
```

## 🔧 Настройка автозапуска

### Создание systemd service

1. Создайте файл сервиса:
```bash
sudo nano /etc/systemd/system/hosting-panel.service
```

2. Добавьте конфигурацию:
```ini
[Unit]
Description=Laptop Hosting Panel
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/laptop-hosting-panel/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Активируйте сервис:
```bash
sudo systemctl daemon-reload
sudo systemctl enable hosting-panel
sudo systemctl start hosting-panel
```

## 🐛 Отладка

### Просмотр логов
```bash
# Backend логи
tail -f backend/logs/app.log

# Systemd логи
sudo journalctl -u hosting-panel -f
```

### Проверка портов
```bash
# Проверить, какой процесс слушает порт
sudo lsof -i :5000
```

### Тестирование API
```bash
# Проверка здоровья
curl http://localhost:5000/api/health

# Системная информация
curl http://localhost:5000/api/system/stats | jq
```

## 🔐 Безопасность

⚠️ **ВАЖНО**: Перед использованием в продакшене:

1. **Измените SECRET_KEY** в `.env`
2. **Измените пароль admin** через API
3. **Настройте firewall** для ограничения доступа
4. **Используйте HTTPS** (nginx + Let's Encrypt)
5. **Регулярно обновляйте** зависимости

### Настройка Nginx

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## 📚 Дополнительные ресурсы

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Socket.IO Documentation](https://socket.io/docs/)
- [PSUtil Documentation](https://psutil.readthedocs.io/)

## 🤝 Вклад

Приветствуются pull requests! Для крупных изменений сначала откройте issue.

## 📄 Лицензия

MIT License - свободное использование и модификация

## 💬 Поддержка

Если у вас возникли проблемы или вопросы:
1. Проверьте раздел "Отладка" в документации
2. Откройте issue на GitHub
3. Опишите проблему подробно с логами

---

**Сделано с ❤️ для управления серверами на домашнем ноутбуке**
