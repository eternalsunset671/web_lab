#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/eternalsunset671/web_lab.git"
APP_DIR="/var/www/university"

DB_NAME="university_db"
DB_USER="university_user"
DB_PASS="password"
DJANGO_SECRET="SecretKey"

echo "=== Обновление системы и установка базовых пакетов ==="
sudo apt update
sudo apt install -y \
    python3 python3-dev build-essential libpq-dev \
    postgresql postgresql-contrib \
    nginx git curl

echo "=== Установка Poetry ==="
if ! command -v poetry &> /dev/null; then
    curl -sSL https://install.python-poetry.org | python3 -
fi
export PATH="$HOME/.local/bin:$PATH"

echo "=== Настройка PostgreSQL ==="
sudo -u postgres psql -c "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASS}';" || true
sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};" || true

echo "=== Клонирование репозитория ==="
sudo rm -rf "$APP_DIR"
sudo git clone "$REPO_URL" "$APP_DIR"
sudo chown -R $USER:www-data "$APP_DIR"
cd "$APP_DIR"

echo "=== Установка зависимостей через Poetry ==="
poetry config virtualenvs.in-project true
poetry install --no-root --no-interaction

echo "=== Переменные окружения ==="
cat > .env <<EOF
DJANGO_SECRET_KEY=${DJANGO_SECRET}
DB_NAME=${DB_NAME}
DB_USER=${DB_USER}
DB_PASSWORD=${DB_PASS}
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=127.0.0.1,localhost,192.168.149.154
CSRF_TRUSTED_ORIGINS=http://127.0.0.1,http://192.168.149.154
EOF
chmod 640 .env

echo "=== Миграции и загрузка данных ==="
python manage.py migrate
python manage.py loaddata data.json

echo "=== Установка gunicorn systemd unit ==="
sudo cp deploy/systemd/gunicorn.service /etc/systemd/system/gunicorn.service
sudo systemctl daemon-reload
sudo systemctl enable --now gunicorn

echo "=== Установка nginx конфига ==="
sudo cp deploy/nginx/university.conf /etc/nginx/sites-available/university.conf
sudo ln -sf /etc/nginx/sites-available/university.conf /etc/nginx/sites-enabled/university.conf
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

echo "=== ДЕПЛОЙ ЗАВЕРШЕН ==="
