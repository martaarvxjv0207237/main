#!/usr/bin/env python3
"""
Telegram Bot - Main Application
"""
import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Привет, {user.mention_html()}!\n\n"
        f"Я телеграм-бот, готовый к работе.\n\n"
        f"Доступные команды:\n"
        f"/start - Начать работу с ботом\n"
        f"/help - Показать справку\n"
        f"/about - Информация о боте"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "📚 <b>Справка по командам:</b>\n\n"
        "/start - Запустить бота\n"
        "/help - Показать это сообщение\n"
        "/about - Узнать больше о боте\n\n"
        "Вы также можете отправить мне любое текстовое сообщение, "
        "и я отвечу на него!"
    )
    await update.message.reply_html(help_text)


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send information about the bot."""
    about_text = (
        "ℹ️ <b>О боте</b>\n\n"
        "Это телеграм-бот, созданный на Python с использованием "
        "библиотеки python-telegram-bot.\n\n"
        "Версия: 1.0.0\n"
        "Разработано для развертывания на VPS"
    )
    await update.message.reply_html(about_text)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    text = update.message.text
    response = f"Вы написали: {text}\n\nЯ получил ваше сообщение! 👍"
    await update.message.reply_text(response)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by Updates."""
    logger.error(f"Exception while handling an update: {context.error}")


def main() -> None:
    """Start the bot."""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable is not set!")
        raise ValueError("TELEGRAM_BOT_TOKEN is required")
    
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    application.add_error_handler(error_handler)

    logger.info("Bot started successfully!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
