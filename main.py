#Main Purpose:  1. Start the camera
#               2. Read the frame from the camera
#               3. Locate the object: rugby ball
#               4. Keep Calculating the position between the camera and the object
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
    window_width = cam.get(cv.CAP_PROP_FRAME_WIDTH)
    window_height = cam.get(cv.CAP_PROP_FRAME_HEIGHT)

    window_area_width = window_width / 3

    window_left = window_area_width
    window_mid_left = window_left + window_area_width / 3
    window_mid_right = window_width - window_area_width * 4 / 3
    window_right = window_width - window_area_width

escButton = 27 #ESC

focal_length = 50.0

lower_blue = (80, 80, 0)
upper_blue = (140, 255, 255)

lower_green = (29, 80, 6)
upper_green = (64, 255, 255)

min_size = 10

#Target Object (rugby ball)
center = None
contours = None
distance = -1.0
dx, dy = None, None
object_width = 2400.0
points = []
position = None
radius = None
x, y = 0 , 0

mixed_contour = None

while True:
  #Get frames from cam
  retval, frame = cam.read()

  frame_blurred = cv.GaussianBlur(frame, (11, 11), 0)       #Blur the frame
  frame_hsv = cv.cvtColor(frame_blurred, cv.COLOR_BGR2HSV)  #Convert the color space to HSV

  #Construct a mask for the object color
  blue_mask = cv.inRange(frame_hsv, lower_blue, upper_blue)
  green_mask = cv.inRange(frame_hsv, lower_green, upper_green)

  #Combine masks together
  mask = cv.bitwise_or(blue_mask, green_mask)
  frame_mask = cv.bitwise_and(frame, frame, mask = mask)

  #Change the color of frame_mask to gray and perfrom erode and dilate to it
  frame_mask = cv.cvtColor(frame_mask, cv.COLOR_BGR2GRAY)
  frame_mask = cv.erode(frame_mask, None, iterations = 2)
  frame_mask = cv.dilate(frame_mask, None, iterations = 2)

  #Find contours in the mask
  contours = cv.findContours(frame_mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
  contours = imutils.grab_contours(contours)

  #Testing
  #TODO: Make multi contours as one
  if len(contours) > 0:
    for contour in contours:
      mixed_contour = cv.convexHull(contour)

    ((x, y), radius) = cv.minEnclosingCircle(mixed_contour)
    mom = cv.moments(mixed_contour)
    center = (int(mom["m10"] / mom["m00"]), int(mom["m01"] / mom["m00"]))

    cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2) #Draw the minimum enclosing circle around the rball
    cv.circle(frame, center, 5, (0, 0, 255) , -1)   #Draw the center of the rball
    points.append(center)                 #Update the list of points containing the center (x, y) of the object

    #Find object position
    if x < window_left:
      position = "Left"

    elif x >= window_left and x < window_right:
      pass
      if x < window_mid_left:
        position = "Middle - Left"

      elif x >= window_mid_left and x < window_mid_right:
        position = "Middle"

      else:
        position = "Middle - Right"

    else:
      position = "Right"

    distance = (object_width * focal_length / (radius * 2)) / 10
    distance = round(distance, 3)

  else:
    position = ""
    distance = -1.0

  #Show the position and the moving direction(dx, dy) from the camera to the target on the screen
  cv.putText(frame, "Position: {}".format(position), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
  cv.putText(frame, "dx: {}, dy: {}".format(dx, dy), (10, int(window_height) - 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
  cv.putText(frame, "Distance: {}cm".format(distance), (int(window_width) - 200, int(window_height) - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

  #Show frame
  cv.imshow("Camera", frame)          #Display the result to the screen

  #Testing
  cv.imshow("Frame_mask", frame_mask)
  cv.imshow("Blue", blue_mask)
  cv.imshow("Green", green_mask)

  #Wait "Esc" is press and break the loop
  if cv.waitKey(1) == escButton:
    break

cam.release()
cv.destroyAllWindows()
print("End of Program")