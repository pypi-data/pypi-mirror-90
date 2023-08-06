import speech_recognition as sr
import pyttsx3

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
enginegirl = pyttsx3.init()
enginegirl.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def talkgirl(text):
    enginegirl.say(text)
    enginegirl.runAndWait()
