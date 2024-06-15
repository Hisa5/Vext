import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

# Especificar la ruta del archivo .env
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

API_KEY = os.getenv("API_KEY")
URL = os.getenv("API_URL")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Verificar que las variables de entorno se han cargado correctamente
if not API_KEY or not URL or not TELEGRAM_TOKEN:
    raise ValueError("Asegúrate de que todas las variables de entorno están definidas en el archivo .env")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hola! Soy tu asistente de Terragene. ¿Cómo puedo ayudarte hoy?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    headers = {"Content-Type": "application/json", "Apikey": f"Api-Key {API_KEY}"}
    data = {"payload": user_message}
    
    try:
        response = requests.post(URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        response_text = result.get('text', 'Sin respuesta')
        
        if not response_text:
            response_text = "Lo siento, no tengo una respuesta en este momento."
        
        await update.message.reply_text(response_text)
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"Error: {e}")

def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)

    application.add_handler(start_handler)
    application.add_handler(message_handler)
    
    application.run_polling()

if __name__ == '__main__':
    main()
