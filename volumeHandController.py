import cv2
import HandTrackingModule as htm
import time
import numpy as np
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap=cv2.VideoCapture(0)
ctime=0
ptime=0
detector=htm.handDetector()
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()
minVol=volRange[0]
maxVol=volRange[1]

while True:
    SUCCESS,img=cap.read()
    img=detector.findHands(img)
    lmlist,bbox=detector.findPosition(img,draw=False)
    if len(lmlist)!= 0:
        # print(lmlist[4],lmlist[8])
        
        length,img,lineInfo=detector.findDistance(4,8,img)
        # print(length)
        
        # handrange -- 21 to 150
        # volume range -- 65 to 0
        vol=np.interp(length,[5,150],[minVol,maxVol])
        volume.SetMasterVolumeLevel(vol, None)
        # print(vol)
        
        if length<21:
           cv2.circle(img,(lineInfo[4],lineInfo[5]),10,(0,225,0),cv2.FILLED) 
       
    ctime=time.time()   
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img,f"FPS: {str(int(fps))}",(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255),2)
    cv2.imshow("Tracking",img)
    cv2.waitKey(1)
        
    
    