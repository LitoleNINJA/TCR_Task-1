import cv2

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
                if len(approx) >= 8 and radius > 50 :
                    cv2.circle(frame, (x, y), radius, (0, 0, 255), 2)
                    if x < width//2 and y < height//2:
                        corner = "Top Left"
                    elif x < width//2 and y > height//2 :
                        corner = "Bottom Left"
                    elif x > width//2 and y < height//2 :
                        corner = "Top Right"
                    else :
                        corner = "Bottom Right" 
        
        _, jpeg = cv2.imencode(".jpg", frame)
        return jpeg.tobytes(), corner, percent_vol