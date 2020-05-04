import cv2
import numpy as np

cam = cv2.VideoCapture(0)

while True:
    screen = cam.read()
    cv2.imshow("Camera", screen)
    if cv2.waitKey(5) == 'q':
      break;

cv2.destroyAllWindows()