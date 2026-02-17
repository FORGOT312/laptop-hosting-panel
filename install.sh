#!/bin/bash
echo "════════════════════════════════════"
echo "  HostPanel v2 — Установка"
echo "════════════════════════════════════"

cd "$(dirname "$0")/backend"

# Зависимости системы
sudo apt-get update -qq
sudo apt-get install -y python3 python3-pip python3-venv -qq

# Venv
python3 -m venv venv
source venv/bin/activate

# Pip
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Конфиг
[ ! -f .env ] && echo "SECRET_KEY=$(python3 -c 'import secrets;print(secrets.token_hex(32))')" > .env

# Директории
mkdir -p data logs servers

echo ""
echo "✅ Готово! Запустите:"
echo "   cd backend && source venv/bin/activate && python app.py"
echo ""
echo "Панель будет доступна на http://localhost:5000"
echo "Логин: admin  |  Пароль: admin"
