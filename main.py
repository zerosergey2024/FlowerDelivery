import telegram
from telegram import Update
from telegram.ext import ContextTypes
from shop.models import Order


# Функция, которая будет вызываться при команде /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Добро пожаловать в бот доставки цветов! Введите /order, чтобы посмотреть свои заказы.')


# Функция, которая будет вызываться при команде /order
async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    orders = Order.objects.filter(user__telegram_id=user.id)

    if orders.exists():
        message = 'Ваши заказы:\n'
        for order in orders:
            message += f'Заказ #{order.id} для {order.user.username}, Адрес доставки: {order.delivery_address}\n'
        await update.message.reply_text(message)
    else:
        await update.message.reply_text('У вас нет новых заказов.')


# Функция, которая будет вызываться для обработки неизвестных команд
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Извините, я не понимаю эту команду.')


# Функция для уведомления администратора о создании нового заказа
def notify_admin(order):
    # Получаем токен и ID администратора из настроек
    bot_token = settings.TELEGRAM_BOT_TOKEN
    SECRET_KEY = settings.SECRET_KEY

    bot = telegram.Bot(token=bot_token)

    message = f'Новый заказ #{order.id} от пользователя {order.user.username}. Адрес доставки: {order.delivery_address}'

    # Отправляем сообщение администратору
    bot.send_message(chat_id=SECRET_KEY, text=message)


def notify_admin():
    return None