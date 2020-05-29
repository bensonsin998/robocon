#Main Purpose:  1. Start the camera
#               2. Read the frame from the camera
#               3. Locate the object: rugby ball
#               4. Calculate distance from camera to object
#               5. Return the velocity
import cv2 as cv
import imutils
import numpy as np

#Global Variable
#Camera and Window Variables:
cam_open = False
cam = cv.VideoCapture(0)   #Open the default camera

if cam.isOpened():
  cam_open = True

else:
  cam = cv.VideoCapture(-1)   #For raspberry pi -> -1 index means it find camera by itself

  if cam.isOpened():
    cam_open = True

if cam_open:
  window_width = cam.get(cv.CAP_PROP_FRAME_WIDTH)
  window_height = cam.get(cv.CAP_PROP_FRAME_HEIGHT)

  window_area_width = window_width / 3

  window_left = window_area_width
  window_right = window_width - window_area_width

  window_mid_left = window_left + window_area_width / 3
  window_mid_right = window_right - window_area_width / 3

else:
  print("Error: Cannot open camera!!!")
  exit()

escButton = 27        #ESC
focal_length = 363    #Camera value <-  Lenovo: 363
                      #                 Logitech 720p camera: 534

#Target Object (rugby ball)
center = None
contours = None
distance = -1.0
dx, dy = None, None
found = False
min_size = 10
mixed_contour = None
object_width = 11.811   #11.8110236inches <-> 30 cm
position = None
radius = None
x, y = 0 , 0

#Color (HSV)
low_blue_H, low_blue_S, low_blue_V = 80, 80, 0
upper_blue_H, upper_blue_S, upper_blue_V = 140, 255, 255
low_yellow_H, low_yellow_S, low_yellow_V = 29, 80, 6
upper_yellow_H, upper_yellow_S, upper_yellow_V = 64, 255, 255


#Create HSV track bar
def nothing(x):
  pass

trackbar_name_blue = "Blue HSV track bar"
trackbar_name_yellow = "Yellow HSV track bar"

cv.namedWindow(trackbar_name_blue, cv.WINDOW_AUTOSIZE)
cv.namedWindow(trackbar_name_yellow, cv.WINDOW_AUTOSIZE)

cv.createTrackbar("L H: ", trackbar_name_blue, low_blue_H, 255, nothing)
cv.createTrackbar("L S: ", trackbar_name_blue, low_blue_S, 255, nothing)
cv.createTrackbar("L V: ", trackbar_name_blue, low_blue_V, 255, nothing)

cv.createTrackbar("U H: ", trackbar_name_blue, upper_blue_H, 255, nothing)
cv.createTrackbar("U S: ", trackbar_name_blue, upper_blue_S, 255, nothing)
cv.createTrackbar("U V: ", trackbar_name_blue, upper_blue_V, 255, nothing)

cv.createTrackbar("L H: ", trackbar_name_yellow, low_yellow_H, 255, nothing)
cv.createTrackbar("L S: ", trackbar_name_yellow, low_yellow_S, 255, nothing)
cv.createTrackbar("L V: ", trackbar_name_yellow, low_yellow_V, 255, nothing)

cv.createTrackbar("U H: ", trackbar_name_yellow, upper_yellow_H, 255, nothing)
cv.createTrackbar("U S: ", trackbar_name_yellow, upper_yellow_S, 255, nothing)
cv.createTrackbar("U V: ", trackbar_name_yellow, upper_yellow_V, 255, nothing)

#Velocity
velocity = None
v_x = 0     #1 = Right  0 = Stop  -1 = Left
v_y = 0     #1 = Front  0 = Stop  -1 = Back
v_z = 0     #1 = Rotate to Right  0 = Stop  -1 = Rotate to Left

while True:
  #Get frames from cam
  retval, frame = cam.read()

  frame_blurred = cv.GaussianBlur(frame, (11, 11), 0)       #Blur the frame
  frame_hsv = cv.cvtColor(frame_blurred, cv.COLOR_BGR2HSV)  #Convert the color space to HSV

  object_lower_blue = (cv.getTrackbarPos("L H: ", trackbar_name_blue),
                        cv.getTrackbarPos("L S: ", trackbar_name_blue),
                        cv.getTrackbarPos("L V: ", trackbar_name_blue))

  object_upper_blue = (cv.getTrackbarPos("U H: ", trackbar_name_blue),
                        cv.getTrackbarPos("U S: ", trackbar_name_blue),
                        cv.getTrackbarPos("U V: ", trackbar_name_blue))

  object_lower_yellow = (cv.getTrackbarPos("L H: ", trackbar_name_yellow),
                          cv.getTrackbarPos("L S: ", trackbar_name_yellow),
                          cv.getTrackbarPos("L V: ", trackbar_name_yellow))

  object_upper_yellow = (cv.getTrackbarPos("U H: ", trackbar_name_yellow),
                          cv.getTrackbarPos("U S: ", trackbar_name_yellow),
                          cv.getTrackbarPos("U V: ", trackbar_name_yellow))

  #Construct a mask for the object color
  blue_mask = cv.inRange(frame_hsv, object_lower_blue, object_upper_blue)
  yellow_mask = cv.inRange(frame_hsv, object_lower_yellow, object_upper_yellow)

  #Combine masks together
  mask = cv.bitwise_or(blue_mask, yellow_mask)
  frame_mask = cv.bitwise_and(frame, frame, mask = mask)

  #Change the color of frame_mask to gray and perfrom erode and dilate to it
  frame_mask = cv.cvtColor(frame_mask, cv.COLOR_BGR2GRAY)
  frame_mask = cv.erode(frame_mask, None, iterations = 3)
  frame_mask = cv.dilate(frame_mask, None, iterations = 3)

  #Find contours in the mask
  contours = cv.findContours(frame_mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
  contours = imutils.grab_contours(contours)

  if len(contours) > 0:
    for contour in contours:
      mixed_contour = cv.convexHull(contour)

    ((x, y), radius) = cv.minEnclosingCircle(mixed_contour)
    mom = cv.moments(mixed_contour)
    #center = (int(mom["m10"] / mom["m00"]), int(mom["m01"] / mom["m00"]))

    if radius >= min_size:
      found = True

    else:
      found = False

  else:
    found = False

  #If object is found, then circle the object, and calculate the distance and velocity
  if found:
    cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2) #Draw the minimum enclosing circle around the rball
    cv.circle(frame, (int(x), int(y)), 5, (0, 0, 255) , -1)   #Draw the center of the rball

    #Find object position
    if x < window_left:   #Object is located in left region
      position = "Left"
      v_x = -1
      v_y = 1
      v_z = 0

    elif x >= window_left and x < window_right: #Object is located in middle region
      if x < window_mid_left:
        position = "Middle - Left"

      elif x >= window_mid_left and x < window_mid_right:
        position = "Middle"

      else:
        position = "Middle - Right"

      v_x = 0
      v_y = 1
      v_z = 0

    else:               #Object is located in right region
      position = "Right"
      v_x = 1
      v_y = 1
      v_z = 0

    #Find object distance to camera
    #print(radius * 2)      #<- Calculate focal length
    distance = ((object_width * focal_length) / (radius * 2)) * 2.54
    distance = round(distance, 3)

    #Rotate the robot if the distance is less then 3cm
    if distance <= 3.0:
      v_y = 0

      if position == "Left" or position == "Middle - Left":
        v_z = -1

      elif position == "Right" or position == "Middle - Right":
        v_z = 1

      else:
        v_z = 0

    #Return velocity
    velocity = (v_x, v_y, v_z)
    print(velocity)     #Testing

  #If object is not found, then reset variable
  else:
    position = ""
    distance = -1.0
    velocity = (0, 0, 0)
    print(velocity)     #Testing

  #Show the position and the distance from the camera to the target on the screen
  cv.putText(frame, "Position: {}".format(position), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
  cv.putText(frame, "Distance: {} cm".format(distance), (int(window_width) - 200, int(window_height) - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

  #Show frame
  cv.imshow("Camera", frame)          #Display the result to the screen

  #Testing
  #cv.imshow("Frame_mask", frame_mask)
  #cv.imshow("Blue", blue_mask)
  #cv.imshow("Yellow", yellow_mask)

  #Wait "Esc" is press and break the loop
  if cv.waitKey(1) == escButton:
    break

cam.release()
cv.destroyAllWindows()
print("End of Program")