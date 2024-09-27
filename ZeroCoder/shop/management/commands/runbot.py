import os
import django
from telegram import Update, Bot
from telegram.ext import CommandHandler, CallbackContext, Updater
from django.core.management.base import BaseCommand
from shop.models import Order

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ZeroCoder.settings')  # Имя вашего проекта
django.setup()

# Логика обработки команд Telegram
def start(update: Update, context: CallbackContext):
    """Отправка приветственного сообщения при команде /start"""
    update.message.reply_text("Добро пожаловать в сервис доставки цветов! Введите /order для заказа.")

def order(update: Update, context: CallbackContext):
    """Отправка сообщения с заказами пользователя"""
    user = update.message.from_user
    orders = Order.objects.filter(user__telegram_id=user.id)

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
        bot_token = 'YOUR_BOT_TOKEN_HERE'
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

        if __name__ == '__main__':
            import os
            import django
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_delivery.settings')
            django.setup()
            