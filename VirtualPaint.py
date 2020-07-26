import cv2
import numpy as np

cap=cv2.VideoCapture(0)
cap.set(3,640) #width
cap.set(4,480) #height
#cap.set(10,110) #brightness

myColors=[[2,35,230,21,255,255],[19,92,115,31,159,229],[95,83,0,99,255,255]]

myPoints=[]                                 #  [ x , y , colorID ]

mycolorValues=[(0,128,255),(121,255,195),(255,0,0)]

def getContours(img):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area=cv2.contourArea(cnt)
        #print(area)
        if area>200 :                                                                                    #To Minimize noise
            cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)
            peri=cv2.arcLength(cnt,True)
            print(peri)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)                                                 #Approx number of corner points                
            print(len(approx))
            objCorner=len(approx)
            x,y,w,h=cv2.boundingRect(approx)
    return x+w,y+h

def drawCanvas(myPoints,mycolorValues):
    for points in myPoints:
        cv2.circle(imgResult,(points[0],points[1]),10,mycolorValues[points[2]],cv2.FILLED)



def findColor(img,myColors,mycolorValues):
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count=0
    newPoints=[]
    for color in myColors:
        lower=np.array(color[0:3])
        upper=np.array(color[3:6])
        mask=cv2.inRange(imgHSV,lower,upper)
        x,y=getContours(mask)
        cv2.circle(imgResult,(x,y),10,mycolorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
             newPoints.append([x,y,count])
        count+=1
        cv2.imshow(str(color[0]),mask)
    return newPoints


while True:
    success,imgf=cap.read()
    img=cv2.flip(imgf,1)
    imgResult=img.copy()
    newPoints=findColor(img,myColors,mycolorValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawCanvas(myPoints,mycolorValues)

    cv2.imshow("Video",imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break