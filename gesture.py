import cvzone
import mediapipe
import cv2  
from cvzone.HandTrackingModule import HandDetector
import webbrowser
import os
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pygame
import sys
import random


width, height = 1000, 720

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
gestureThreshold = 300
buttonPressed = False
buttonCounter = 0
buttonDelay = 30
annotations = [[]]
annotationNumber = -1
annotationStart = False

detector = HandDetector(detectionCon=0.8, maxHands=1)

def google_gesture():
    
    webbrowser.open_new_tab("http://www.google.com")


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(0, None)
minVol = volRange[0]
maxVol = volRange[1]


"""def playgame():
    
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

    myFont = pygame.font.SysFont('monospace',35)"""

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
    

    """while not game_over:
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                x=player_pos[0]
                y = player_pos[1]

                if event.key == pygame.K_LEFT:
                    if x>0:
                        x -= player_size
                elif event.key == pygame.K_RIGHT:
                    if x<WIDTH-player_size:
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

    return score"""


def paint_gesture():
    while True:

        success, img = cap.read()
        pre_current = "drawingpic.png"
        current = cv2.imread(pre_current)

        hands, img = detector.findHands(img)
        cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 5)

        if hands and buttonPressed is False:
            hand = hands[0]
            fingers = detector.fingersUp(hand)
            cx, cy = hand['center']
            lmList = hand['lmList']
            x2,y2 = lmList[8][0] , lmList[8][1]
        if fingers == [0,1,1,0,0]:
            
            cv2.circle(current,(x2,y2),12,(0,0,255),cv2.FILLED)


        if fingers == [0,1,0,0,0]:
            
            if annotationStart is False:
                annotationStart=True
                annotationNumber += 1
                annotations.append([])

            cv2.circle(current,(x2,y2),12,(0,0,255),cv2.FILLED)
            annotations[annotationNumber].append((x2,y2))

        else:
            annotationStart = False

    for i in range(len(annotations)):
        for j in range(len(annotations[i])): 
            if j!= 0 :
                cv2.line(current, annotations[i][j-1],annotations[i][j],(0,0,200),12)




while True:
    success, img = cap.read()
    #pre_current = "drawingpic.png"
    #current = cv2.imread(pre_current)

    hands, img = detector.findHands(img, flipType=False)
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 5)


    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        lmList = hand['lmList']
        
        if cy <= gestureThreshold:
            if len(lmList) != 0:
                x1,y1 = lmList[4][0] , lmList[4][1]
                x2,y2 = lmList[8][0] , lmList[8][1]
                cx_new , cy_new = (x1+x2)//2, (y1+y2)//2

                cv2.circle(img,(x1,y1),8,(255,0,255),cv2.FILLED)
                cv2.circle(img,(x2,y2),8,(255,0,255),cv2.FILLED)
                cv2.line(img,(x1,y1),(x2,y2),(255,0,255),5)
                cv2.circle(img,(cx_new,cy_new),8,(255,0,255),cv2.FILLED)

                length = math.hypot(x2-x1, y2-y1)

                vol = np.interp(length, [15,100], [minVol, maxVol])
                volume.SetMasterVolumeLevel(vol, None)
            

                if length < 50:
                    cv2.circle(img,(cx_new,cy_new),15,(0,255,0),cv2.FILLED)

            


        if cy <= gestureThreshold:
            if fingers == [1, 1, 1, 1, 1]:
                buttonPressed = True
                google_gesture()

        

        if cy <= gestureThreshold:
            if fingers == [0,1, 1, 1, 1]:
                buttonPressed = True

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
                

                
                
                while not game_over:
        

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            x=player_pos[0]
                            y = player_pos[1]

                            if event.key == pygame.K_LEFT:
                                if x>0:
                                    x -= player_size
                            elif event.key == pygame.K_RIGHT:
                                if x<WIDTH-player_size:
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

    
    
    

        


            

       
        """if fingers == [0,1,1,0,0]:
            
            cv2.circle(current,(x2,y2),12,(0,0,255),cv2.FILLED)


        if fingers == [0,1,0,0,0]:
            
            if annotationStart is False:
                annotationStart=True
                annotationNumber += 1
                annotations.append([])

            cv2.circle(current,(x2,y2),12,(0,0,255),cv2.FILLED)
            annotations[annotationNumber].append(indexFinger)

        else:
            annotationStart = False


    for i in range(len(annotations)):
        for j in range(len(annotations[i])): 
            if j!= 0 :
                cv2.line(current, annotations[i][j-1],annotations[i][j],(0,0,200),12)"""

    
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay :
            buttonCounter=0
            buttonPressed = False

    
    cv2.imshow('Image', img)
    #cv2.imshow('Pic',current)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break