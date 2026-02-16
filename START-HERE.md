# 📦 Laptop Hosting Panel - Полный пакет

## ✅ Что создано

Полнофункциональная веб-панель для управления серверами на вашем ноутбуке через WSL!

### 🎯 Основные компоненты

#### Backend (Python + Flask)
- ✅ `app.py` - главный сервер с WebSocket
- ✅ `server_manager.py` - управление процессами серверов
- ✅ `system_monitor.py` - мониторинг ресурсов (CPU, RAM, диск, сеть)
- ✅ `database.py` - SQLite база данных
- ✅ API endpoints для всех операций
- ✅ Real-time обновления через Socket.IO

#### Frontend (HTML + JavaScript)
- ✅ Адаптивный интерфейс с тёмной темой
- ✅ Мониторинг системы в реальном времени
- ✅ Управление серверами (старт/стоп/рестарт)
- ✅ Интерактивная консоль
- ✅ WebSocket интеграция

#### Документация
- ✅ `README.md` - полное описание проекта
- ✅ `INSTALLATION.md` - пошаговая установка
- ✅ `QUICKSTART.md` - быстрый старт
- ✅ `EXAMPLES.md` - примеры 50+ конфигураций
- ✅ `docs/README.md` - техническая документация

#### Утилиты
- ✅ `install.sh` - автоматический установщик
- ✅ `.env.example` - шаблон конфигурации
- ✅ `requirements.txt` - Python зависимости

## 🚀 Быстрый старт (3 минуты)

### Вариант 1: Автоматическая установка

```bash
# В WSL выполните:
cd /mnt/c/Users/ВашеИмя
# Скопируйте папку laptop-hosting-panel сюда
cd laptop-hosting-panel
./install.sh
```

### Вариант 2: Ручная установка

```bash
cd laptop-hosting-panel/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Откройте `frontend/index.html` в браузере!

## 📁 Структура файлов

```
laptop-hosting-panel/
│
├── 📄 README.md              ← Начните отсюда
├── 📄 INSTALLATION.md        ← Пошаговая установка на ваш ноутбук
├── 📄 QUICKSTART.md          ← Быстрый старт (5 минут)
├── 📄 EXAMPLES.md            ← 50+ примеров конфигураций
├── 🔧 install.sh             ← Автоматический установщик
│
├── backend/                  ← Python Backend
│   ├── app.py               ← 🚀 ЗАПУСТИТЕ ЭТОТ ФАЙЛ!
│   ├── requirements.txt     ← Зависимости
│   ├── .env.example         ← Пример конфигурации
│   │
│   ├── api/                 ← API endpoints
│   │   ├── auth.py         ← Аутентификация
│   │   └── servers.py      ← Управление серверами
│   │
│   ├── core/                ← Бизнес-логика
│   │   ├── server_manager.py  ← Менеджер процессов
│   │   └── system_monitor.py  ← Мониторинг системы
│   │
│   └── models/              ← База данных
│       └── database.py      ← SQLite модели
│
├── frontend/                 ← Веб-интерфейс
│   └── index.html           ← 🌐 ОТКРОЙТЕ В БРАУЗЕРЕ!
│
└── docs/                     ← Полная документация
    └── README.md            ← Техническая документация
```

## 🎮 Что можно делать

### ✅ Любые серверы и приложения
- 🎮 Minecraft (Vanilla, Spigot, Paper, Forge, Bungeecord)
- 🤖 Discord/Telegram боты
- 🌐 Node.js, Python, Ruby приложения
- 🗄️ MongoDB, Redis, PostgreSQL
- 🎯 CS:GO, Terraria, Factorio, Valheim
- 🔧 И любые другие процессы!

### ✅ Полное управление
- ▶️ Запуск/остановка/перезапуск
- 📊 Мониторинг ресурсов (CPU, RAM, сеть)
- 🖥️ Интерактивная консоль
- 📈 Графики использования
- 🔄 Автозапуск при старте

### ✅ Удобный интерфейс
- 🌙 Тёмная тема
- 📱 Адаптивный дизайн
- ⚡ Real-time обновления
- 🚀 Без перезагрузок страницы

## 💡 Примеры использования

### Minecraft Server
```json
{
  "name": "My Minecraft",
  "command": "java -Xmx2G -jar server.jar nogui",
  "working_dir": "/home/user/minecraft",
  "port": 25565
}
```

### Discord Bot
```json
{
  "name": "My Bot",
  "command": "python3 bot.py",
  "working_dir": "/home/user/bot",
  "port": null
}
```

### Web Server
```json
{
  "name": "Web API",
  "command": "node index.js",
  "working_dir": "/home/user/api",
  "port": 3000
}
```

Больше примеров в `EXAMPLES.md`!

## 🔧 Технологии

- **Backend**: Python 3.8+, Flask, Socket.IO, psutil, SQLite
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla), Socket.IO Client
- **Платформа**: WSL2 (Ubuntu 22.04)
- **Архитектура**: REST API + WebSocket

## 📊 Возможности

### Реализовано ✅
- ✅ Создание/удаление серверов
- ✅ Запуск/остановка/перезапуск
- ✅ Мониторинг системы (CPU, RAM, диск, сеть)
- ✅ Статистика каждого сервера
- ✅ Интерактивная консоль
- ✅ Отправка команд
- ✅ Автоматическое чтение логов
- ✅ WebSocket real-time обновления
- ✅ Простая аутентификация
- ✅ SQLite база данных
- ✅ Адаптивный UI

### Планируется (можно добавить)
- ⏱️ Планировщик задач (cron)
- 💾 Автоматические бэкапы
- 📧 Email/Telegram уведомления
- 📊 Графики истории
- 🐳 Docker интеграция
- 👥 Мультипользовательский режим
- 🔐 OAuth авторизация

## 🛠️ Требования

### Минимальные
- Windows 10/11 с WSL2
- Ubuntu 22.04
- 2GB RAM
- Python 3.8+

### Рекомендуемые
- Windows 11
- 8GB+ RAM
- Python 3.10+
- SSD диск

## 📞 Поддержка

### Если что-то не работает:

1. **Проверьте INSTALLATION.md** - там есть раздел "Решение проблем"
2. **Посмотрите логи**: `tail -f backend/logs/app.log`
3. **Проверьте консоль браузера**: F12 → Console
4. **Проверьте порты**: `sudo lsof -i :5000`

### Типичные проблемы:

#### Backend не запускается
```bash
cd backend
source venv/bin/activate
python3 app.py
```

#### "Module not found"
```bash
pip install -r requirements.txt
```

#### WebSocket не подключается
- Убедитесь что backend запущен на порту 5000
- Проверьте URL в `frontend/index.html`

## 🎯 Следующие шаги

1. ✅ Прочитайте `INSTALLATION.md`
2. ✅ Запустите панель через `install.sh`
3. ✅ Создайте первый тестовый сервер
4. ✅ Изучите примеры в `EXAMPLES.md`
5. ✅ Настройте автозапуск
6. ✅ Измените пароль admin!

## 📚 Полезные ссылки

- **README.md** - полное описание проекта
- **INSTALLATION.md** - установка на ваш ноутбук
- **QUICKSTART.md** - быстрый старт за 5 минут
- **EXAMPLES.md** - 50+ примеров конфигураций
- **docs/README.md** - техническая документация

## 🎉 Результат

После установки у вас будет:

✅ Веб-панель на `http://localhost:3000`
✅ API на `http://localhost:5000`
✅ Возможность управлять любыми серверами
✅ Мониторинг ресурсов в реальном времени
✅ Красивый современный интерфейс
✅ Автоматическое логирование

**Ваш ноутбук = полноценный хостинг-сервер! 🚀**

---

## 🚀 НАЧНИТЕ С `INSTALLATION.md` 🚀

Удачи! 🎯
