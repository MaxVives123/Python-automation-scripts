import os
import speech_recognition as sr
import pyttsx3
from openai import OpenAI

# Inicializar el cliente de OpenAI
client = OpenAI(api_key="aqui iria tu key de OpenAI")

# Inicializar el motor de síntesis de voz
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Reconociendo...")
        query = recognizer.recognize_google(audio, language='es-ES')
        print(f"Tú dijiste: {query}")
    except sr.UnknownValueError:
        print("Lo siento, no entendí eso.")
        query = None
    except sr.RequestError:
        print("Error en el servicio de reconocimiento de voz.")
        query = None

    return query

def assistant_response(query):
    if query:
        if 'patata' in query.lower():
            return "FACTS FACTS FACTS FACTS FACTS"
        else:
            # Crear una transmisión de completado de chat
            stream = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": query }],
                stream=True,
            )
            response = ""  # Inicializar una cadena vacía para almacenar la respuesta
            for chunk in stream:
                # Agregar el contenido del chunk a la cadena de respuesta
                response += chunk.choices[0].delta.content or ""
            return response.strip()  # Devolver la respuesta completa sin espacios en blanco adicionales al inicio y al final
    return "Lo siento, no pude procesar tu solicitud."






if __name__ == "__main__":
    while True:
        query = listen()
        if query:
            response = assistant_response(query)
            print(f"Respuesta: {response}")
            speak(response)
            if 'adiós' in query.lower():
                break
