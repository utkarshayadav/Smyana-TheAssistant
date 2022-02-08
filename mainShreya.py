import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import email
import traceback 

import imaplib


import datetime

engine = pyttsx3.init('sapi5')                       #for text to speech function
voices = engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voice',voices[1].id)             #sets the female voice 

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)                #will return hour from 0 to 24 (due to int typecasting)
    if hour>= 0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("I am Smyana. How may I help you?")
    
def takeCommand():

    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query





if __name__=="__main__":
    wishMe()
    
    while 1:
        query = takeCommand().lower()

        #wikipedia
        if 'wikipedia' in query:
            speak("Searching wikipedia")
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences=3)
            speak("According to wikipedia")
            print(results)
            speak(results)
        
        #youtube
        elif 'open youtube' in query:
            print("Opening youtube...")
            webbrowser.open("youtube.com")

        #google
        elif 'open google' in query:
            print("Opening google...")
            webbrowser.open("google.com")

        #music

        #time
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M")
            print(f"The time is {strTime}")
            speak(f"The time is {strTime}")

        #vscode
        elif 'open code' in query:
            codePath = "C:\\Users\\Shreya\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"  #system dependent
            print("Opening vscode...") 
            os.startfile(codePath)

        #cmd
        #elif 'open command prompt' in query:
        #    os.system("start cmd")

        #email
        elif "email" in query:
            ORG_EMAIL = "@gmail.com" 
            FROM_EMAIL = "smyanatheassistant" + ORG_EMAIL 
            FROM_PWD = "smyana123." 
            SMTP_SERVER = "imap.gmail.com" 
            SMTP_PORT = 993
            def read_email_from_gmail():
                try:
                    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
                    mail.login(FROM_EMAIL,FROM_PWD)
                    webbrowser.open("https://mail.google.com//mail//u//0//?ogbl#inbox")
                    """mail.select('inbox')

                    data = mail.search(None, 'ALL')
                    mail_ids = data[1]
                    id_list = mail_ids[0].split()   
                    first_email_id = int(id_list[0])
                    latest_email_id = int(id_list[-1])

                    for i in range(latest_email_id,first_email_id, -1):
                        data = mail.fetch(str(i), '(RFC822)' )
                        for response_part in data:
                            arr = response_part[0]
                            if isinstance(arr, tuple):
                                msg = email.message_from_string(str(arr[1],'utf-8'))
                                email_subject = msg['subject']
                                email_from = msg['from']
                                print('From : ' + email_from + '\n')
                                print('Subject : ' + email_subject + '\n')"""

                except Exception as e:
                    #traceback.print_exc() 
                    print(str(e))


            read_email_from_gmail()


            
        







        








            
        







        







            
        

            
        



















            
        









            
        






