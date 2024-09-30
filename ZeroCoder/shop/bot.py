import os
import django
from django.shortcuts import redirect
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import TOKEN, ADMIN_CHAT_ID
django.setup()
from .models import Order  # Импорт моделей только после инициализации Django


# Установите переменную окружения с указанием на файл настроек вашего проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ZeroCoder.settings')

# Настройка Django
django.setup()  # Эта строка должна быть перед любым импортом, связанным с моделями

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Welcome to the Flower Delivery Bot!')

# Уведомление об новых заказах
async def notify_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    orders = Order.objects.filter(status='new')
    if orders.exists():
        message = 'New Orders:\n'
        for order in orders:
            message += f'Order {order.id} for {order.user.username}, Delivery Address: {order.delivery_address}\n'
        await update.message.reply_text(message)
    else:
        await update.message.reply_text('No new orders.')

# Отправка уведомления через Telegram при оформлении заказа
def cart(request):
    # Код оформления заказа
    address = 'some_address'  # Вставьте реальный адрес
    message = f'New order from {request.user.username}, delivery address: {address}'
    requests.get(f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ADMIN_CHAT_ID}&text={message}')
    return redirect('order_history')

# Инициализация и запуск бота
def main():
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('orders', notify_admin))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()





