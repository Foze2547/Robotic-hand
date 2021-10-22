import cv2
import time
import os
import HandTrackingModule as htm

wCam, hCam = 640, 480

cap = cv2.VideoCapture(1)

cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0

# create object class detect
detector = htm.handDetector(detectionCon=0.5)

# index id of hand landmark
tipIds = [4, 8, 12, 16, 20]

while True:

    # Step 1 check webcam
    success, img = cap.read()

    # class method findhand
    img = detector.findHands(img)

    lmList = detector.findPosition(img, draw=False)
    # print(lmList)
    sayHiPattern = [4, 8, 12, 16, 20]

    fightPattern = [8, 12]

    carabaoPattern = [4, 20]

    devilPattern = [8, 20]

    lovePattern = [4, 8, 20]

    gratePattern = [4]

    promisePattern = [20]

    if len(lmList) != 0:

        fingers = []

        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            if tipIds[0] not in fingers:
                fingers.append(tipIds[0])

        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                if tipIds[id] not in fingers:
                    fingers.append(tipIds[id])
                    print(tipIds[id])

        fingers.sort()

        if fingers == sayHiPattern:
            cv2.putText(img, str("Hello everybody"), (4, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)
        elif fingers == carabaoPattern:
            cv2.putText(img, str("Hi there"), (4, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)
        elif fingers == fightPattern:
            cv2.putText(img, str("Fi to"), (4, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)
        elif fingers == devilPattern:
            cv2.putText(img, str("Hello Rock&Roll"), (4, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)
        elif fingers == lovePattern:
            cv2.putText(img, str("Lovely"), (4, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)
        elif fingers == gratePattern:
            cv2.putText(img, str("Very Good"), (4, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)
        elif fingers == promisePattern:
            cv2.putText(img, str("Promise Me"), (4, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
