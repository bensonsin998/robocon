import cv2 as cv
import imutils as im
import numpy as np
import math
import pyrealsense2 as rs

print("Message: Camera Algorithm: Start...")

# Camera variables
color_fps = 15
depth_fps = 15
window_height = 480
window_width = 640

# Create an pyrealsense2 object which owns the handles to all connected intel Realsense devices
pipe = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, window_width, window_height, rs.format.bgr8, color_fps)
config.enable_stream(rs.stream.depth, window_width, window_height, rs.format.z16, depth_fps)

try:
  # Start streaming
  pipe.start(config)

except Exception as e:
  print("RS -> Error: ", e)
  print("Message: Camera Algorithm: Start -> End")
  exit()

# -------------------------------------------------------------------------------------------------------------

# Color Space: HSV
object_lower_blue = (low_blue_H, low_blue_S, low_blue_V) = (83, 98, 43)
object_upper_blue = (upper_blue_H, upper_blue_S, upper_blue_V) = (95, 255, 255)

object_lower_yellow = (low_yellow_H, low_yellow_S, low_yellow_V) = (20, 167, 0)
object_upper_yellow = (upper_yellow_H, upper_yellow_S, upper_yellow_V) = (85, 255, 255)


# """   # <- Delete the first # to comment the Track bar block
# Debug: Color Space -> Track bar
def nothing(x):
  pass

trackbar_name_blue = "Blue HSV track bar"
trackbar_name_yellow = "Yellow HSV track bar"

# Blue track bar window
cv.namedWindow(trackbar_name_blue, cv.WINDOW_AUTOSIZE)

cv.createTrackbar("L H: ", trackbar_name_blue, low_blue_H, 255, nothing)
cv.createTrackbar("L S: ", trackbar_name_blue, low_blue_S, 255, nothing)
cv.createTrackbar("L V: ", trackbar_name_blue, low_blue_V, 255, nothing)

cv.createTrackbar("U H: ", trackbar_name_blue, upper_blue_H, 255, nothing)
cv.createTrackbar("U S: ", trackbar_name_blue, upper_blue_S, 255, nothing)
cv.createTrackbar("U V: ", trackbar_name_blue, upper_blue_V, 255, nothing)

# Yellow track bar window
cv.namedWindow(trackbar_name_yellow, cv.WINDOW_AUTOSIZE)

cv.createTrackbar("L H: ", trackbar_name_yellow, low_yellow_H, 255, nothing)
cv.createTrackbar("L S: ", trackbar_name_yellow, low_yellow_S, 255, nothing)
cv.createTrackbar("L V: ", trackbar_name_yellow, low_yellow_V, 255, nothing)

cv.createTrackbar("U H: ", trackbar_name_yellow, upper_yellow_H, 255, nothing)
cv.createTrackbar("U S: ", trackbar_name_yellow, upper_yellow_S, 255, nothing)
cv.createTrackbar("U V: ", trackbar_name_yellow, upper_yellow_V, 255, nothing)

# """   # <- Delete the first # to comment the Track bar block

# Distance
distance = -1.0   # -1.0 <-> Target not found
# safe_distance = 30.0  # >= 30cm <- Always full power, i.e. v_y = 1
target_distance = 20.0  # Target: 20cm <- The most suitable distance to kick the target

# Esc Button (ASCII code)
escButton = 27

# Position
# Position:
#           -> Left
#           -> Middle - Left
#           -> Middle
#           -> Middle - Right
#           -> Right
position = None

# Target: Kickball (Rugby ball)
min_size = 10

# Velocity
# x:  1 = Right  0 = Stop  -1 = Left
# y:  1 = Front  0 = Stop  -1 = Back
# z:  1 = Rotate to Right  0 = Stop  -1 = Rotate to Left
velocity = (0, 0, 0)

# Window
window_middle = window_width / 2

window_area_width = window_width / 3
window_left = window_area_width
window_right = window_width - window_area_width
window_mid_left = window_left + window_area_width / 3
window_mid_right = window_right - window_area_width / 3

# Window -> Region
region_l1_s = (int(window_left), 0)
region_l1_e = (int(window_left), int(window_height))

region_r1_s = (int(window_right), 0)
region_r1_e = (int(window_right), int(window_height))

# -------------------------------------------------------------------------------------------------------------

def find_position(_x):
  _position = ""

  if _x < window_left:
    _position = "Left"

  elif _x >= window_left and _x < window_right:
    if _x < window_mid_left:
      _position = "Middle - Left"

    elif _x >= window_mid_left and _x < window_mid_right:
      _position = "Middle"

    else:
      _position = "Middle - Right"

  else:
    _position = "Right"

  return _position

def find_velocity(_distance, _x):
  _v_x = 0
  _v_y = 0
  _v_z = 0

  # v_x
  if _x < window_middle:
    _v_x = -1 if ((_x - window_middle) / 100) < -1 else (_x - window_middle) / 100

  elif _x > window_middle:
    _v_x = 1 if ((_x - window_middle) / 100) > 1 else (_x - window_middle) / 100

  else:
    _v_x = 0

  # v_y
  if _distance > target_distance:
    _v_y = 1 if ((_distance - target_distance) / 10) > 1 else (_distance - target_distance) / 10

  elif _distance == target_distance:
    _v_y = 0

  else:
    _v_y = -1 if ((_distance - target_distance) / 10) < -1 else (_distance - target_distance) / 10

  # v_z
  _v_z = 0

  return (_v_x, _v_y, _v_z)

# -------------------------------------------------------------------------------------------------------------

try:
  while True:
    # Wait for frames from camera
    frames = pipe.wait_for_frames()

    # Get color frame and depth frame from frames data set
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()

    # Prevent getting error data frames data set
    if not color_frame or not depth_frame:
      continue

    # Convert images to numpy arrays
    color_image = np.asanyarray(color_frame.get_data())
    depth_image = np.asanyarray(depth_frame.get_data())

    # Apply color map on depth image
    #   -> Depth image must be converted to 8-bit per pixel first
    depth_colormap = cv.applyColorMap(cv.convertScaleAbs(depth_image, alpha = 0.3), cv.COLORMAP_JET)

    # Smoothing image and filtering noisy data -> Gaussian Blur
    color_frame = cv.GaussianBlur(color_image, (11, 11), 0)

    # Convert color space from BGR -> HSV
    frame_hsv = cv.cvtColor(color_frame, cv.COLOR_BGR2HSV)

    # """   # <- Delete the first # to comment the Track bar block
    # Debug: Get HSV color from trackbar
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

    # """   # <- Delete the first # to comment the Track bar block

    # Construct a mask for the object color
    blue_mask = cv.inRange(frame_hsv, object_lower_blue, object_upper_blue)
    yellow_mask = cv.inRange(frame_hsv, object_lower_yellow, object_upper_yellow)

    # Combine masks together
    blue_yellow_mask = cv.bitwise_or(blue_mask, yellow_mask)
    frame_mask = cv.bitwise_and(color_frame, color_image, mask = blue_yellow_mask)

    # Change the color of frame_mask to gray and perfrom erode and dilate to it
    frame_mask = cv.cvtColor(frame_mask, cv.COLOR_BGR2GRAY)
    frame_mask = cv.erode(frame_mask, None, iterations = 3)
    frame_mask = cv.dilate(frame_mask, None, iterations = 3)

    # Find contours in the frame_mask
    contours = cv.findContours(frame_mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = im.grab_contours(contours)

    # Calculate contour information
    if len(contours) > 0:   # If more than one contours is found
      for contour in contours:
        mixed_contour = cv.convexHull(contour)    # Combine contours together

      # Calculate the xy coordinates and radius of the contour
      ((x, y), radius) = cv.minEnclosingCircle(mixed_contour)

      # Requirement: Contour must be larger than or equal to the min_size
      if radius >= min_size:
        found = True

      else:
        found = False

    else:
      found = False

    # If target is found
    if found:
      # Circle the target and center
      cv.circle(color_image, (int(x), int(y)), int(radius), (0, 255, 255), 2)   # Circle the target
      cv.circle(color_image, (int(x), int(y)), 5, (0, 0, 255), -1)    # Draw the center of the target

      # Distance
      # distance = depth_frame.get_distance(int(window_width / 2), int(window_height / 2))   # <- Testing
      distance = round(depth_frame.get_distance(int(x), int(y)) * 100, 3)

      # Position
      position = find_position(x)

      # Velocity
      velocity = find_velocity(distance, x)

    # Reset variables if target is not found
    else:
      distance = -1.0
      position = "None"
      velocity = (0, 0, 0)

    # ROS:
    #      publish the velocity to the ROS core

    # Debug:
    #        Color_image -> Region
    cv.line(color_image, region_l1_s, region_l1_e, (255, 0, 0), 2)
    cv.line(color_image, region_r1_s, region_r1_e, (255, 0, 0), 2)
    #        Color_image -> Display contour information
    cv.putText(color_image, "Position: {}".format(position), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
    cv.putText(color_image, "Distance: {}cm".format(distance), (int(window_width) - 200, int(window_height) - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    #         Display: Color_image
    cv.imshow("Intel RealSense: color_image", color_image)
    #                  Depth_image
    cv.imshow("Intel RealSense: depth_colormap", depth_colormap)

    if cv.waitKey(1) == escButton:
      break

except Exception as e:
  print("RS -> Error: ", e)
  print("Message: Camera Algorithm: Start -> End")
  exit()

finally:
  print("Message: Camera Algorithm: Start -> End")
  # Stop streaming
  pipe.stop()

# End of program
cv.destroyAllWindows()    # Close all the windows create by the program

print("Message: Camera Algorithm: End")

# -------------------------------------------------------------------------------------------------------------