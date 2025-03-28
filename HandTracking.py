import cv2
import mediapipe as mp
import time
 
capture=cv2.VideoCapture(0)
mphands=mp.solutions.hands
hands=mphands.Hands()
mpdraw=mp.solutions.drawing_utils

ptime=0
ctime=0

while True:
    SUCCESS,img=capture.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    
    if(results.multi_hand_landmarks):
        for handlms in results.multi_hand_landmarks:
            for id,lm in enumerate(handlms.landmark):
                # print(id,lm)
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                print(id,cx,cy)
                if(id == 0):
                    cv2.circle(img,(cx,cy),15,(225,0,225),cv2.FILLED)
                
            mpdraw.draw_landmarks(img,handlms,mphands.HAND_CONNECTIONS)
    
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,255),2)
    cv2.imshow("Image",img)
    cv2.waitKey(1)
