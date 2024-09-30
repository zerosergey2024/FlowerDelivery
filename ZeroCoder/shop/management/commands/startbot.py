from django.core.management.base import BaseCommand
from telegram.ext import Application, CommandHandler
from django.conf import settings
from ZeroCoder.shop.bot import start, order, unknown  # Убедитесь, что путь импорта корректный

class Command(BaseCommand):
    help = 'Start the Telegram bot'

    def handle(self, *args, **kwargs):
        # Получаем токен Telegram из настроек Django
        bot_token = settings.TELEGRAM_BOT_TOKEN

        # Инициализация приложения Telegram
        application = Application.builder().token(bot_token).build()

        # Добавляем обработчики команд
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("order", order))
        application.add_handler(CommandHandler("unknown", unknown))

        # Запуск бота с использованием polling
        application.run_polling()


