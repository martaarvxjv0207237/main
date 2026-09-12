# Telegram Bot - Deployment Guide

Полнофункциональный телеграм-бот с инструкциями по развертыванию на VPS.

## 🚀 Быстрый старт

### 1. Создание бота в Telegram

1. Найдите [@BotFather](https://t.me/botfather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям и создайте имя для бота
4. Скопируйте токен, который выдаст BotFather

### 2. Настройка локально

```bash
# Клонируйте репозиторий
git clone <your-repo-url>
cd telegram-bot

# Создайте .env файл
cp .env.example .env

# Отредактируйте .env и добавьте токен
nano .env
# Замените your_bot_token_here на реальный токен

# Установите зависимости
pip install -r requirements.txt

# Запустите бота
python bot.py
```

## 🖥️ Развертывание на VPS

### Метод 1: Docker (Рекомендуется)

#### Предварительные требования
- VPS с Ubuntu 20.04+ или Debian 11+
- Docker и Docker Compose

#### Установка Docker

```bash
# Обновите систему
sudo apt update && sudo apt upgrade -y

# Установите Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установите Docker Compose
sudo apt install docker-compose -y

# Добавьте пользователя в группу docker
sudo usermod -aG docker $USER
newgrp docker
```

#### Развертывание

```bash
# Подключитесь к VPS
ssh user@your-vps-ip

# Клонируйте репозиторий
git clone <your-repo-url>
cd telegram-bot

# Создайте .env файл
cp .env.example .env
nano .env  # Добавьте ваш токен

# Сделайте скрипт исполняемым
chmod +x deploy.sh

# Запустите развертывание
./deploy.sh
```

#### Управление ботом

```bash
# Просмотр логов
docker-compose logs -f

# Перезапуск
docker-compose restart

# Остановка
docker-compose down

# Запуск
docker-compose up -d

# Обновление после изменений
git pull
docker-compose down
docker-compose build
docker-compose up -d
```

### Метод 2: Systemd (Без Docker)

```bash
# Подключитесь к VPS
ssh user@your-vps-ip

# Установите Python и зависимости
sudo apt update
sudo apt install python3 python3-pip -y

# Клонируйте репозиторий
git clone <your-repo-url> /home/$USER/telegram-bot
cd /home/$USER/telegram-bot

# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Создайте .env файл
cp .env.example .env
nano .env  # Добавьте ваш токен

# Настройте systemd service
sudo cp systemd/telegram-bot.service /etc/systemd/system/
sudo nano /etc/systemd/system/telegram-bot.service
# Измените пути и пользователя при необходимости

# Запустите сервис
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot

# Проверьте статус
sudo systemctl status telegram-bot
```

#### Управление через systemd

```bash
# Просмотр логов
sudo journalctl -u telegram-bot -f

# Перезапуск
sudo systemctl restart telegram-bot

# Остановка
sudo systemctl stop telegram-bot

# Запуск
sudo systemctl start telegram-bot

# Обновление после изменений
cd /home/$USER/telegram-bot
git pull
sudo systemctl restart telegram-bot
```

## 📝 Структура проекта

```
telegram-bot/
├── bot.py                  # Основной файл бота
├── requirements.txt        # Python зависимости
├── .env.example           # Пример конфигурации
├── .env                   # Конфигурация (создается вами)
├── Dockerfile             # Docker образ
├── docker-compose.yml     # Docker Compose конфигурация
├── deploy.sh              # Скрипт развертывания
├── systemd/
│   └── telegram-bot.service  # Systemd unit файл
└── README.md              # Эта документация
```

## 🛠️ Разработка и расширение

### Добавление новых команд

Откройте `bot.py` и добавьте новую функцию-обработчик:

```python
async def my_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Описание команды"""
    await update.message.reply_text("Ответ команды")

# В функции main() добавьте:
application.add_handler(CommandHandler("mycommand", my_command))
```

### Добавление обработки фото/документов

```python
from telegram.ext import MessageHandler, filters

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка фотографий"""
    await update.message.reply_text("Получил фото!")

# В main():
application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
```

## 🔧 Устранение неполадок

### Бот не запускается

1. Проверьте токен в `.env` файле
2. Убедитесь, что токен правильно скопирован (без пробелов)
3. Проверьте логи: `docker-compose logs` или `sudo journalctl -u telegram-bot`

### Бот не отвечает

1. Проверьте, что бот запущен: `docker-compose ps` или `sudo systemctl status telegram-bot`
2. Проверьте интернет-соединение на VPS
3. Убедитесь, что токен действителен

### Ошибки при развертывании

1. Проверьте, что Docker установлен: `docker --version`
2. Проверьте, что Docker Compose установлен: `docker-compose --version`
3. Убедитесь, что порты не заняты другими приложениями

## 📊 Мониторинг

### Просмотр ресурсов (Docker)

```bash
docker stats
```

### Просмотр использования памяти

```bash
free -h
```

### Автоматический перезапуск при сбое

Бот автоматически перезапускается при сбое благодаря:
- Docker: `restart: unless-stopped` в docker-compose.yml
- Systemd: `Restart=always` в service файле

## 🔐 Безопасность

1. **Никогда не коммитьте .env файл** - он в .gitignore
2. **Используйте сильные пароли** для VPS
3. **Настройте firewall** на VPS:
   ```bash
   sudo ufw allow ssh
   sudo ufw enable
   ```
4. **Регулярно обновляйте систему**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

## 📚 Дополнительные ресурсы

- [python-telegram-bot документация](https://docs.python-telegram-bot.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Docker документация](https://docs.docker.com/)

## 📄 Лицензия

MIT License

## 🤝 Поддержка

Если возникли вопросы или проблемы, создайте Issue в репозитории.
