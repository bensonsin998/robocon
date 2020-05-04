import cv2
import imutils
import numpy as np

cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("No camera connected")
    exit(0)
process = True
quitbutton = 27     #Esc

while process:
    ret, frame = cam.read()

    frame = imutils.resize(frame, width = 800, height = 600)


    cv2.imshow("Camera", frame)

    if(0xFF & cv2.waitKey(1) == quitbutton):
        print("Esc is pressed")
        process = False

cv2.destroyAllWindows()