# shop/management/commands/startbot.py

from django.core.management.base import BaseCommand
from telegram.ext import Application, CommandHandler
from ...bot import start, order, unknown  # Импортируем функции команд
from django.conf import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Start the Telegram bot'

    def handle(self, *args, **kwargs):
        # Укажите свой токен Telegram API
        bot_token = settings.TELEGRAM_BOT_TOKEN

        # Инициализация приложения Telegram
        application = Application.builder().token(bot_token).build()

        # Обработчики команд
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("order", order))

        # Обработчик неизвестных команд
        application.add_handler(CommandHandler("unknown", unknown))

        # Запуск бота
        application.run_polling()



