import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import pyowm
import requests
from bs4 import BeautifulSoup

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

owm = pyowm.OWM('8bc8cc477562745811d2b9a7eff9414d')

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    command = ''
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except:
        pass
    return command

def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'who is' in command:
        person = command.replace('who the heck is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'weather' in command:
        try:
            observation = owm.weather_at_place('New York, US')
            weather = observation.get_weather()
            temperature = weather.get_temperature('celsius')["temp"]
            status = weather.get_status()
            talk(f"The weather is currently {status} with a temperature of {temperature} degrees Celsius.")
        except:
            talk("Sorry, I couldn't retrieve the weather information.")
    elif 'news' in command:
        try:
            url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=a67cbc84eefe4e71aca0fd79af3e8688'
            response = requests.get(url)
            news = response.json()
            articles = news['articles']
            talk("Here are the top headlines:")
            for article in articles[:5]:
                talk(article['title'])
        except:
            talk("Sorry, I couldn't fetch the latest news.")
    else:
        talk('Please say the command again.')

while True:
    run_alexa()
