import cv2
import numpy as np

cap=cv2.VideoCapture(0)
cap.set(3,800)
cap.set(4,600)
greenLower = (26, 75, 70)
greenUpper = (42, 255, 255)

def empty(a):
    pass

cv2.namedWindow('Parameters')
cv2.resizeWindow('Parameters',640,400)
cv2.createTrackbar('HUE MIN','Parameters',26,179,empty)
cv2.createTrackbar('HUE MAX','Parameters',46,179,empty)
cv2.createTrackbar('SAT MIN','Parameters',65,255,empty)
cv2.createTrackbar('SAT MAX','Parameters',255,255,empty)
cv2.createTrackbar('VAL MIN','Parameters',90,255,empty)
cv2.createTrackbar('VAL MAX','Parameters',255,255,empty)

cv2.createTrackbar('threshold1','Parameters',30,255,empty)
cv2.createTrackbar('threshold2','Parameters',255,255,empty)

'''def stackImages(scale,imgArray):
    rows=len(imgArray)
    cols=len(imgArray[0])
    rowsAvailable=isinstance(imgArray[0],list)
    width=imgArray[0][0].shape[1]
    height=imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(rows):
            for y in range(cols):
                if imgArray[x][y].shape[:2]==imgArray[0][0].shape[2]:
                    imgArray[x][y]=cv2.resize(imgArray[x][y],(0,0),None,scale,scale)
                else:
                    imgArray[x][y]=cv2.resize(imgArray[x][y],(imgArray[0][0].shape[1],imgArray[0][0].shape[0]),None,scale,scale)
                if len(imgArray[x][y].shape)==2:
                    imgArray[x][y]=cv2.cvtColor(imgArray[x][y],cv2.COLOR_GRAY2BGR)
        imageBlank=np.zeros((height,width,3),np.uint8)
        hor=[imageBlank]*rows
        hor_con=[imageBlank]*rows
        for x in range(rows):
            hor[x]=np.hstack(imgArray[x])
        ver=np.vstack(hor)
    else:
        for x in range(rows):
            if imgArray[x].shape[:2]==imgArray[0].shape[:2]:
                imgArray[x]=cv2.resize(imgArray[x],(0,0),None,scale,scale)
            else:
                imgArray[x]=cv2.resize(imgArray[x],(imgArray[0].shape[1],imgArray[0].shape[0]),None,scale,scale)
            if len(imgArray[x].shape)==2:
                imgArray[x]=cv2.cvtColor(imgArray[x],cv2.COLOR_GRAY2BGR)
        hor=np.hstack(imgArray)
        ver=hor
    return ver'''
def findcircle(img,imgContour):
    circles=cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1.2,10000,param1=threshold2,param2=threshold1)
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(imgContour, (int(x), int(y)), int(r),
                                (0, 255, 255), 2)

def getContours(img,imgContour):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        #center=None
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt,True), True)
        area=cv2.contourArea(cnt)
        if len(approx)>8 and area>1000:
            circles=cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 100, 50, 10)
            if circles is not None:
                #circles = np.round(circles[0, :]).astype("int")

                #cv2.drawContours(imgContour,cnt,-1,(255,0,255),3)
                    
                c = max(contours, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                cv2.circle(imgContour, (int(x), int(y)), int(radius),
                                (0, 255, 255), 2)

                #print(cv2.contourArea(cnt)*100/(320*480))
                
            

while True:
    success,img=cap.read()
    imgContour=img.copy()
    imgBlur=cv2.GaussianBlur(img,(7,7),1)
    imgGray=cv2.cvtColor(imgBlur,cv2.COLOR_BGR2GRAY)
    
    h_min=cv2.getTrackbarPos('HUE MIN','Parameters')
    h_max=cv2.getTrackbarPos('HUE MAX','Parameters')
    sat_min=cv2.getTrackbarPos('SAT MIN','Parameters')
    sat_max=cv2.getTrackbarPos('SAT MAX','Parameters')
    val_min=cv2.getTrackbarPos('VAL MIN','Parameters')
    val_max=cv2.getTrackbarPos('VAL MAX','Parameters')
    threshold1=cv2.getTrackbarPos('threshold1','Parameters')
    threshold2=cv2.getTrackbarPos('threshold2','Parameters')
    imgCanny=cv2.Canny(imgGray,threshold1,threshold2)
    kernel=np.ones((5,5))
    imgDil=cv2.dilate(imgCanny,kernel,iterations=1)
    imgDil=cv2.cvtColor(imgDil,cv2.COLOR_GRAY2BGR)
    lower=np.array([h_min,sat_min,val_min])
    upper=np.array([h_max,sat_max,val_max])
    hsv=cv2.cvtColor(imgBlur,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,lower,upper)
    result=cv2.bitwise_and(img,img,mask=mask)

    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    findcircle(mask,imgContour)
    #getContours(mask,imgContour)
    imgCanny=cv2.cvtColor(imgCanny,cv2.COLOR_GRAY2BGR)
    #imgStack=stackImages(0.8,([img,hsv],[mask,imgContour]))
    
    mask=cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
    hStack=np.hstack([imgCanny,imgContour])
    cv2.imshow("Result",hStack)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
