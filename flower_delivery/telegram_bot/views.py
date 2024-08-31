from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.ext import Application, CommandHandler
from django.conf import settings
from .bot import start

bot_application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

bot_application.add_handler(CommandHandler('start', start))

@csrf_exempt
async def webhook(request):
    if request.method == 'POST':
        update = Update.de_json(request.body.decode('utf-8'))
        await bot_application.process_update(update)
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)






