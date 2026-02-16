#!/bin/bash

# 🚀 Laptop Hosting Panel - Установочный скрипт
# Автоматическая установка и настройка панели хостинга

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   🖥️  Laptop Hosting Panel - Установка                   ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функции для вывода
info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка WSL
if ! grep -q Microsoft /proc/version; then
    error "Этот скрипт должен запускаться в WSL!"
    exit 1
fi

info "Обнаружен WSL. Продолжаем установку..."

# Обновление системы
info "Обновление списка пакетов..."
sudo apt-get update -qq

# Установка зависимостей
info "Установка системных зависимостей..."
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    build-essential \
    > /dev/null 2>&1

# Проверка Python
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
info "Версия Python: $PYTHON_VERSION"

if (( $(echo "$PYTHON_VERSION < 3.8" | bc -l) )); then
    error "Требуется Python 3.8 или выше!"
    exit 1
fi

# Переход в директорию backend
cd backend

# Создание виртуального окружения
if [ ! -d "venv" ]; then
    info "Создание виртуального окружения..."
    python3 -m venv venv
else
    info "Виртуальное окружение уже существует"
fi

# Активация виртуального окружения
info "Активация виртуального окружения..."
source venv/bin/activate

# Установка Python пакетов
info "Установка Python зависимостей..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1

# Создание .env файла
if [ ! -f ".env" ]; then
    info "Создание файла конфигурации..."
    cp .env.example .env
    
    # Генерация случайного SECRET_KEY
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    sed -i "s/your-secret-key-change-this-in-production/$SECRET_KEY/" .env
    
    info "Файл .env создан с уникальным SECRET_KEY"
else
    warn "Файл .env уже существует, пропускаем..."
fi

# Создание необходимых директорий
info "Создание директорий..."
mkdir -p data logs servers

# Инициализация базы данных
info "Инициализация базы данных..."
python3 -c "from models.database import init_db; init_db()" 2>/dev/null || true

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   ✅ Установка завершена успешно!                        ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
info "Для запуска сервера выполните:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
info "Backend будет доступен на: http://localhost:5000"
echo ""
info "Учетные данные по умолчанию:"
echo "  Логин: admin"
echo "  Пароль: admin"
warn "⚠️  ОБЯЗАТЕЛЬНО измените пароль после первого входа!"
echo ""

# Опция автоматического запуска
read -p "Запустить сервер сейчас? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    info "Запуск сервера..."
    python app.py
fi
