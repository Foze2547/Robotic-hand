import cv2
import time
import os
import HandTrackingModule as htm

wCam, hCam = 640, 480

cap = cv2.VideoCapture(1)

cap.set(3, wCam)
cap.set(4, hCam)

# Step 2 check image from folder
folderPath = "fingerImages"
myList = os.listdir(folderPath)
myList.sort()
# print(myList)

# check count of image
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
    # print(f'{folderPath}/{imPath}')

# print(len(overlayList))

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

    if len(lmList) != 0:

        fingers = []

        # for thump finger left hand
        # check thump that left side or right side
        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # for 4 finger
        # check finger open
        # for check data in list compare
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # notice : thump finger can't bring to below than index check low, so will another solution
        # print(fingers)

        # check index finger open
        # if point 8 of hand landmark below than point 6
        # if lmList[8][2] < lmList[6][2]:
        #     print("index finger open")
        # else:
        #    print("index finger close")

        # have sum count finger opened
        totalFingers = fingers.count(1)
        # print(totalFingers)

        # get size from image
        h, w, c = overlayList[0].shape

        # set overlay image to video
        img[0:h, 0:w] = overlayList[totalFingers]

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
