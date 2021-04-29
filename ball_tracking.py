# python code for ball tracking based on color 
import cv2
import numpy as np

img = cv2.VideoCapture(0)
height = img.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = img.get(cv2.CAP_PROP_FRAME_WIDTH)
green_u = (90,255,255)
green_l = (50,80,100)


while True :
    suc, frame = img.read()
    blur = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, green_l, green_u)
    cv2.erode(mask, None, iterations=2)
    cv2.dilate(mask, None, iterations=2)
    cv2.imshow("mask", mask)
    cnt, hier = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center  = None

    if len(cnt) > 0 :
        for c in cnt :
            approx = cv2.approxPolyDP(c, 0.01*cv2.arcLength(c, True), True)
            ((x,y), radius) = cv2.minEnclosingCircle(c)
            x = int(x)
            y = int(y)
            if len(approx) >=8 and radius > 50 :
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)
                if x < width//2 and y < height//2:
                    corner = "Top Left"
                elif x < width//2 and y > height//2 :
                    corner = "Bottom Left"
                elif x > width//2 and y < height//2 :
                    corner = "Top Right"
                else :
                    corner = "Bottom Right"
                cv2.putText(frame, corner, (x-50, y-50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1) 

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

img.release()
cv2.destroyAllWindows()