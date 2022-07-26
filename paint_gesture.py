import cvzone
import mediapipe
import cv2  
from cvzone.HandTrackingModule import HandDetector
import os
import numpy as np


brushThickness = 15


folderPath = 'Header'
myList = os.listdir(folderPath)
overlayList = []

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
header = overlayList[1]
drawColor = (0,0,255)


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)


detector = HandDetector(detectionCon=0.8, maxHands=1)
xp,yp = 0,0
imgCanvas = np.zeros((720,1280,3), np.uint8)



while True:
    success, img = cap.read()
    
    img = cv2.flip(img,1)

    hands,img = detector.findHands(img)
    if hands:
        hand = hands[0]
        lmList = hand['lmList']
        if len(lmList) != 0:
            
            x1,y1 = lmList[8][0] , lmList[8][1]
            x2,y2 = lmList[12][0] , lmList[12][1]
    
    

    
    
     
        fingers = detector.fingersUp(hand)
        if fingers[1] and fingers[2]:
            xp,yp = 0,0
        
            if y1 < 170:
                if 250<x1<360:
                    header= overlayList[1]
                    drawColor = (0,0,255)
                
                
                elif 450<x1<680:
                    header= overlayList[2]
                    drawColor = (0,255,0)
                elif 750<x1<1000:
                    header= overlayList[3]
                    drawColor = (0,255,255)
            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)

        
    

        if fingers[1] and fingers[2]==False:
            cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
            if xp==0 and yp==0:
                xp,yp = x1,y1

            cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
            cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)
            xp,yp = x1,y1
    imgGray = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _,imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgCanvas)
        



    img[0:170,0:1204] = header
    #img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow('Image', img)
    cv2.imshow('Canvas', imgCanvas)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break