import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser
import os
import cv2
import random
import smtplib
import sys
import operator
import PyPDF2
import requests
from bs4 import BeautifulSoup
from pywikihow import search_wikihow


# Alexa will recognize your voice!!
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)



# Email
def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('rahul1234@gmail.com','rahul2006')  #Email and Password 
    server.sendmail('rahul1234@gmail.com',to,content)
    server.close()

def talk(text):
    engine.say(text)
    engine.runAndWait()

def wish():

    time = datetime.datetime.now().strftime('%H')

    if(time>="0" and time<="12"):
        talk("good morning sir")
    elif(time>"12" and time<"18"):
        talk("good afternoon sir")
    else:
        talk("good evening sir")
    talk("I am alexa , please tell me how may I help you")

if __name__ == "__main__":
    talk("Hello, How are you sir")
    wish()
# Using your Microphone as a source and calling the speech_recognition to the source !!

def take_command():  
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source,duration=0.5)
            listener.pause_threshold =1
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


# Read PDF
def pdf_reader():
    book = open('C:\\Users\\acer\\Desktop\\work\\Calculator with python\\boss.pdf','rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    talk(f"Total numbers of pages in this book {pages}")
    print(f"Total numbers of pages in this book {pages}")
    talk("sir please enter the page number i have to read")
    page_number = int(input("please enter the page number: "))
    page = pdfReader.getPage(page_number)
    reading = page.extractText()
    talk(reading)

def run_alexa():
    command = take_command()
    print (command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('Playing' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk('Current time is ' + time)
    elif 'wikipedia' in command:
        person = command.replace('wikipedia', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
    elif 'eat' in command:
        talk('I have a headache, so i cant give you any thing right now')
    elif 'joke' in command:
        print(pyjokes.get_joke())
        talk(pyjokes.get_joke())
    elif 'open youtube' in command:
        webbrowser.open("youtube.com")
    elif 'open google' in command:
        talk("sir, what should I search on google")
        cp = take_command().lower()
        webbrowser.open(f"{cp}")
    elif 'start music' in command:
        talk('starting sir wait a second')
        music_dir = 'H:\\Songs'
        songs = os.listdir(music_dir)
        print(songs)
        rd = random.choice(songs)
        os.startfile(os.path.join(music_dir, rd))
    elif 'open notepad' in command:
        notebook_path = "C:\\ProgramData\Microsoft\\Windows\\Start Menu\\Programs\\Accessories\\Notepad"
        os.startfile(notebook_path)
    elif 'open command prompt' in command:
        os.system("start cmd")
    elif 'open camera' in command:
        cap = cv2.VideoCapture(0)
        while True:
            ret, img = cap.read()
            cv2.imshow('webcam',img)
            k = cv2.waitKey(50)
            if k==27:
                break
        cap.release()
        cv2.destroyAllWindows()
    elif "email to rahul" in command:
        try:
            talk("sir, what should I say?")
            content = take_command().lower()
            to = 'bipulkhosla231@gmail.com'
            sendEmail(to,content)
            talk("Email has been sent to rahul")
        
        except Exception as e:
            print(e)
            talk('sir, there is some error')

    elif "no thanks" in command:
        talk('thanks for using me sir, have a good day.')
        sys.exit()

    # Calculations!!
    elif "do some calculations" in command:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            talk("Say what you want to calculate, example: 4 plus 4")
            print("listening......")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        my_string = r.recognize_google(audio)
        print(my_string)
        
        def get_operator_fn(op):
            return {
                '+' : operator.add,  #Plus
                '-' : operator.sub,  #Minus
                'x' : operator.mul,  #Multiplied by
                'divided' : operator.__truediv__, #divided
            }[op]
        def eval_binary_expr(op1, oper, op2):
            op1,op2 = int(op1), int(op2)
            return get_operator_fn(oper)(op1,op2)
        talk("your result is")
        print(f"your result is: {eval_binary_expr(*(my_string.split()))}")
        talk(eval_binary_expr(*(my_string.split())))

    elif "read pdf" in command:
        pdf_reader()

    # Weather Forecast
    elif "temperature" in command:
        search = "temperature in punjab"
        url = f"https://www.google.com/search?q={search}"
        r = requests.get(url)
        data = BeautifulSoup(r.text,"html.parser")
        temp = data.find("div", class_="BNeawe").text
        print(f"current {search} is {temp}")
        talk(f"current {search} is {temp}")

    elif "activate how to do mode" in command:
        talk("How to do mode is activated please tell me what you want to know")
        how = take_command()
        max_results = 1
        how_to = search_wikihow(how, max_results)
        assert len(how_to) == 1
        how_to[0].print()
        talk(how_to[0].summary)
        
        

    else:
        talk('Please Say the command again.')

    talk('sir,do you have any other work')
        
while True:
    run_alexa()




