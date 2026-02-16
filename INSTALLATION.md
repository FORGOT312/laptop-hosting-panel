# 🎯 Установка на ваш ноутбук - Пошаговая инструкция

## Шаг 1: Подготовка WSL

### 1.1 Проверьте WSL

Откройте PowerShell от имени администратора и выполните:

```powershell
wsl --version
```

Если WSL не установлен:

```powershell
wsl --install
```

Перезагрузите компьютер после установки.

### 1.2 Установите Ubuntu

```powershell
wsl --install -d Ubuntu-22.04
```

При первом запуске создайте пользователя и пароль.

## Шаг 2: Копирование проекта

### Вариант А: Из текущей директории Claude

Если вы сейчас в WSL:

```bash
# Скопируйте проект в вашу домашнюю директорию
cp -r /home/claude/laptop-hosting-panel ~/laptop-hosting-panel
cd ~/laptop-hosting-panel
```

### Вариант Б: Скачать ZIP архив

1. Скачайте весь проект как ZIP
2. Распакуйте в любую папку Windows, например:
   `C:\Users\ВашеИмя\laptop-hosting-panel`

3. Откройте WSL и перейдите в директорию:

```bash
cd /mnt/c/Users/ВашеИмя/laptop-hosting-panel
```

### Вариант В: Клонировать из GitHub (если загружен)

```bash
cd ~
git clone https://github.com/yourusername/laptop-hosting-panel.git
cd laptop-hosting-panel
```

## Шаг 3: Запуск установки

### Автоматическая установка (РЕКОМЕНДУЕТСЯ)

```bash
chmod +x install.sh
./install.sh
```

Установщик:
- ✅ Обновит систему
- ✅ Установит Python и зависимости
- ✅ Создаст виртуальное окружение
- ✅ Настроит базу данных
- ✅ Создаст конфигурационные файлы

### Ручная установка

Если автоматическая установка не сработала:

```bash
# 1. Обновите систему
sudo apt update && sudo apt upgrade -y

# 2. Установите зависимости
sudo apt install -y python3 python3-pip python3-venv git curl build-essential

# 3. Перейдите в backend
cd backend

# 4. Создайте виртуальное окружение
python3 -m venv venv

# 5. Активируйте окружение
source venv/bin/activate

# 6. Установите пакеты
pip install --upgrade pip
pip install -r requirements.txt

# 7. Создайте .env файл
cp .env.example .env

# 8. Создайте директории
mkdir -p data logs servers
```

## Шаг 4: Первый запуск

### Запустите Backend

```bash
cd backend
source venv/bin/activate
python app.py
```

Вы должны увидеть:
```
🚀 Starting Laptop Hosting Panel...
📡 Backend running on http://localhost:5000
🔌 WebSocket available on ws://localhost:5000
 * Running on http://0.0.0.0:5000
```

**НЕ ЗАКРЫВАЙТЕ это окно терминала!**

### Откройте Frontend

#### Способ 1: Прямое открытие файла

1. Откройте Windows Explorer
2. Перейдите к `\\wsl$\Ubuntu\home\ваш-пользователь\laptop-hosting-panel\frontend`
3. Дважды кликните на `index.html`

#### Способ 2: Python HTTP Server (рекомендуется)

Откройте **НОВЫЙ** WSL терминал:

```bash
cd ~/laptop-hosting-panel/frontend
python3 -m http.server 3000
```

Откройте браузер: `http://localhost:3000`

## Шаг 5: Первый вход

1. Откройте `http://localhost:3000` (или открытый файл)
2. Логин: `admin`
3. Пароль: `admin`
4. **⚠️ ВАЖНО: Измените пароль сразу после входа!**

## Шаг 6: Создайте тестовый сервер

### Простой тестовый сервер

1. Нажмите **"Создать сервер"**
2. Заполните форму:

```
Название: Test Server
Команда: bash -c 'echo "Server started at $(date)"; sleep 3600'
Рабочая директория: /home/ваш-пользователь/test-server
Порт: (оставьте пустым)
```

3. Нажмите **"Создать"**
4. Нажмите **"Старт"** на созданном сервере
5. Нажмите **"Консоль"** чтобы увидеть вывод

Поздравляю! 🎉 Ваша панель работает!

## Шаг 7: Создайте реальный сервер (например, Minecraft)

### Minecraft Server

1. Создайте директорию:
```bash
mkdir -p ~/minecraft-server
cd ~/minecraft-server
```

2. Скачайте server.jar:
```bash
wget https://piston-data.mojang.com/v1/objects/84194a2f286ef7c14ed7ce0090dba59902951553/server.jar
```

3. Примите EULA:
```bash
echo "eula=true" > eula.txt
```

4. В веб-панели создайте сервер:
```
Название: My Minecraft Server
Команда: java -Xmx2G -Xms1G -jar server.jar nogui
Рабочая директория: /home/ваш-пользователь/minecraft-server
Порт: 25565
```

5. Запустите сервер через панель
6. Подключитесь в Minecraft: `localhost:25565`

## Шаг 8: Настройка автозапуска (опционально)

### Автозапуск панели при входе в Windows

1. Создайте файл `start-panel.bat`:

```batch
@echo off
wsl -d Ubuntu bash -c "cd ~/laptop-hosting-panel/backend && source venv/bin/activate && python app.py"
```

2. Сохраните в:
```
C:\Users\ВашеИмя\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\start-panel.bat
```

3. Теперь панель будет запускаться автоматически!

### Автозапуск через systemd (альтернатива)

```bash
sudo nano /etc/systemd/system/laptop-hosting-panel.service
```

Вставьте:
```ini
[Unit]
Description=Laptop Hosting Panel
After=network.target

[Service]
Type=simple
User=ваш-пользователь
WorkingDirectory=/home/ваш-пользователь/laptop-hosting-panel/backend
Environment="PATH=/home/ваш-пользователь/laptop-hosting-panel/backend/venv/bin"
ExecStart=/home/ваш-пользователь/laptop-hosting-panel/backend/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Активируйте:
```bash
sudo systemctl daemon-reload
sudo systemctl enable laptop-hosting-panel
sudo systemctl start laptop-hosting-panel
```

## Шаг 9: Доступ из локальной сети (опционально)

### Узнайте IP адрес WSL

```bash
hostname -I | awk '{print $1}'
```

Например: `172.20.10.5`

### Откройте порт в Windows Firewall

PowerShell от администратора:
```powershell
New-NetFirewallRule -DisplayName "Laptop Hosting Panel" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 5000
```

### Настройте проброс портов

```powershell
netsh interface portproxy add v4tov4 listenport=5000 listenaddress=0.0.0.0 connectport=5000 connectaddress=172.20.10.5
```

Теперь панель доступна по IP вашего ноутбука в локальной сети!

## Решение проблем

### Backend не запускается

```bash
# Проверьте Python
python3 --version

# Проверьте зависимости
cd backend
source venv/bin/activate
pip list

# Проверьте порт
sudo lsof -i :5000
```

### "Module not found"

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### "Permission denied"

```bash
chmod +x install.sh
chmod 755 backend/app.py
```

### WebSocket не подключается

1. Убедитесь что backend запущен
2. Откройте консоль браузера (F12)
3. Проверьте URL в frontend/index.html (должен быть `http://localhost:5000`)

### Сервер не может подключиться к базе

```bash
cd backend
python3 -c "from models.database import init_db; init_db()"
```

## Полезные команды

### Остановить backend

Нажмите `Ctrl+C` в терминале где запущен backend

### Обновить зависимости

```bash
cd backend
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### Очистить базу данных

```bash
rm backend/data/panel.db
python backend/app.py  # Создаст новую БД
```

### Просмотр логов

```bash
tail -f backend/logs/app.log
```

## Следующие шаги

✅ Панель установлена и работает!
✅ Создали тестовый сервер
✅ Настроили автозапуск

Теперь вы можете:
- 📖 Изучить [EXAMPLES.md](EXAMPLES.md) для примеров разных серверов
- 📚 Прочитать полную документацию в [docs/README.md](docs/README.md)
- 🎮 Создать свой игровой сервер
- 🤖 Запустить Discord/Telegram бота
- 🌐 Развернуть веб-приложение

## Получение помощи

Если что-то не работает:

1. ✅ Проверьте раздел "Решение проблем" выше
2. ✅ Посмотрите логи: `tail -f backend/logs/app.log`
3. ✅ Проверьте документацию: [docs/README.md](docs/README.md)
4. ✅ Откройте issue на GitHub

---

**Поздравляем! Ваш ноутбук теперь полноценный хостинг-сервер! 🎉**

Удачного использования! 🚀
