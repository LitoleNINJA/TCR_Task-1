# Color Based Ball Tracking with OpenCV-Python
### Detects and Tracks ball in the video feed based on colour.<br><br>

## Key Points :

1. Detect all the green balls in the image
2. Track the ball as it moves around in the video
3. HSV color space is used to detect the green ball. Hence we convert the input RGB image to HSV color space.
4. Draw an outline for the detected ball.
5. Finds the region in which the ball resides.
6. Displays the percentage of area covered by the ball.


## Requirements:

1. python-3.8.6
2. Flask==1.1.2
3. opencv-python==4.5.1.48
4. Jinja2==2.11.3


## Results :
The result is amazing. The ball is successfully detected. Also if the ball looses the frame, we catch it later when it comes in the frame.
