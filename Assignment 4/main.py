import numpy as np
import matplotlib.pyplot as plt
import cv2

cap = cv2.VideoCapture(2) 

if not cap.isOpened():
    print("Cannot open camera")
    exit()
else:
    print("Camera opened successfully")

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('live_camera.avi', fourcc, 30.0, (640, 480)) # pt.2: save frames to live-camera.avi

# pt.1: grab 4,500 frames from the camera
print("capturing 4,500 frames...")
for i in range (4500):
    ret, frame = cap.read()
    if ret:
        out.write(frame)
    else:
        break

cap.release()
out.release()

# pt.3 & 4: open and replay the video
cap = cv2.VideoCapture('live_camera.avi') 
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        cv2.imshow('replaying video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break