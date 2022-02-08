import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import easyimap as e     #to read emails
import requests
import email
import traceback 
import cv2
import random
import imaplib
import random
from requests import get
import datetime
import smtplib
import pygame
import pyjokes
import random
import sys
from newsapi import NewsApiClient
import pycountry
import pyautogui #game

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

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('smyanatheassistant@gmail.com', 'smyana123.')
    server.sendmail('smyanatheassistant@gmail.com', to, content)
    server.close()
    
def takeCommand():

    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 2 #speed change
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query.lower()}\n")
    
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

#weather
def format_response(weather):
    try:
        name = weather['name']
        desc = weather['weather'][0]['description']
        temp = weather['main']['temp']
        final = 'City: %s \nConditions: %s \nTemperature (*F): %s'% (name,desc,temp)
    except:
        final = 'There was a problem retrieving that information'
    return final


def get_weather(city):
    weather_key = '995e215ca0a63c1c3a2ba841f1168bad'
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'APPID': weather_key, 'q':city, 'units': 'imperial'}
    response = requests.get(url, params=params)
    weather = response.json()

    return format_response(weather)


#news


#game
def playgame():

    pygame.init()

    WIDTH = 800
    HEIGHT = 600

    RED = (255,0,0)
    BLUE = (0,0,255)
    YELLOW = (255,255,0)
    BG_COLOR = (0,0,0)


    player_size = 50
    player_pos = [WIDTH/2,HEIGHT - 2*player_size]

    enemy_size = 50
    enemy_pos = [random.randint(0,WIDTH-enemy_size),0]

    SPEED = 10
    enemy_list = [enemy_pos]
    score =0 

    screen = pygame.display.set_mode((WIDTH,HEIGHT))

    game_over = False
    clock = pygame.time.Clock()

    myFont = pygame.font.SysFont('monospace',35)

    def set_level(score,SPEED):
        if score < 20:
            SPEED = 5
        elif score < 40:
            SPEED = 8
        elif score < 60:
            SPEED = 12
        else:
            SPEED = 15
        return SPEED
    def drop_enemies(enemy_list):
        delay = random.random()
        if len(enemy_list)<7 and delay < 0.2:
            x_pos = random.randint(0,WIDTH-enemy_size)
            y_pos = 0
            enemy_list.append([x_pos,y_pos])

    def draw_enemies(enemy_list):
        for enemy_pos in enemy_list:
            pygame.draw.rect(screen,BLUE,(enemy_pos[0],enemy_pos[1],enemy_size,enemy_size))

    def update_enemy_positions(enemy_list,score):
        for idx,enemy_pos in enumerate(enemy_list):
            if enemy_pos[1]>=0 and enemy_pos[1]< HEIGHT:
                enemy_pos[1] += SPEED
            else:
                enemy_list.pop(idx)
                score += 1
        return score

    def collision_check(enemy_list,player_pos):
        for enemy_pos in enemy_list:
            if detect_collision(enemy_pos, player_pos):
                return True
        return False


    def detect_collision(player_pos, enemy_pos):
        p_x = player_pos[0]
        p_y = player_pos[1]

        e_x = enemy_pos[0]
        e_y = enemy_pos[1]

        if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
            if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)): 
                return True
        return False
    

    while not game_over:
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.USEREVENT:
                x=player_pos[0]
                y = player_pos[1]
                lr = takeCommand().lower()
                
                if 'left' in lr:
                    if x>0:
                        pyautogui.press('left')
                        x -= player_size
                elif 'right' in lr:
                    if x<WIDTH-player_size:
                        pyautogui.press("right")
                        x += player_size
                player_pos = [x,y]

        screen.fill(BG_COLOR)

    
    
    

        drop_enemies(enemy_list)
        score = update_enemy_positions(enemy_list,score)
        SPEED = set_level(score,SPEED)

        text = "Score:" + str(score)
        label = myFont.render(text,1,YELLOW)
        screen.blit(label,(WIDTH-200, HEIGHT-40))

        if collision_check(enemy_list,player_pos):
            game_over = True
            break
        draw_enemies(enemy_list)

        pygame.draw.rect(screen,RED,(player_pos[0],player_pos[1],player_size,player_size))
    

        clock.tick(30)

        pygame.display.update()

    return score

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
        
        if 'game' in query:
            speak("Starting a fun game for you")
            again = True
            query = query.replace("game","")
            while again:
                results = playgame()
                print("Well played. Your score is"+ str(results))
                speak("Well played. Your score is"+ str(results))
                print("Do you want to play again")
                speak("Do you want to play again")
                answer = takeCommand().lower()
                if 'no' in answer:
                    again = False
                    sys.exit()



        #weather
        elif 'weather' in query:
            speak("Which city's weather report you wanna know")
            query = query.replace("weather","")
            city = takeCommand().lower()
            
            q=get_weather(city)
            speak("Checking "+city+" weather report")
            
            print(q)
            speak(q)
        
        #youtube
        elif 'open youtube' in query:
            print("Opening youtube...")
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"))
            webbrowser.get('chrome').open("youtube.com")

        #google
        elif 'open google' in query:
            print("Opening google...")
            speak("What do you want to search?")
            cm = takeCommand().lower()
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"))
            webbrowser.get('chrome').open(f"https://www.google.com/search?q={cm}")
        #jokes
        elif 'joke' in query:
            joke = pyjokes.get_joke()
            speak(joke)
            print(joke)

        #time
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M")
            print(f"The time is {strTime}")
            speak(f"The time is {strTime}")

        #vscode
        elif 'open code' in query:
            codePath = "C:\\Users\\utkar\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"  #system dependent
            print("Opening vscode...") 
            os.startfile(codePath)

        #cmd
        elif 'open cmd' in query or 'open command prompt' in query:
            os.system("start cmd")

        #Camera
        elif 'open camera' in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(20)
                if k == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()

        #music
        elif 'play music' in query:
            music_dir = "C:\\Users\\utkar\\Music"
            songs = os.listdir(music_dir)
            while 1:
                rd = random.choice(songs)
                if rd.endswith('.mp3'):
                    os.startfile(os.path.join(music_dir, rd))
                    break;

        #ip address
        elif 'ip address' in query:
            ip = get('https://api.ipify.org').text       #uses get function from request module
            print(ip)
            speak(f"Your IP address is {ip}")

        #send email
        elif "send email" in query:
            try:
                speak("What should I say?")
                content = takeCommand().lower()
                to = "roxutkarsha@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
                
            except Exception as e:
                print(e)
            
        #read email
        elif "read email" in query:
            server = e.connect("imap.gmail.com", "smyanatheassistant@gmail.com", "smyana123.")
            server.listids()

            speak("Top 3 emails are from")
            speak(server.mail(server.listids()[0]).from_addr)
            speak(server.mail(server.listids()[1]).from_addr)
            speak(server.mail(server.listids()[2]).from_addr)
            speak("Which email should I read, first, second or third")

            number = takeCommand().lower()

            if "first" in number or "1" in number:
                speak("The subject of the email is")
                speak(server.mail(server.listids()[0]).title)
                speak("The body of te email is")
                speak(server.mail(server.listids()[0]).body)

            if "second" in number or "2" in number:
                speak("The subject of the email is")
                speak(server.mail(server.listids()[1]).title)
                speak("The body of te email is")
                speak(server.mail(server.listids()[1]).body)

            if "third" in number or "3" in number:
                speak("The subject of te email is")
                speak(server.mail(server.listids()[2]).title)
                speak("The body of te email is")
                speak(server.mail(server.listids()[2]).body)
        
        elif "news" in query:
            # you have to get your api key from newapi.com and then paste it below
            newsapi = NewsApiClient(api_key='e87e1af4b58449dba9338a3cb5459f2c')
            speak("Which country's news do you want to know")
            input_country = takeCommand().lower()
            input_countries = [f'{input_country.strip()}']
            countries = {}

        # iterate over all the countries in
        # the world using pycountry module
            for country in pycountry.countries:
 
        # and store the unique code of each country
        # in the dictionary along with it's full name
                countries[country.name] = country.alpha_2
            # now we will check that the entered country name is
            # valid or invalid using the unique code
            codes = [countries.get(country.title(), 'Unknown code') for country in input_countries]

        # now we have to display all the categories from which user will
        # decide and enter the name of that category
            speak("Which category are you interested in? 1 Business 2 Entertainment 3 General 4 Health 5 Science 6 Technology")
            option = takeCommand().lower()
 
        # now we will fetch the new according to the choice of the user
            top_headlines = newsapi.get_top_headlines(
 
            # getting top headlines from all the news channels
                category=f'{option.lower()}', language='en', country=f'{codes[0].lower()}')
            
        # fetch the top news inder that category
            Headlines = top_headlines['articles']
 
        # now we will display the that news with a good readability for user
            if Headlines:
                c = 0
                for articles in Headlines:
                    b = articles['title'][::-1].index("-")
                    if c > 4:
                        break
                    if "news" in (articles['title'][-b+1:]).lower():
                        speak(f"{articles['title'][-b+1:]}: {articles['title'][:-b-2]}.")
                        print
                        (f"{articles['title'][-b+1:]}: {articles['title'][:-b-2]}.")
                        c = c + 1
                    else:
                        speak(f"{articles['title'][-b+1:]} News: {articles['title'][:-b-2]}.")
                        print(f"{articles['title'][-b+1:]} News: {articles['title'][:-b-2]}.")
                        c = c + 1
                        
            else:
                speak("Sorry no articles found for {input_country} Something Wrong")
        #print(f"Sorry no articles found for {input_country}, Something Wrong!!!")
            speak("Do you want to search again?")
            option = takeCommand().lower()
            if option == 'yes':
                continue
            else:
                exit()
 

 
            
        #email
        # elif "email" in query:
        #     ORG_EMAIL = "@gmail.com" 
        #     FROM_EMAIL = "smyanatheassistant" + ORG_EMAIL 
        #     FROM_PWD = "smyana123." 
        #     SMTP_SERVER = "imap.gmail.com" 
        #     SMTP_PORT = 993
        #     def read_email_from_gmail():
        #         try:
        #             mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        #             mail.login(FROM_EMAIL,FROM_PWD)
        #             webbrowser.open("https://mail.google.com//mail//u//0//?ogbl#inbox")
        #             """mail.select('inbox')

        #             data = mail.search(None, 'ALL')
        #             mail_ids = data[1]
        #             id_list = mail_ids[0].split()   
        #             first_email_id = int(id_list[0])
        #             latest_email_id = int(id_list[-1])

        #             for i in range(latest_email_id,first_email_id, -1):
        #                 data = mail.fetch(str(i), '(RFC822)' )
        #                 for response_part in data:
        #                     arr = response_part[0]
        #                     if isinstance(arr, tuple):
        #                         msg = email.message_from_string(str(arr[1],'utf-8'))
        #                         email_subject = msg['subject']
        #                         email_from = msg['from']
        #                         print('From : ' + email_from + '\n')
        #                         print('Subject : ' + email_subject + '\n')"""

        #         except Exception as e:
        #             #traceback.print_exc() 
        #             print(str(e))


        #    read_email_from_gmail()





            
        







        








            
        







        







            
        

            
        



















            
        









            
        






