from flask import Flask
from flask import Response
from flask import render_template
from ball_tracking import camera

app = Flask(__name__)

@app.route("/")
def index() :
    return render_template("index.html")

def gen(camera) :
    while True :
        frame = camera.gen_frame()
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/video_feed")
def video_feed() :
    return Response(gen(camera()), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__' :
    app.run(debug=True)