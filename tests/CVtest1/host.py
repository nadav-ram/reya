import socket
import cv2
from cv2 import add

HOST = "127.0.0.1"
PORT = 55555

camera = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier()
face_cascade.load(cv2.samples.findFile("static/haarcascade_frontalface_alt.xml"))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()

if conn:
    
    print("Connected to: " + str(addr))
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = cv2.flip(frame, 1)
            grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #grayscale = cv2.equalizeHist(grayscale)
            faces = face_cascade.detectMultiScale(grayscale)
            
            for (x, y, w, h) in faces:
                center = [x + w//2, y + h//2]
                cv2.putText(frame, "X: " + str(center[0]) + "Y: " + str(center[1]), (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 4)
                frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 165, 255), 2)                

            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            conn.send(frame)