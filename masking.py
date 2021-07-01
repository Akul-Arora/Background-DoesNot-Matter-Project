import cv2
import time
import numpy as np

fourcc=cv2.VideoWriter_fourcc(*"XVID")
outputVideo=cv2.VideoWriter("output.avi", fourcc, 20.0, (640,480))
videocapture=cv2.VideoCapture(0)
time.sleep(2)
bg=0
for i in range(60):
    ret,bg=videocapture.read()
    
bg=np.flip(bg,axis=1)

while(videocapture.isOpened()):
    ret, img= videocapture.read()
    if not ret:
        break
    img= np.flip(img,axis=1)

    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    lower_black=np.array([0,0,0])
    upper_black=np.array([8,8,8])
    mask1=cv2.inRange(hsv,lower_black,upper_black)

    lower_black=np.array([32,32,32])
    upper_black=np.array([40,40,40])
    mask2=cv2.inRange(hsv,lower_black,upper_black)

    mask1=mask1+mask2

    mask1=cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3)),np.uint8)
    mask1=cv2.morphologyEx(mask1,cv2.MORPH_DILATE,np.ones((3,3)),np.uint8)
    mask2=cv2.bitwise_not(mask1)
    result1=cv2.bitwise_and(img,img,mask=mask2)
    result2=cv2.bitwise_and(bg,bg,mask=mask1)

    output=cv2.addWeighted(result1,1,result2,1,0)

    outputVideo.write(output)
    cv2.imshow("Image",output)
    cv2.waitKeyEx(1)

videocapture.release()
cv2.destroyAllWindows()