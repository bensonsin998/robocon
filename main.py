#Main Purpose:  1. Start the camera
#               2. Read the frame from the camera
#               3. Locate the object: rugby ball
#               4. Keep Calculating the position between the camera and the object
from collections import deque
import cv2 as cv
import imutils
import numpy as np

#Global Variable
#Camera and Window Variables:
cam = cv.cv2.VideoCapture(0, cv.CAP_DSHOW)   #Open the default camera
if not cam.isOpened():      #Error handler -> When cannot open the camera
    print("Error: Cannot open camera!!!")
    exit();
else:
    cam_Width = cam.get(cv.CAP_PROP_FRAME_WIDTH)
    cam_Height = cam.get(cv.CAP_PROP_FRAME_HEIGHT)
    cam_Width_Middle = cam_Width / 2
escButton = 27 #ESC
#Target Object (rugby ball)
center = None
contours = None
direction = None
dx, dy = None, None
HSVLower = (29, 86, 6)
HSVUpper = (64, 255, 255)
minSize = 10
points = deque(maxlen = 100)
points_counter = 0
position = None
radius = None
x, y = 0 , 0

while True:
  #Get frames from cam
  retval, frame = cam.read()

  frame_blurred = cv.GaussianBlur(frame, (11, 11), 0)       #Blur the frame
  frame_hsv = cv.cvtColor(frame_blurred, cv.COLOR_BGR2HSV)  #Convert the color space to HSV

  #Construct a mask for the object color
  frame_mask = cv.inRange(frame_hsv, HSVLower, HSVUpper)
  frame_mask = cv.erode(frame_mask, None, iterations = 2)
  frame_mask = cv.dilate(frame_mask, None, iterations = 2)

  #Find contours in the mask
  contours = cv.findContours(frame_mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
  contours = imutils.grab_contours(contours)

  #If the program find one or more contours
  if len(contours) > 0:
    larget_contours = max(contours, key = cv.contourArea)

    ((x, y), radius) = cv.minEnclosingCircle(larget_contours)
    mom = cv.moments(larget_contours)
    center = (int(mom["m10"] / mom["m00"]), int(mom["m01"] / mom["m00"]))

    if radius > minSize:   #The rball requires at least 10 pixel radius to track it
      cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2) #Draw the minimum enclosing circle around the rball
      cv.circle(frame, center, 5, (0, 0, 255) , -1)   #Draw the center of the rball
      points.appendleft(center)                 #Update the list of points containing the center (x, y) of the object

      #Testing
      print("Center: ", center)
      print("X, Y", (x, y))

  #TODO: Find the distance and position from the camera to the target
  if x < cam_Width_Middle - 100:
    direction = "Right"
  elif x >= cam_Width_Middle - 100 and x <= cam_Width_Middle + 100:
    if x < cam_Width_Middle:
      direction = "Middle - Right"
    elif x == cam_Width_Middle:
      direction = "Middle"
    else:
      direction = "Middle - Left"
  else:
    direction = "Left"

  cv.putText(frame, direction, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 3)
  cv.putText(frame, "dx: {}, dy: {}".format(dx, dy), (10, 670), cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

  #Testing
  cv.imshow("Frame_mask", frame_mask)

  #Display the result to the screen
  cv.imshow("Camera", frame)

  #Wait "Esc" is press and break the loop
  if cv.waitKey(1) == escButton:
    break

  points_counter += 1

cam.release()
cv.destroyAllWindows()