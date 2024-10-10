import streamlit as st
import os
import time
import glob
from gtts import gTTS
from googletrans import Translator
import base64

st.title("Conversión de Texto a Audio con Traducción")

# Mostrar GIF animado utilizando HTML
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

st.subheader("Convierte y traduce texto a audio")
st.write(
    'Este servicio permite traducir texto y convertirlo en audio en diferentes idiomas. '
)

# Área de texto para ingresar contenido
st.markdown("Introduce el texto que deseas traducir y escuchar:")
text = st.text_area("Ingrese el texto a traducir y escuchar.")

# Selección de idioma de destino
option_lang = st.selectbox("Selecciona el idioma de traducción y síntesis", ("Español", "Inglés", "Árabe"))
lang_dict = {"Español": "es", "Inglés": "en", "Árabe": "ar"}
target_lang = lang_dict[option_lang]

# Función de traducción y síntesis de voz
def translate_and_text_to_speech(text, target_lang):
    translator = Translator()
    translation = translator.translate(text, dest=target_lang)
    translated_text = translation.text
    tts = gTTS(translated_text, lang=target_lang)
    my_file_name = translated_text[:20] or "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, translated_text

if st.button("Traducir y Convertir a Audio"):
    result, translated_text = translate_and_text_to_speech(text, target_lang)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown("## Texto traducido:")
    st.write(translated_text)
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
