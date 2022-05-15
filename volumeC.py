import cv2
import time
import numpy as np

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)

while 