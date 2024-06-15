import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

API_KEY = "y7jjmBBP.pglw383yahVorfRBwK6Zo323dJ1lpnjN"
API_URL = "https://payload.vextapp.com/hook/S590KL2AS8/catch/T-Assistant"

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    response_text = await make_api_request(user_message)
    await update.message.reply_text(response_text)

async def make_api_request(payload: str) -> str:
    headers = {
        'Content-Type': 'application/json',
        'Apikey': f"Api-Key {API_KEY}"
    }
    data = {'payload': payload}
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result.get('text', 'Sin respuesta de la API')
    except requests.exceptions.RequestException as e:
        return f'Error al contactar la API: {e}'

def main():
    token = '7294271445:AAFQcFGbsEUHGKtjWNhk7HjQEiPnHIwdm94'
    application = Application.builder().token(token).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == '__main__':
    main()
