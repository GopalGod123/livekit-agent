from gtts import gTTS
import os

def speak_text(text, filename="response.mp3"):
    tts = gTTS(text)
    tts.save(filename)
    return filename
