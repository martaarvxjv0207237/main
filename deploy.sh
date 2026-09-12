#!/bin/bash

# Скрипт для развертывания на VPS

set -e

echo "🚀 Начало развертывания Telegram бота..."

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo "⚠️  Файл .env не найден!"
    echo "Скопируйте .env.example в .env и добавьте ваш TELEGRAM_BOT_TOKEN"
    exit 1
fi

# Проверка наличия Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен!"
    echo "Установите Docker: https://docs.docker.com/engine/install/"
    exit 1
fi

# Проверка наличия Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен!"
    echo "Установите Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

# Остановка существующих контейнеров
echo "🛑 Остановка существующих контейнеров..."
docker-compose down || true

# Сборка и запуск
echo "🔨 Сборка Docker образа..."
docker-compose build

echo "▶️  Запуск бота..."
docker-compose up -d

echo "✅ Бот успешно развернут!"
echo ""
echo "Полезные команды:"
echo "  docker-compose logs -f        - Просмотр логов"
echo "  docker-compose ps             - Статус контейнеров"
echo "  docker-compose restart        - Перезапуск бота"
echo "  docker-compose down           - Остановка бота"
echo "  docker-compose up -d          - Запуск бота"
