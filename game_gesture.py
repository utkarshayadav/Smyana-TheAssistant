import cvzone
import mediapipe
import cv2  
from cvzone.HandTrackingModule import HandDetector


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)


imgBackground = cv2.imread("resources/background.png")
imgRed = cv2.imread("resources/red.png",cv2.IMREAD_UNCHANGED)
imgBlue = cv2.imread("resources/blue.png",cv2.IMREAD_UNCHANGED)


detector = HandDetector(detectionCon=0.8, maxHands=2)


while True:
    _, img = cap.read()

    img = cv2.flip(img,1)

    hands,img = detector.findHands(img, flipType=False)

    img = cv2.addWeighted(img, 0.2,imgBackground,0.8,0)

    if hands:
        for hand in hands:
            if hand['type'] == 'Left':
                img = cvzone.overlayPNG(img,imgRed,[50,100])



    #cvzone.overlayPNG(img,imgRed,(100,200))
    cv2.imshow('Image',img)
    cv2.waitKey(1)