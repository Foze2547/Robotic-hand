import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import osascript

#######################
wCam, hCam = 400, 400
#######################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# previous time
pTime = 0

# object from handDetector class module
# detectionCon is
# min_detection_confidence: Minimum confidence value ([0.0, 1.0]) for hand
# detection to be considered successful. See details in
# https://solutions.mediapipe.dev/hands#min_detection_confidence.

detector = htm.handDetector(detectionCon=0.7)

# initial volume
vol = 0
volBar = 400
volPer = 0

while True:

    # read image from webcam
    success, img = cap.read()

    # detector hand from video image(2)
    detector.findHands(img)

    # find position of image
    lmList = detector.findPosition(img, draw=False)

    # printed log when detect hand in position 4, 8 image(3_1, 3_2)
    if len(lmList) != 0:
        # print(lmList[4],lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2] # position of thumb finger
        x2, y2 = lmList[8][1], lmList[8][2] # position of index finger

        # add circle to position of landmark image(4)
        cv2.circle(img, (x1, y1), 15, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)

        # center line of between 2 finger
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # add line between 2 finger image (5)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3)

        # add center point between 2 finger image 6
        cv2.circle(img, (cx, cy), 15,  (255,0,255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1) # calculator length between 2 finger
        # print(length) # if wide more better narrow of between 2 finger

        # Hand range 25 - 280
        # Volume Range 0 - 100
        vol = np.interp(length, [25, 280], [0, 100]) # it can change follow your hand
        volBar = np.interp(length, [25, 280], [400, 100])
        volPer = np.interp(length, [25, 280], [0,100])
        # print(vol)
        print(volBar)

        # https://dev.to/kojikanao/control-mac-sound-volume-by-python-h4g
        # didn't forget install at preference it's name osascript for make script controller volume on your mac
        osascript.osascript("set volume output volume {}".format(vol))

        # if length less than 50 it will be chaged color image (7)
        if length < 50:
            cv2.circle(img, (cx,cy),15, (0,255,255), cv2.FILLED)

    # outline Volume
    cv2.rectangle(img, (50,100), (85,400), (0,255,0), 3)
    # Bar Volume
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)

    if volPer == 0:
        # Text Percent Volume turn off
        cv2.putText(img, f'{int(volPer)} %', (40, 500), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0, 255), 3)
    else:
        # Text Percent Volume turn on
        cv2.putText(img, f'{int(volPer)} %', (40, 500), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 3)

    # watch framerate video
    cTime = time.time() # current time
    fps = 1/(cTime-pTime) # framerate video
    pTime = cTime

    # display text framerate image(1)
    cv2.putText(img, f'FPS: {int(fps)}', (40,70), cv2.FONT_HERSHEY_COMPLEX, 2, (255,0,255),3)

    # display video
    cv2.imshow("img",img)
    cv2.waitKey(1)

