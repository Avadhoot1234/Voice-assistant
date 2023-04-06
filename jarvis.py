import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install speechRecognition
import datetime
import wikipedia  # pip install wikipedia
import webbrowser
import os
import smtplib
import wolframalpha
import psutil
import pyaudio
import cv2
import sys
import time
import pyautogui
import psutil
import PyPDF2
import pywhatkit as kit
from requests import get
from bs4 import BeautifulSoup
from pywikihow import search_wikihow
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import QTimer,QTime,QDate,Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from JarvisFinal import Ui_MainWindow
import MyAlarm
import pyjokes
import speedtest
from twilio.rest import Client

engine = pyttsx3.init('sapi5')  # speech API.
voices = engine.getProperty('voices')  # all voices
# 0 is for male,1 is female voice
# print(voices[0].id)
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate',180)

def speak(audio):
    jarvis.runAllMoviesDynamically("speaking")
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    jarvis.runAllMoviesDynamically("speaking")
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am Jarvis Sir. Please tell me how may I help you")

def sendEmail(to, content):
    os.startfile('C:\\Users\\Intel\\Desktop\\python\\Anmol Tripathi RCTSEC (2).pdf')
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('#####@gmail.com', '#######')
    server.sendmail('####@gmail.com', to, content)
    server.close()

class MainThread(QThread):
    import requests
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.TaskExecution() 

    def takeCommand(self):
        # It takes microphone input from the user and returns string output
        jarvis.runAllMoviesDynamically("listening")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            jarvis.runAllMoviesDynamically("Recognizing...")
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")

        except Exception as e:
            print(e)
            print("Say that again please...")
            return "None"
        return query
    
    def pdfreader(self):
        os.startfile('C:/Users/admin/Desktop/python/Anmol Tripathi RCTSEC (2).pdf')
        book='C:/Users/admin/Desktop/python/Anmol Tripathi RCTSEC (2).pdf'
        pdfReader=PyPDF2.PdfReader(book)
        pages=len(pdfReader.pages)
        speak(f"Total numbers of pages in this book {pages}")
        speak("sir please enter the page number I have to read")
        pg=int(input("Please enter the page number"))
        page =pdfReader.pages[pg]
        text=page.extract_text() 
        speak(text)


    def TaskExecution(self):
        wishMe()
        while True:
            self.query = self.takeCommand().lower()

            # Logic for executing tasks based on query
            if 'wikipedia' in self.query:
                speak('Searching Wikipedia...')
                self.query = self.query.replace("wikipedia", "")
                results = wikipedia.summary(self.query, sentences=2)
                speak("According to Wikipedia...")
                speak(results)

            elif 'open youtube' in self.query:
                webbrowser.open("youtube.com")

            elif "open command prompt" in self.query:
                os.system("start cmd")


            elif 'open google' in self.query:
                webbrowser.open("google.com")

            elif 'open stack overflow' in self.query:
                webbrowser.open("stackoverflow.com")

            elif 'play music' in self.query:
                music_dir = 'D:\\songs\\My Love Songs2'
                songs = os.listdir(music_dir)
                print(songs)
                os.startfile(os.path.join(music_dir, songs[0]))

            elif "calculate" in self.query: 
                app_id = "Wolframalpha api id"
                client = wolframalpha.Client(app_id)
                indx = self.query.lower().split().index('calculate')
                query = self.query.split()[indx + 1:]
                res = client.query(' '.join(query))
                answer = next(res.results).text
                print("The answer is " + answer)
                speak("The answer is " + answer)

            elif 'the time' in self.query:
            # formmatting the time
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir, the time is {strTime}")

            elif 'open notepad' in self.query:
                npath="C:\\Windows\\system32\\notepad.exe"
                os.startfile(npath)
            

            elif 'open camera' in self.query:
                cap=cv2.VideoCapture(0)
                while True:
                    ret,img=cap.read()
                    cv2.imshow('webcam',img)
                    k=cv2.waitkey(50)
                    if k==27:
                        break;
                cap.release()
                cv2.destroyAllWindows()

            elif 'send email ' in self.query:
                try:
                    speak("What should I say?")
                    content = self.takeCommand()
                    to = "abhay.dhumal9@gmail.com"
                    sendEmail(to, content)
                    speak("Email has been sent!")
                except Exception as e:
                    print(e)
                    speak("Sorry sir email couldn't be delivered")
            
            elif 'close notepad' in self.query:
                speak("okay sir closing the application")
                os.system("taskkill /f /im notepad.exe")
            
            elif "temperature" in self.query:
                search="Weather in Mumbai"
                url=f"https://www.google.com/search?q={search}"
                r=self.requests.get(url)
                data=BeautifulSoup(r.text,"html.parser")
                temp=data.find("div",class_="BNeawe").text
                speak(f"current {search} is {temp}")

            
            elif "search on google" in self.query:
                speak("Sir,What should I search on google")
                cm = self.takeCommand().lower()
                webbrowser.open(f"{cm}")
            
            elif "activate how to mode" in self.query:
                speak("How to  mode activeted")
                how=self.takeCommand()
                max_results=1
                how_to=search_wikihow(how,max_results)
                assert len(how_to)==1
                how_to[0].print()
                speak(how_to[0].summary)

            elif "send sms" in self.query:
                
                speak("What should I send sir")
                msz=self.takeCommand()
                account_sid = 'AC0b87856370c9649ab0029234109c438d'
                auth_token = '4ecbedc80dba9eed15c7ad739f155661'
                client = Client(account_sid, auth_token)

                message = client.messages \
                    .create(
                        body=msz,
                        from_='+15856393761',
                        to='+918779292839'
                    )

                print(message.sid)
                speak("Sir the message has been sent")
            
            elif "make a phone call" in self.query:
                account_sid='AC0b87856370c9649ab0029234109c438d'
                auth_token='4ecbedc80dba9eed15c7ad739f155661'
                client=Client(account_sid,auth_token)

                message=client.calls \
                    .create(
                        twiml='<Response><Say>This is test phone call</Say></Response>',
                        from_='+15856393761',
                        to='+918779292839'
                    )
                
                print(message.sid)
                speak("Call has been made sucessfully")
            
            elif "ip address" in self.query:
                ip = get('https://api.ipify.org').text
                speak(f"Your IP address is {ip}")

            elif "send message" in self.query:
                kit.sendwhatmsg("+918652172362","This is Testing Protocol Test 5",13,48)

            elif "increase the volume" in self.query:
                pyautogui.press("volumeup")
            
            elif "decrease the volume" in self.query:
                pyautogui.press("volumedown")

            elif 'set alarm' in self.query:
                speak("What time should I set the alarm.Please set it like 5:30 AM format")
                tt=self.takeCommand()
                tt=tt.replace("set alarm to","")
                tt=tt.upper()
                MyAlarm.alarm(tt)

            elif 'read pdf' in self.query:
                self.pdfreader()

            elif 'internet speed' in self.query:
                st = speedtest.Speedtest()
                dl = st.download()
                up = st.upload()
                speak(f"sir we have {dl} bit per second downloading speed and {up} bit per second uploading speed")
            
            elif "play song on youtube" in self.query:
                kit.playonyt("see you again")

            elif "tell me a joke" in self.query:
                joke = pyjokes.get_joke()
                speak(joke)

            elif 'take screenshot' in self.query:
                speak("sir,please tell me the name for this screenshot file")
                time.sleep(3)
                name=self.takeCommand().lower()
                speak("hold on a second sir")
                img=pyautogui.screenshot()
                img.save(f"{name}.png")
                speak("Task completed")

            elif 'swap the window' in self.query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")


            elif "open music" in self.query:
                music_dir = "C:/Users/admin/Desktop/Personal_folder/songs/Bones.mp3"
                #songs = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir))

            elif 'open mobile camera' in self.query:
                import urllib.request
                import cv2
                import numpy as np    
                URL="http://192.168.29.171:8080"
                while True:
                    img_arr=np.array(bytearray(urllib.request.urlopen(URL).read()),dtype=np.uint8)
                    img=cv2.imdecode(img_arr,-1)
                    cv2.imshow('IPWebcam',img)
                    q=cv2.waitKey(1)
                    if q==ord("q"):
                        break;
                cv2.destroyAllWindows()


            # exit loop
            elif 'close program' in self.query:
                
                speak("Have a good day sir")
                exit()

startExecution=MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie=QtGui.QMovie("C:/Users/admin/Desktop/python/jarvis/initializing.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()

        self.ui.movie=QtGui.QMovie("C:/Users/admin/Desktop/python/jarvis/tumblr_o7vs1zNO341runoqyo6_540.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()

        self.ui.movie=QtGui.QMovie("C:/Users/admin/Desktop/python/jarvis/05bd96100762b05b616fb2a6e5c223b4_w200.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()

        self.ui.movie=QtGui.QMovie("C:/Users/admin/Desktop/python/jarvis/4be66f1aea5e87a674461cff90ff51bc.gif")
        self.ui.label_4.setMovie(self.ui.movie)
        self.ui.movie.start()

        self.ui.movie=QtGui.QMovie("C:/Users/admin/Desktop/python/jarvis/Screen_C_Loop_v001.gif")
        self.ui.label_5.setMovie(self.ui.movie)
        self.ui.movie.start()

        self.ui.movie=QtGui.QMovie("C:/Users/admin/Desktop/python/jarvis/rotating.gif")
        self.ui.label_6.setMovie(self.ui.movie)
        self.ui.movie.start()

        self.ui.movie=QtGui.QMovie("C:/Users/admin/Desktop/python/jarvis/speaking2.gif")
        self.ui.label_7.setMovie(self.ui.movie)
        self.ui.movie.start()

        self.ui.movie=QtGui.QMovie("C:/Users/admin/Desktop/python/jarvis/listening2.gif")
        self.ui.label_8.setMovie(self.ui.movie)
        self.ui.movie.start()

        self.ui.movie=QtGui.QMovie("C:/Users/admin/Desktop/python/jarvis/loading.gif")
        self.ui.label_9.setMovie(self.ui.movie)
        self.ui.movie.start()

        self.ui.movie=QtGui.QMovie("C:/Users/admin/Desktop/python/jarvis/sleeping.gif")
        self.ui.label_10.setMovie(self.ui.movie)
        self.ui.movie.start()

        self.ui.movie=QtGui.QMovie("C:/Users/admin/Desktop/python/jarvis/f424b7131782573.619c1afdda994.gif")
        self.ui.label_11.setMovie(self.ui.movie)
        self.ui.movie.start()
        startExecution.start()

        self.ui.movie=QtGui.QMovie("C:/Users/admin/Desktop/python/jarvis/extra4.gif")
        self.ui.label_12.setMovie(self.ui.movie)
        self.ui.movie.start()
        startExecution.start()

        self.ui.movie=QtGui.QMovie("C:/Users/admin/Desktop/python/jarvis/extra1.gif")
        self.ui.label_13.setMovie(self.ui.movie)
        self.ui.movie.start()
        startExecution.start()

        
        self.ui.movie=QtGui.QMovie("C:/Users/admin/Desktop/python/jarvis/he-he.gif")
        self.ui.label_14.setMovie(self.ui.movie)
        self.ui.movie.start()
        startExecution.start()

        
        self.ui.movie=QtGui.QMovie("C:/Users/admin/Desktop/python/jarvis/Screen_I_Loop_prores_v001.gif")
        self.ui.label_15.setMovie(self.ui.movie)
        self.ui.movie.start()
        startExecution.start()

        self.ui.movie=QtGui.QMovie("C:/Users/admin/Desktop/python/jarvis/Owl_SW_Attack_Mode_Generic_Loop_v001.gif")
        self.ui.label_17.setMovie(self.ui.movie)
        self.ui.movie.start()
        startExecution.start()

        self.ui.movie=QtGui.QMovie("C:/Users/admin/Desktop/python/jarvis/Owl_SW_Flight_Mode_Generic_Loop_v001.gif")
        self.ui.label_18.setMovie(self.ui.movie)
        self.ui.movie.start()
        startExecution.start()

    def runAllMoviesDynamically(self,state):
        if state=="listening":
            self.ui.label_8.raise_()
            self.ui.label_7.hide()
            self.ui.label_9.hide()
            self.ui.label_10.hide()
            self.ui.label_8.show()
        elif state=="speaking":
            self.ui.label_7.raise_()
            self.ui.label_8.hide()
            self.ui.label_9.hide()
            self.ui.label_10.hide()
            self.ui.label_7.show()
        elif state=="Recognizing...":
            self.ui.label_9.raise_()
            self.ui.label_8.hide()
            self.ui.label_7.hide()
            self.ui.label_10.hide()
            self.ui.label_9.show()
        elif state=="sleeping":
            self.ui.label_10.raise_()
            self.ui.label_8.hide()
            self.ui.label_9.hide()
            self.ui.label_7.hide()
            self.ui.label_10.show()
        
             

app=QApplication(sys.argv)
jarvis=Main()
jarvis.show()
exit(app.exec_())
