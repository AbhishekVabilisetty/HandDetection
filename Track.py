import cv2

import HandTrackingModule as h
import time


ptime=0
ctime=0 
capture=cv2.VideoCapture(0)
detector=h.handDetector()
while True:
    SUCCESS,img=capture.read()
    img=detector.findHands(img)
    lmlist=detector.findPosition(img,draw=False)
    if(len(lmlist)!=0):
        print(lmlist[4])
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,255),2)
    cv2.imshow("Tracking",img)
    cv2.waitKey(1)