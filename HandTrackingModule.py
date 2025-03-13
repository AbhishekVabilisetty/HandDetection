import cv2
import mediapipe as mp
import time
import math
 
class handDetector():
    def __init__(self,mode=False,maxHands=2,modelCom=1,detectioncon=0.5,trackingcon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.modelcom=modelCom
        self.detectioncon=detectioncon
        self.trackingcon=trackingcon

        self.mphands=mp.solutions.hands
        self.hands = self.mphands.Hands(self.mode,self.maxHands,self.modelcom,self.detectioncon,self.trackingcon)
        self.mpdraw=mp.solutions.drawing_utils

    def findHands(self,img,draw=True):

        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)
    
        if(self.results.multi_hand_landmarks):
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(img,handlms,self.mphands.HAND_CONNECTIONS)
        return img   
    
    def findPosition(self,img,handNo=0,draw=True): 
        xList=[]
        yList=[]
        bbox=[]
        self.lmlist=[]
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand.landmark):
                        # print(id,lm)
                        h,w,c=img.shape
                        cx,cy=int(lm.x*w),int(lm.y*h)
                        # print(id,cx,cy)
                        xList.append(cx)
                        yList.append(cy)
                        self.lmlist.append([id,cx,cy])
                        # if draw:
                        #     cv2.circle(img,(cx,cy),10,(225,0,225),cv2.FILLED)
            xmin,xmax=min(xList),max(xList)
            ymin,ymax=min(yList),max(yList)
            bbox=xmin,ymin,xmax,ymax
            if draw:
                cv2.rectangle(img,(bbox[0]-20,bbox[1]-20),(bbox[2]+20,bbox[3]+20),(0,225,0),2)
        return self.lmlist,bbox
    
    def findDistance(self,p1,p2,img,draw=True):
        
        x1,y1=self.lmlist[p1][1],self.lmlist[p1][2]
        x2,y2=self.lmlist[p2][1],self.lmlist[p2][2]
        mid1,mid2=(x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(x1,y1),10,(255,0,0),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(255,0,0),cv2.FILLED)
        if draw :
            cv2.line(img,(x1,y1),(x2,y2),(255,0,225),3)
            cv2.circle(img,(mid1,mid2),10,(255,0,225),cv2.FILLED)
        length=math.hypot(x2-x1,y2-y1)
        return length,img,[x1,y1,x2,y2,mid1,mid2]
    

def main():
    ptime=0
    ctime=0 
    capture=cv2.VideoCapture(0)
    detector=handDetector()
    while True:
        SUCCESS,img=capture.read()
        img=detector.findHands(img)
        lmlist=detector.findPosition(img)
        if(len(lmlist)!=0):
            print(lmlist[4])
        ctime=time.time()
        fps=1/(ctime-ptime)
        ptime=ctime
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,255),2)
        cv2.imshow("Image",img)
        cv2.waitKey(1)
        


if __name__=="__main__":
    main()