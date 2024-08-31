from telegram import Update, Bot
from telegram.ext import CommandHandler, Updater, CallbackContext, Application
from django.http import JsonResponse
from django.conf import settings
from flower_delivery.orders.models import Order


bot = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Добро пожаловать! Я бот для обработки заказов.')

async def get_orders(update: Update, context: CallbackContext):
    orders = Order.objects.filter(user__telegram_id=update.message.chat_id)
    if orders.exists():
        response = "\n".join([f"Заказ #{order.id}: {order.status} - {order.total_price} руб." for order in orders])
        await update.message.reply_text(response)
    else:
        await update.message.reply_text('У вас пока нет заказов.')

def main():
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("orders", get_orders))

    bot.run_polling()

if __name__ == '__main__':
    main()

