import cv2
import numpy as np

process = True
quitbutton = 27     #Esc

cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("No camera connected")
    exit(0)

while process:
    ret, screen = cam.read()
    display = screen.copy()
    cv2.imshow("Camera", display)

    if(0xFF & cv2.waitKey(1) == quitbutton):
        print("Esc is pressed")
        process = False

cv2.destroyAllWindows()