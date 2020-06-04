#Camera Object Detection with 2 camera multiprocessing Prototype
from multiprocessing import Process
import cv2 as cv
import imutils
import numpy as np

#Variable
carbase_width = 66    #Carbase width: 66 ca
escButton = 27        #Esc button
focal_length = 621    #Logitech 720p camera
found1, found2 = False, False   #Target found or not

#Target Object (rugby ball)
min_size = 10
object_width = 11.811   #11.8110236inches <-> 30 cm

#Color (HSV)
low_blue_H, low_blue_S, low_blue_V = 80, 80, 40
upper_blue_H, upper_blue_S, upper_blue_V = 140, 255, 255
low_yellow_H, low_yellow_S, low_yellow_V = 29, 80, 6
upper_yellow_H, upper_yellow_S, upper_yellow_V = 64, 255, 255

object_lower_blue = (low_blue_H, low_blue_S, low_blue_V)
object_upper_blue = (upper_blue_H, upper_blue_S, upper_blue_V)

object_lower_yellow = (low_yellow_H, low_yellow_S, low_yellow_V)
object_upper_yellow = (upper_yellow_H, upper_yellow_S, upper_yellow_V)

#Create HSV track bar
def nothing(x):     #Function for track bar
  pass              #Pass

trackbar_name_blue = "Blue HSV track bar"
trackbar_name_yellow = "Yellow HSV track bar"

#Distance
distance1 = -1.0
distance2 = -1.0

#Position
position1 = None
position2 = None

#Velocity
#x: 1 = Right  0 = Stop  -1 = Left
#y: 1 = Front  0 = Stop  -1 = Back
#z: 1 = Rotate to Right  0 = Stop  -1 = Rotate to Left
velocity1 = None
velocity2 = None

v_x1 = 0
v_y1 = 0
v_z1 = 0

v_x2 = 0
v_y2 = 0
v_z2 = 0

def findObjectToCamDistance(radius):
  global focal_length, object_width
  distance = ((object_width * focal_length) / (radius * 2)) * 2.54

  return distance

def findObjectToCamPosition(x, window1_left, window1_mid_left, window1_mid_right, window1_right):
  if x < window1_left:    #Object is located in left region
    position = "Left"

  elif x >= window1_left and x < window1_right:   #Object is located in middle region
    if x < window1_mid_left:
      position = "Middle - Left"

    elif x >= window1_mid_left and x < window1_mid_right:
      position = "Middle"

    else:
      position = "Middle - Right"

  else:                   #Object is located in right region
    position = "Right"

  return position

def findVelocity():
  pass

#Multiprocessing Function
def camera1():
  global distance1, found1, position1
  global object_lower_blue, object_upper_blue, object_lower_yellow, object_upper_yellow

  #Open camera1
  cam = cv.VideoCapture(1)
  if cam.isOpened():
    window_width = cam.get(cv.CAP_PROP_FRAME_WIDTH)
    window_height = cam.get(cv.CAP_PROP_FRAME_HEIGHT)

    window_area_width = window_width / 3

    window_left = window_area_width
    window_right = window_width - window_area_width

    window_mid_left = window_left + window_area_width / 3
    window_mid_right = window_right - window_area_width / 3

  else:
    print("Error: Camera 1 cannot open!!!")
    exit()

  while True:
    #Read frame from camera1
    retval, frame = cam.read()

    #Blur frame
    frame_blurred = cv.GaussianBlur(frame, (11, 11), 0)

    #Convert frame color space
    frame_hsv = cv.cvtColor(frame_blurred, cv.COLOR_BGR2HSV)

    #Construct a mask for the object color
    blue_mask = cv.inRange(frame_hsv, object_lower_blue, object_upper_blue)
    yellow_mask = cv.inRange(frame_hsv, object_lower_yellow, object_upper_yellow)

    #Combine masks together
    mask = cv.bitwise_or(blue_mask, yellow_mask)
    frame_mask = cv.bitwise_and(frame, frame, mask = mask)

    #Change the color of frame mask to gray and perfrom erode and dilate to it
    frame_mask = cv.cvtColor(frame_mask, cv.COLOR_BGR2GRAY)

    #Find contours in the frame?_mask
    contours = cv.findContours(frame_mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    #Contours object detection
    if len(contours) > 0:
      for contour in contours:
        mixed_contour = cv.convexHull(contour)

      ((x, y), radius) = cv.minEnclosingCircle(mixed_contour)

      if radius >= min_size:
        found1 = True

      else:
        found1 = False

    #If contours is found
    if found1:
      cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2) #Draw the minimum enclosing circle around the rball
      cv.circle(frame, (int(x), int(y)), 5, (0, 0, 255) , -1)   #Draw the center of the rball
      distance1 = findObjectToCamDistance(radius)
      position1 = findObjectToCamPosition(x, window_left, window_mid_left, window_mid_right, window_right)

    else:
      distance1 = -1.0
      position1 = None

    #Show the position and the distance from the camera to the target on the screen
    cv.putText(frame, "Position: {}".format(position1), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
    cv.putText(frame, "Distance: {} cm".format(distance1), (int(window_width) - 200, int(window_height) - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    #Testing
    #Main Frame
    cv.imshow("Camera 1", frame)
    #Frame Mask
    cv.imshow("Frame1 Mask", frame_mask)

    if cv.waitKey(1) == escButton:
      break

  cam.release()

def camera2():
  global distance2, found2, position2
  global object_lower_blue, object_upper_blue, object_lower_yellow, object_upper_yellow

  #Open camera2
  cam = cv.VideoCapture(2)
  if cam.isOpened():
    window_width = cam.get(cv.CAP_PROP_FRAME_WIDTH)
    window_height = cam.get(cv.CAP_PROP_FRAME_HEIGHT)

    window_area_width = window_width / 3

    window_left = window_area_width
    window_right = window_width - window_area_width

    window_mid_left = window_left + window_area_width / 3
    window_mid_right = window_right - window_area_width / 3

  else:
    print("Error: Camera 2 cannot open!!!")
    exit()

  while True:
    #Read frame from camera2
    retval, frame = cam.read()

    #Blur frame
    frame_blurred = cv.GaussianBlur(frame, (11, 11), 0)

    #Convert frame color space
    frame_hsv = cv.cvtColor(frame_blurred, cv.COLOR_BGR2HSV)

    #Construct a mask for the object color
    blue_mask = cv.inRange(frame_hsv, object_lower_blue, object_upper_blue)
    yellow_mask = cv.inRange(frame_hsv, object_lower_yellow, object_upper_yellow)

    #Combine masks together
    mask = cv.bitwise_or(blue_mask, yellow_mask)
    frame_mask = cv.bitwise_and(frame, frame, mask = mask)

    #Change the color of frame mask to gray and perfrom erode and dilate to it
    frame_mask = cv.cvtColor(frame_mask, cv.COLOR_BGR2GRAY)

    #Find contours in the frame mask
    contours = cv.findContours(frame_mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    #Contours object detection
    if len(contours) > 0:
      for contour in contours:
        mixed_contour = cv.convexHull(contour)

      ((x, y), radius) = cv.minEnclosingCircle(mixed_contour)

      if radius >= min_size:
        found2 = True

      else:
        found2 = False

    #If contours is found
    if found2:
      cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2) #Draw the minimum enclosing circle around the rball
      cv.circle(frame, (int(x), int(y)), 5, (0, 0, 255) , -1)   #Draw the center of the rball
      distance2 = findObjectToCamDistance(radius)
      position2 = findObjectToCamPosition(x, window_left, window_mid_left, window_mid_right, window_right)

    else:
      distance2 = -1.0
      position2 = None

    #Show the position and the distance from the camera to the target on the screen
    cv.putText(frame, "Position: {}".format(position2), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
    cv.putText(frame, "Distance: {} cm".format(distance2), (int(window_width) - 200, int(window_height) - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    #Testing
    #Main Frame
    cv.imshow("Camera 2", frame)
    #Frame Mask
    cv.imshow("Frame2 Mask", frame_mask)

    if cv.waitKey(1) == escButton:
      break

  cam.release()

#Main Thread
if __name__ == '__main__':
  #Create Multiprocessing
  cam1_p = Process(target = camera1)
  cam2_p = Process(target = camera2)

  #Start Multiprocessing
  cam1_p.start()
  cam2_p.start()

  #End Multiprocessing
  cam1_p.join()
  cam2_p.join()

  #End of Program
  cv.destroyAllWindows()
  print("Message: End of Program!!!")