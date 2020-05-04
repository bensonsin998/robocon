import cv2
import imutils
import numpy as np

process = True
quitbutton = 27     #Esc

cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("No camera connected")
    exit(0)

while process:
    ret, screen = cam.read()
    screen = imutils.resize(screen, width = 800, height = 600)


    cv2.imshow("Camera", screen)

    if(0xFF & cv2.waitKey(1) == quitbutton):
        print("Esc is pressed")
        process = False

cv2.destroyAllWindows()