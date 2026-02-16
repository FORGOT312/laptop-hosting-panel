# 🚀 Быстрый старт

## Шаг 1: Установка

В WSL выполните:

```bash
cd /path/to/laptop-hosting-panel
chmod +x install.sh
./install.sh
```

Или вручную:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Шаг 2: Запуск Backend

```bash
cd backend
source venv/bin/activate
python app.py
```

Backend запустится на `http://localhost:5000`

## Шаг 3: Открыть Frontend

Просто откройте файл в браузере:

```bash
# В Windows откройте:
\\wsl$\Ubuntu\path\to\laptop-hosting-panel\frontend\index.html

# Или используйте Python сервер:
cd frontend
python3 -m http.server 3000
# Откройте http://localhost:3000
```

## Шаг 4: Создайте первый сервер

1. Нажмите "Создать сервер"
2. Заполните форму:
   - **Название**: My Test Server
   - **Команда**: `echo "Server started" && sleep 3600`
   - **Рабочая директория**: `/home/yourusername/test-server`
   - **Порт**: (оставьте пустым)
3. Нажмите "Создать"
4. Нажмите "Старт"

## Примеры серверов

### Minecraft Server

```json
{
  "name": "Minecraft Server",
  "command": "java -Xmx2G -Xms1G -jar server.jar nogui",
  "working_dir": "/home/user/minecraft",
  "port": 25565
}
```

Перед запуском:
```bash
mkdir -p /home/user/minecraft
cd /home/user/minecraft
# Скачайте server.jar с minecraft.net
wget https://...server.jar
echo "eula=true" > eula.txt
```

### Node.js App

```json
{
  "name": "Web Server",
  "command": "node server.js",
  "working_dir": "/home/user/my-app",
  "port": 3000
}
```

### Python Script

```json
{
  "name": "Data Processor",
  "command": "python3 main.py",
  "working_dir": "/home/user/scripts",
  "port": null
}
```

## API Примеры

### Получить список серверов
```bash
curl http://localhost:5000/api/servers
```

### Запустить сервер
```bash
curl -X POST http://localhost:5000/api/servers/{SERVER_ID}/start
```

### Отправить команду
```bash
curl -X POST http://localhost:5000/api/servers/{SERVER_ID}/command \
  -H "Content-Type: application/json" \
  -d '{"command": "say Hello"}'
```

### Системная статистика
```bash
curl http://localhost:5000/api/system/stats | jq
```

## Доступ из Windows к серверам WSL

Если сервер слушает на порту 25565 в WSL, он доступен из Windows по адресу:
- `localhost:25565`
- `127.0.0.1:25565`

## Автозапуск при входе в Windows

Создайте файл `start-panel.bat` в папке автозагрузки:

```batch
@echo off
wsl -d Ubuntu bash -c "cd /path/to/backend && source venv/bin/activate && python app.py"
```

Поместите его в:
```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
```

## Решение проблем

### Backend не запускается
```bash
# Проверьте логи
tail -f backend/logs/app.log

# Проверьте порт
sudo lsof -i :5000
```

### Сервер не может запуститься
```bash
# Проверьте права
ls -la /path/to/server

# Проверьте логи
curl http://localhost:5000/api/servers/{ID}/console
```

### WebSocket не подключается
- Убедитесь что backend запущен
- Проверьте CORS настройки
- Откройте консоль браузера (F12)

## Следующие шаги

1. ✅ Измените пароль admin
2. ✅ Настройте автозапуск нужных серверов
3. ✅ Установите Nginx для HTTPS (опционально)
4. ✅ Настройте резервное копирование

Полная документация: `docs/README.md`
