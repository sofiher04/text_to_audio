import streamlit as st
import os
import time
import glob
from gtts import gTTS
import base64

st.title("Conversión de Texto a Audio")

# Mostrar GIF animado utilizando HTML para garantizar la reproducción
gif_path = 'Text-to-speech.gif'
gif_html = f'<img src="data:image/gif;base64,{base64.b64encode(open(gif_path, "rb").read()).decode()}" width="350" alt="Text to Speech">'
st.markdown(gif_html, unsafe_allow_html=True)

with st.sidebar:
    st.subheader("Escribe y/o selecciona texto para ser escuchado.")

# Crear carpeta "temp" si no existe
try:
    os.mkdir("temp")
except FileExistsError:
    pass

st.subheader("Conoce uno de los beneficios de convertir texto a audio")
st.write(
    'En el ámbito empresarial, la conversión de texto a voz puede automatizar una variedad de tareas. '
    'Los chatbots y asistentes virtuales de voz pueden responder preguntas frecuentes y brindar soporte al cliente de manera eficiente y económica. '
    'Esto libera a los empleados para realizar tareas más estratégicas y creativas.'
)

# Agregar enlace informativo
st.markdown(
    'Si quieres saber más, haz click [aquí](https://www.gomeranoticias.com/2023/09/08/por-que-convertir-texto-a-voz-una-mirada-a-las-ventajas-de-la-conversion-de-texto-en-audio/).'
)

# Área de texto para ingresar contenido
st.markdown("¿Quieres escucharlo? Copia el texto:")
text = st.text_area("Ingrese el texto a escuchar.")

# Selección de idioma
option_lang = st.selectbox("Selecciona el lenguaje", ("Español", "English"))
lg = 'es' if option_lang == "Español" else 'en'

def text_to_speech(text, lg):
    tts = gTTS(text, lang=lg)
    my_file_name = text[:20] or "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name

if st.button("Convertir a Audio"):
    result = text_to_speech(text, lg)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown("## Tu audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    # Enlace de descarga
    bin_str = base64.b64encode(audio_bytes).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{result}.mp3">Descargar archivo de audio</a>'
    st.markdown(href, unsafe_allow_html=True)

# Función para eliminar archivos temporales antiguos
def remove_files(n):
    now = time.time()
    for f in glob.glob("temp/*.mp3"):
        if os.stat(f).st_mtime < now - n * 86400:
            os.remove(f)
            print("Deleted", f)

remove_files(7)

