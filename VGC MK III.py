import cv2
import time
import HandTrackingModule as htm
from enum import Enum

from pynput import keyboard
from pynput.keyboard import Key, Controller
keyboard = Controller()

class Status(Enum):
    NONE = "NONE"
    MUTED = "MUTED"
    PLAY_PAUSE = "Play/Pause"
    PREVIOUS = "Previous"
    NEXT = "Next"



status = Status.NONE


def getPosition(ar):
    global status
    print(status)
    a = ""
    for i in ar:
        a += str(ar[i])

    if a == "00000":
        if status != Status.MUTED:
            keyboard.press(Key.media_volume_mute)
            keyboard.release(Key.media_volume_mute)
            status = Status.MUTED
            return ('MUTED')
    elif a == "01000":
        if status != Status.PLAY_PAUSE:
            keyboard.press(Key.media_play_pause)
            keyboard.release(Key.media_play_pause)
            status = Status.PLAY_PAUSE
            return ('PLAY/PAUSE')
    elif a == "01100":
        if status != Status.PREVIOUS:
            keyboard.press(Key.media_previous)
            keyboard.release(Key.media_previous)
            status = Status.PREVIOUS
            return ('PREVIOUS')
    elif a == "01111":
        if status != Status.NEXT:
            keyboard.press(Key.media_next)
            keyboard.release(Key.media_next)
            status = Status.NEXT
            return ('NEXT')
    elif a == "11111":
        if status != Status.NONE:

            status = Status.NONE
            return ('NONE')
    # if (a == "00000"):
    #     if status != Status.MUTED:
    #         status = Status.MUTED
    #         keyboard.press(Key.media_volume_mute)
    #         keyboard.release(Key.media_volume_mute)
    #         return ('MUTED')
    #
    # if (a == "01000"):
    #     if status != Status.PLAY_PAUSE:
    #         keyboard.press(Key.media_play_pause)
    #         keyboard.release(Key.media_play_pause)
    #         return ('Play/Pause')
    # success = True
    #
    # if (a == "01100"):
    #     if success == False:
    #         keyboard.press(Key.media_previous)
    #         keyboard.release(Key.media_previous)
    #         return ('Previous')
    # success = True
    # if (a == "01111"):
    #     if success == False:
    #         keyboard.press(Key.media_next)
    #         keyboard.release(Key.media_next)
    #         return ('Next')


wcam, hcam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)

pTime = 0

detector = htm.handDetector(detectionCon=0.6)

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=False)

    # print(lmList)

    lmId = [4, 8, 12, 16, 20]

    if (len(lmList) != 0):
        fingers = []

        if (lmList[lmId[0]][1] > lmList[lmId[0] - 1][1]):
            fingers.append(1)
        else:
            fingers.append(0)


        for id in range(1, len(lmId)):

            if (lmList[lmId[id]][2] < lmList[lmId[id] - 2][2]):
                fingers.append(1)

            else:
                fingers.append(0)

        cv2.rectangle(img, (10, 255), (380, 360), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(getPosition(fingers)), (0, 350), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 55), 10)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 3)
    cv2.imshow("image", img)
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break
