import streamlit as st
import requests
import subprocess
import sys
import nest_asyncio

# Aplicar nest_asyncio
nest_asyncio.apply()

# Clave de la API y URL
API_KEY = "y7jjmBBP.pglw383yahVorfRBwK6Zo323dJ1lpnjN"
URL = "https://payload.vextapp.com/hook/S590KL2AS8/catch/T-Assistant"

# Configuración de la página de Streamlit
st.set_page_config(layout="wide")

# Ejecutar el bot de Telegram al iniciar la aplicación
def run_telegram_bot():
    script_path = "/mount/src/vext/Telegram/bot.py"
    subprocess.Popen([sys.executable, script_path])

run_telegram_bot()

# Colocar el logo en la parte superior izquierda
st.image("demo_streamlit/LOGOTIPO TERRAGENE Rev.1_Fondo Transparente-E.png", width=300)
st.title("Terragene Assistant")

# Inicializar el estado de la conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Inicializar el estado del input del usuario
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Función para manejar el envío del mensaje
def send_message():
    user_input = st.session_state.user_input
    if user_input:
        st.session_state.messages.append(f"Tú: {user_input}")
        headers = {"Content-Type": "application/json", "Api-Key": API_KEY}
        data = {"payload": user_input}
        
        try:
            response = requests.post(URL, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            api_response_text = result.get('text', 'Sin respuesta')
            st.session_state.messages.append(f"API: {api_response_text}")
        except requests.exceptions.RequestException as e:
            st.session_state.messages.append(f"Error: {e}")
        
        st.session_state["user_input"] = ""

# Mostrar los mensajes en el chat
for message in st.session_state.messages:
    st.write(message)

# Entrada de texto para el mensaje del usuario
st.text_input("Tú:", key="user_input")

# Botón para enviar el mensaje
if st.button("Enviar"):
    send_message()
    st.experimental_rerun()
