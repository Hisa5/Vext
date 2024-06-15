import streamlit as st
import requests
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
URL = os.getenv("API_URL")



# Configuración de la página de Streamlit
st.set_page_config(layout="wide")  # Establecer el layout de la página en ancho completo

# Colocar el logo en la parte superior izquierda
st.image("demo_streamlit/LOGOTIPO TERRAGENE Rev.1_Fondo Transparente-E.png", width=300)  # Ajusta el ancho según tus necesidades (doble del tamaño original de 150)
st.title("Terragene Assistant")

# Inicializar el estado de la conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar los mensajes en el chat
for message in st.session_state.messages:
    st.write(message)

# Entrada de texto para el mensaje del usuario
user_input = st.text_input("Tú:", key="user_input")

# Función para manejar el envío del mensaje
def send_message():
    if user_input:
        # Agregar el mensaje del usuario a la conversación
        st.session_state.messages.append(f"Tú: {user_input}")

        # Hacer la solicitud a la API
        headers = {"Content-Type": "application/json", "Apikey": f"Api-Key {API_KEY}"}
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

# Botón para enviar el mensaje
if st.button("Enviar", on_click=send_message):
    st.experimental_rerun()
