from flask import Flask
from flask import Response
from flask import redirect
from flask import render_template
from vision import camera

app = Flask(__name__)

@app.route("/")
def index() :
    return render_template("index.html")

cor = None
percent = None
def gen(camera) :
    while True :
        global cor
        global percent
        frame, cor, percent = camera.gen_frame()
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/video_feed")
def video_feed() :
    return Response(gen(camera()), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/data")
def data() :
    str(percent)
    return render_template("info.html", cor=cor, percent=percent)

if __name__ == '__main__' :
    app.run(debug = True)