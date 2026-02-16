# 🎮 Примеры конфигураций серверов

## Minecraft Servers

### Vanilla Server
```json
{
  "name": "Minecraft Vanilla 1.20",
  "command": "java -Xmx4G -Xms2G -jar server.jar nogui",
  "working_dir": "/home/user/minecraft/vanilla",
  "port": 25565,
  "auto_start": true
}
```

Подготовка:
```bash
mkdir -p /home/user/minecraft/vanilla
cd /home/user/minecraft/vanilla
wget https://piston-data.mojang.com/v1/objects/.../server.jar
echo "eula=true" > eula.txt
```

### Spigot/Paper Server
```json
{
  "name": "Paper Server",
  "command": "java -Xmx6G -Xms4G -XX:+UseG1GC -jar paper.jar --nogui",
  "working_dir": "/home/user/minecraft/paper",
  "port": 25565
}
```

### Forge Modded Server
```json
{
  "name": "Modded Minecraft",
  "command": "./run.sh",
  "working_dir": "/home/user/minecraft/modded",
  "port": 25565
}
```

### Bungeecord Proxy
```json
{
  "name": "Bungeecord Proxy",
  "command": "java -Xmx512M -jar BungeeCord.jar",
  "working_dir": "/home/user/minecraft/proxy",
  "port": 25577
}
```

## Web Applications

### Node.js Express API
```json
{
  "name": "Express API",
  "command": "node index.js",
  "working_dir": "/home/user/apps/express-api",
  "port": 3000
}
```

### Next.js Application
```json
{
  "name": "Next.js App",
  "command": "npm start",
  "working_dir": "/home/user/apps/nextjs-app",
  "port": 3000
}
```

### React Development Server
```json
{
  "name": "React Dev",
  "command": "npm run dev",
  "working_dir": "/home/user/apps/react-app",
  "port": 5173
}
```

### Flask Python API
```json
{
  "name": "Flask API",
  "command": "source venv/bin/activate && flask run --host=0.0.0.0 --port=5001",
  "working_dir": "/home/user/apps/flask-api",
  "port": 5001
}
```

### Django Application
```json
{
  "name": "Django App",
  "command": "source venv/bin/activate && python manage.py runserver 0.0.0.0:8000",
  "working_dir": "/home/user/apps/django-app",
  "port": 8000
}
```

## Bots

### Discord Bot (Python)
```json
{
  "name": "Discord Bot",
  "command": "source venv/bin/activate && python bot.py",
  "working_dir": "/home/user/bots/discord-bot",
  "port": null
}
```

### Discord Bot (JavaScript)
```json
{
  "name": "Discord Bot JS",
  "command": "node index.js",
  "working_dir": "/home/user/bots/discord-bot-js",
  "port": null
}
```

### Telegram Bot
```json
{
  "name": "Telegram Bot",
  "command": "source venv/bin/activate && python telegram_bot.py",
  "working_dir": "/home/user/bots/telegram-bot",
  "port": null
}
```

## Databases

### MongoDB
```json
{
  "name": "MongoDB",
  "command": "mongod --dbpath ./data --port 27017",
  "working_dir": "/home/user/databases/mongodb",
  "port": 27017
}
```

### Redis
```json
{
  "name": "Redis Server",
  "command": "redis-server",
  "working_dir": "/home/user/databases/redis",
  "port": 6379
}
```

### PostgreSQL (если не используете системный)
```json
{
  "name": "PostgreSQL",
  "command": "postgres -D ./data",
  "working_dir": "/home/user/databases/postgres",
  "port": 5432
}
```

## Game Servers

### Terraria Server
```json
{
  "name": "Terraria Server",
  "command": "./TerrariaServer.bin.x86_64 -config serverconfig.txt",
  "working_dir": "/home/user/games/terraria",
  "port": 7777
}
```

### CS:GO Server
```json
{
  "name": "CS:GO Server",
  "command": "./srcds_run -game csgo -console -usercon +game_type 0 +game_mode 1 +mapgroup mg_active +map de_dust2",
  "working_dir": "/home/user/games/csgo",
  "port": 27015
}
```

### Factorio Server
```json
{
  "name": "Factorio Server",
  "command": "./bin/x64/factorio --start-server my-save.zip",
  "working_dir": "/home/user/games/factorio",
  "port": 34197
}
```

### Valheim Server
```json
{
  "name": "Valheim Server",
  "command": "./valheim_server.x86_64 -name 'My Server' -port 2456 -world 'Dedicated' -password 'secret'",
  "working_dir": "/home/user/games/valheim",
  "port": 2456
}
```

## Development Tools

### Webpack Dev Server
```json
{
  "name": "Webpack Dev",
  "command": "npm run dev",
  "working_dir": "/home/user/dev/webpack-project",
  "port": 8080
}
```

### Python HTTP Server
```json
{
  "name": "Simple HTTP Server",
  "command": "python3 -m http.server 8000",
  "working_dir": "/home/user/www",
  "port": 8000
}
```

### Live Server (npm)
```json
{
  "name": "Live Server",
  "command": "npx live-server --port=8080",
  "working_dir": "/home/user/html",
  "port": 8080
}
```

## Background Services

### File Watcher
```json
{
  "name": "File Watcher",
  "command": "python3 file_watcher.py",
  "working_dir": "/home/user/scripts",
  "port": null
}
```

### Backup Script
```json
{
  "name": "Auto Backup",
  "command": "bash backup.sh",
  "working_dir": "/home/user/backups",
  "port": null
}
```

### Cron Alternative
```json
{
  "name": "Scheduler",
  "command": "python3 scheduler.py",
  "working_dir": "/home/user/scheduler",
  "port": null
}
```

## Media Servers

### Plex Media Server (если установлен локально)
```json
{
  "name": "Plex",
  "command": "/usr/lib/plexmediaserver/Plex\\ Media\\ Server",
  "working_dir": "/var/lib/plexmediaserver",
  "port": 32400
}
```

### Jellyfin
```json
{
  "name": "Jellyfin",
  "command": "./jellyfin",
  "working_dir": "/home/user/jellyfin",
  "port": 8096
}
```

## Monitoring & Logging

### Prometheus
```json
{
  "name": "Prometheus",
  "command": "./prometheus --config.file=prometheus.yml",
  "working_dir": "/home/user/monitoring/prometheus",
  "port": 9090
}
```

### Grafana
```json
{
  "name": "Grafana",
  "command": "./bin/grafana-server",
  "working_dir": "/home/user/monitoring/grafana",
  "port": 3000
}
```

## VPN & Networking

### OpenVPN Server
```json
{
  "name": "OpenVPN",
  "command": "sudo openvpn --config server.conf",
  "working_dir": "/etc/openvpn",
  "port": 1194
}
```

### Nginx (Custom)
```json
{
  "name": "Nginx",
  "command": "nginx -c ./nginx.conf -g 'daemon off;'",
  "working_dir": "/home/user/nginx",
  "port": 8080
}
```

## Testing & CI/CD

### Selenium Grid
```json
{
  "name": "Selenium Hub",
  "command": "java -jar selenium-server.jar hub",
  "working_dir": "/home/user/selenium",
  "port": 4444
}
```

### Local Jenkins
```json
{
  "name": "Jenkins",
  "command": "java -jar jenkins.war --httpPort=8080",
  "working_dir": "/home/user/jenkins",
  "port": 8080
}
```

## Useful Scripts

### Keep-Alive Script
Создайте `keepalive.sh`:
```bash
#!/bin/bash
while true; do
    echo "[$(date)] Server is alive"
    sleep 60
done
```

Используйте:
```json
{
  "name": "Keep Alive",
  "command": "bash keepalive.sh",
  "working_dir": "/home/user/scripts",
  "port": null
}
```

### Auto-Restart on Crash
Создайте `run.sh`:
```bash
#!/bin/bash
while true; do
    echo "Starting server..."
    java -jar server.jar
    echo "Server crashed! Restarting in 5 seconds..."
    sleep 5
done
```

### Port Forwarding Script
```bash
#!/bin/bash
# Forward port from WSL to Windows
netsh.exe interface portproxy add v4tov4 listenport=25565 listenaddress=0.0.0.0 connectport=25565 connectaddress=$(hostname -I | awk '{print $1}')
```

## Советы

### Использование переменных окружения
Создайте `.env` файл в директории сервера:
```bash
PORT=3000
NODE_ENV=production
DATABASE_URL=mongodb://localhost:27017/mydb
```

Команда:
```bash
source .env && node server.js
```

### Логирование
Перенаправьте вывод в файл:
```bash
java -jar server.jar 2>&1 | tee server.log
```

### Проверка перед запуском
```bash
#!/bin/bash
if [ ! -f "config.yml" ]; then
    echo "Config not found!"
    exit 1
fi
java -jar server.jar
```

### Мультиплексирование (screen/tmux)
```bash
screen -dmS myserver java -jar server.jar
# или
tmux new-session -d -s myserver 'java -jar server.jar'
```

Но с нашей панелью это не нужно! 😎
