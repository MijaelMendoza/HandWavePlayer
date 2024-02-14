import cv2
import numpy as np
import HandTrackingModule as htm
import math
import time

from pynput.keyboard import Key, Controller

keyboard = Controller()


wCam, lCam = 720, 480


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, lCam)
pTime = 0

detection = htm.handDetector(detectionCon=0.75)

lastangle = None
lastlength = None
Exitcode = None

minAngle = 0
maxAngle = 180
angle = 0
angleB = 400
angleD = 0
minHand = 50
maxHand = 300
while True:
    success, img = cap.read()
    img = detection.findHands(img)
    lmList = detection.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (0, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)
        angle = np.interp(length, [minHand, maxHand], [minAngle, maxAngle])
        #print(angle)
        angleB = np.interp(length, [minHand, maxHand], [400, 150])
        angleD = np.interp(length, [minHand, maxHand], [0, 180])  #  0 - 180

        if lastlength:
            if length > lastlength:
                keyboard.press(Key.media_volume_up)
                keyboard.release(Key.media_volume_up)
                print("SUBIENDO VOLUMEN")
            elif length < lastlength:
                keyboard.press(Key.media_volume_down)
                keyboard.release(Key.media_volume_down)
                print("BAJANDO VOLUMEN")

        lastangle = angle
        lastlength = length

        # print(int(length), angle)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)
    if Exitcode:
        keyboard.press(Key.space)
        keyboard.release(Key.space)
        break
