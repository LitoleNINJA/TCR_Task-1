import cv2
import numpy as np

class camera(object) :
    def __init__(self) :
        self.img = cv2.VideoCapture(0)

    def __del__(self) :
        self.img.release()
        cv2.destroyAllWindows()

    def gen_frame(self) :
        height = self.img.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = self.img.get(cv2.CAP_PROP_FRAME_WIDTH)
        green_u = (75,255,255)
        green_l = (40,60,130)
        suc, frame = self.img.read()
        blur = cv2.GaussianBlur(frame, (7, 7), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, green_l, green_u)
        cv2.erode(mask, None, iterations=2)
        cv2.dilate(mask, None, iterations=2)
        cnt, hier = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        corner = "None"
        percent_vol = "None"

        if len(cnt) > 0 :
            for c in cnt :
                approx = cv2.approxPolyDP(c, 0.01*cv2.arcLength(c, True), True)
                ((x,y), radius) = cv2.minEnclosingCircle(c)
                radius = int(radius)
                x = int(x)
                y = int(y)
                percent_vol = ((3.14159*radius*radius) * 100 )/(height*width)
                percent_vol = round(percent_vol, 2)
                percent_vol = str(percent_vol)
                if len(approx) >=8 and radius > 50 :
                    cv2.circle(frame, (x, y), radius, (0, 0, 255), 2)
                    if x < width//2 and y < height//2:
                        corner = "Top Left"
                    elif x < width//2 and y > height//2 :
                        corner = "Bottom Left"
                    elif x > width//2 and y < height//2 :
                        corner = "Top Right"
                    else :
                        corner = "Bottom Right"

        height = int(height)
        width = int(width)
        blank_image = np.zeros((height, 400, 3), np.uint8)
        blank_image[:] = (41,36,33)
        cv2.putText(blank_image, "Region = "+corner, (25, 150), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)
        
        if percent_vol == "0.0" :
            percent_vol = "None"
        cv2.putText(blank_image, "Area = "+percent_vol+" %", (25, 250), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        join = cv2.hconcat([frame, blank_image])
        
        _, jpeg = cv2.imencode(".jpg", join)
        return jpeg.tobytes()