from flask import Flask, render_template, Response
import cv2
import socket

app = Flask(__name__)
#camera = cv2.VideoCapture(0)

HOST = "127.0.0.1"
PORT = 55555

def generate_frames():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    while True:
        frame = s.recv(102400)
        yield(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video")
def video():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(debug=True)

