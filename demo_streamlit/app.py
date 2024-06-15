# app.py

import streamlit as st
import requests
import subprocess
import sys
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# Clave de la API y URL
API_KEY = "y7jjmBBP.pglw383yahVorfRBwK6Zo323dJ1lpnjN"
URL = "https://payload.vextapp.com/hook/S590KL2AS8/catch/T-Assistant"

# Configuración de la página de Streamlit
st.set_page_config(layout="wide")  # Establecer el layout de la página en ancho completo

# Colocar el logo en la parte superior izquierda
st.image("demo_streamlit/LOGOTIPO TERRAGENE Rev.1_Fondo Transparente-E.png", width=300)  # Ajusta el ancho según tus necesidades
st.title("Terragene Assistant")

# Inicializar el estado de la conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Función para manejar el envío del mensaje
def send_message():
    user_input = st.session_state.user_input
    if user_input:
        # Agregar el mensaje del usuario a la conversación
        st.session_state.messages.append(f"Tú: {user_input}")

        # Hacer la solicitud a la API
        headers = {"Content-Type": "application/json", "Api-Key": API_KEY}
        data = {"payload": user_input}
        
        try:
            response = requests.post(URL, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()

            # Extraer y agregar la respuesta de la API a la conversación
            api_response_text = result.get('text', 'Sin respuesta')
            st.session_state.messages.append(f"API: {api_response_text}")
        except requests.exceptions.RequestException as e:
            st.session_state.messages.append(f"Error: {e}")
        
        # Limpiar el campo de entrada
        st.session_state.user_input = ""

# Mostrar los mensajes en el chat
for message in st.session_state.messages:
    st.write(message)

# Entrada de texto para el mensaje del usuario
st.text_input("Tú:", key="user_input")

# Botón para enviar el mensaje
if st.button("Enviar"):
    send_message()
    st.experimental_rerun()

# Ejecutar el segundo script (Telegram bot) en segundo plano
def run_telegram_bot():
    subprocess.Popen([sys.executable, "Telegram/app.py"])

# Ejecutar el bot de Telegram al iniciar la aplicación
run_telegram_bot()

# Código del bot de Telegram
def telegram_bot():
    # Clave API y URL de la API
    API_KEY = "y7jjmBBP.pglw383yahVorfRBwK6Zo323dJ1lpnjN"
    API_URL = "https://payload.vextapp.com/hook/S590KL2AS8/catch/T-Assistant"

    # Función para manejar los mensajes y hacer la solicitud a la API
    async def handle_message(update: Update, context: CallbackContext) -> None:
        user_message = update.message.text
        response_text = await make_api_request(user_message)
        await update.message.reply_text(response_text)

    # Función para hacer la solicitud a la API
    async def make_api_request(payload: str) -> str:
        headers = {
            'Content-Type': 'application/json',
            'Apikey': f"Api-Key {API_KEY}"
        }
        data = {
            'payload': payload
        }
        try:
            response = requests.post(API_URL, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result.get('text', 'Sin respuesta de la API')
        except requests.exceptions.RequestException as e:
            return f'Error al contactar la API: {e}'

    def main():
        # Coloca aquí tu token
        token = '7294271445:AAFQcFGbsEUHGKtjWNhk7HjQEiPnHIwdm94'

        # Crea el Application y pásale tu token
        application = Application.builder().token(token).build()

        # Enlaza todos los mensajes de texto a la función handle_message
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Inicia el bot
        application.run_polling()

    if __name__ == '__main__':
        main()

# Llamar a la función principal del bot si se ejecuta como script principal
if __name__ == '__main__':
    telegram_bot()
