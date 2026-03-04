import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

# pt.1: grab 4,500 frames from the camera
if os.path.exists('live_camera.avi'):
    print("live_camera.avi already exists, skipping capture...")
else:
    cap = cv2.VideoCapture() 
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    else:
        print("Camera opened successfully")

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('live_camera.avi', fourcc, 30.0, (640, 480)) # pt.2: save frames to live-camera.avi
    print("capturing 4,500 frames...")
    for i in range (4500):
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            if (i % 100 == 0): # print progress every 100 frames
                print(f"Captured {i} frames...")
        else:
            break

    cap.release()
    out.release()

# pt.3 & 4: open and replay the video
print("replaying video...")
cap = cv2.VideoCapture('live_camera.avi') 
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        cv2.imshow('replaying video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cv2.destroyAllWindows()

# pt.5: 1000th frame processing
cap.set(cv2.CAP_PROP_POS_FRAMES, 999) # set the position to the 1000th frame
ret, frame_1000 = cap.read()

if ret:
    # show frame and frame shape
    cv2.imshow('1000th frame', frame_1000)
    print(f"1000th frame shape: {frame_1000.shape}")

    # show B, G, R channels
    b, g, r = cv2.split(frame_1000)
    zeros = np.zeros_like(b)
    b = cv2.merge((b, zeros, zeros))
    g = cv2.merge((zeros, g, zeros))
    r = cv2.merge((zeros, zeros, r))
    
    cv2.imshow('Blue channel', b)
    cv2.imshow('Green channel', g)
    cv2.imshow('Red channel', r)
    
    # resize to 70% 
    resized_frame = cv2.resize(frame_1000, None, fx=0.7, fy=0.7)

    # convert to HSV
    hsv = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2HSV)

    # assigne 50% to V values
    h, s, v = cv2.split(hsv)
    v[:] = 128 # set V values to 50% (128 out of 255)
    modified_hsv = cv2.merge((h, s, v))
    
    modified_bgr = cv2.cvtColor(modified_hsv, cv2.COLOR_HSV2BGR) # convert processed image back to BGR
    filtered_image = cv2.GaussianBlur(modified_bgr, (7, 7), 0) # 7x7 Gaussian blur
    cv2.imshow('Filtered image', filtered_image) # show filtered image in new window
    cv2.imwrite('modified_img.jpg', filtered_image) # save filtered image as filtered_image.jpg

    print("\nPress 'q' to close windows...")
    while(1):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        
# S channel histogram
print("\nPress 'q' to close histograms...")
plt.figure()
plt.title("S channel histogram")
plt.hist(s.ravel(), bins=256, range=(0, 256))

# equalize histogram of S channel
equalized_s = cv2.equalizeHist(s)
equalized_hsv = cv2.merge((h, equalized_s, v))

plt.figure()
plt.title("Equalized S channel histogram")
plt.hist(equalized_s.ravel(), bins=256, range=(0, 256))
plt.show()

cv2.destroyAllWindows()