import cv2
import numpy as np

cam = cv2.VideoCapture(0)

while True:
    ret, img = cam.read()
    vis = img.copy()
    cv2.imshow("Cmaera", vis)
    if cv2.waitKey(5) == 27:
      break;

cv2.destroyAllWindows()