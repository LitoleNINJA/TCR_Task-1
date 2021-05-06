from flask import Flask, Response, render_template, jsonify
from ball_tracking import camera

app = Flask(__name__)

@app.route("/")
def index() :
    return render_template("index.html")

corner= "None"
percent_vol = "None"
def gen(camera) :
    while True :
        global corner
        global percent_vol
        frame, corner, percent_vol = camera.gen_frame()
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/video_feed")
def video_feed() :
    return Response(gen(camera()), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/send_data")
def send_data() :
    global percent_vol
    print(corner, percent_vol)
    if percent_vol == '0.0' :
        percent_vol = "None"
    percent_vol += " %"
    ball = "Not Present"
    if corner != "None" :
        ball = "Present" 
    return jsonify(ball=ball, corner=corner, area=percent_vol)

if __name__ == '__main__' :
    app.run(debug=True)