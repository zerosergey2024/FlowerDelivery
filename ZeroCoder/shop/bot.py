# shop/bot.py

import os
import django
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, Updater
from django.conf import settings
from django.core.management.base import BaseCommand
from .models import Order  # Убедитесь, что модель Order импортируется корректно

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ZeroCoder.settings')
django.setup()

# Логика обработки команд Telegram
def start(update: Update, context: CallbackContext):
    """Отправка приветственного сообщения при команде /start"""
    update.message.reply_text("Добро пожаловать в сервис доставки цветов! Введите /order для заказа.")

def order(update: Update, context: CallbackContext):
    """Отправка сообщения с заказами пользователя"""
    user = update.message.from_user
    orders = Order.objects.filter(telegram_id=user.id)  # Используйте telegram_id, если это поле у вас в модели Order

    if not orders:
        update.message.reply_text("У вас нет заказов.")
    else:
        message = "Ваши заказы:\n"
        for order in orders:
            message += f"- Заказ #{order.id}: {order.status} - {order.total_price} USD\n"
        update.message.reply_text(message)

def unknown(update: Update, context: CallbackContext):
    """Ответ на неизвестные команды"""
    update.message.reply_text("Извините, я не понимаю эту команду.")

class Command(BaseCommand):
    help = 'Запуск Telegram бота'

    def handle(self, *args, **kwargs):
        # Укажите свой токен Telegram API
        bot_token = settings.TELEGRAM_BOT_TOKEN # Используйте переменные окружения
        updater = Updater(token=bot_token, use_context=True)
        dispatcher = updater.dispatcher

        # Обработчики команд
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("order", order))

        # Обработчик неизвестных команд
        dispatcher.add_handler(CommandHandler("unknown", unknown))

        # Запуск бота
        updater.start_polling()
        updater.idle()  # Ожидание завершения работы бота


