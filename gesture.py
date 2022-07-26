import cvzone
import mediapipe
import cv2  
from cvzone.HandTrackingModule import HandDetector
import os
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import sys
import random as rnd
import pyautogui



width, height = 1000, 720
ww, hh = list(pyautogui.size())[0], list(pyautogui.size())[1]

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
gestureThreshold = 300
buttonPressed = False
buttonCounter = 0
buttonDelay = 30


detector = HandDetector(detectionCon=0.8, maxHands=1)



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(0, None)
minVol = volRange[0]
maxVol = volRange[1]


    



while True:
    success, img = cap.read()  
    hands, img = detector.findHands(img, flipType=False)
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 5)


    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        lmList = hand['lmList']
        x2,y2 = lmList[8][0] , lmList[8][1]

        xVal = int(np.interp(lmList[8][0],[width//5,width//3],[0,width]))
        yVal = int(np.interp(lmList[8][1],[150,height//3],[0,height]))
        indexFinger = xVal,yVal
        
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