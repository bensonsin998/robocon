import cv2 as cv
import imutils as im
import numpy as np
import math
import pyrealsense2 as rs

print("Message: Camera Algorithm: Start...")

# Variables
# RealSense
print("Message: Intel RealSense Camera: Initializing...")

# Camera variables
color_fps = 30
depth_fps = 30
window_height = 480
window_width = 640
# Debug: Display information
print("Information: Intel RealSense Camera")
print("             window_height: ", window_height, "\t window_width: ", window_width)
print("             color_fps: ", color_fps)
print("             depth_fps: ", depth_fps)

# Create an rs object which owns the handles to all connected intel Realsense devices
pipe = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, window_width, window_height, rs.format.bgr8, color_fps)
config.enable_stream(rs.stream.depth, window_width, window_height, rs.format.z16, depth_fps)

try:
  # Start streaming
  pipe.start(config)

except Exception as e:
  print("RS -> Error: ", e)
  print("Message: Camera Algorithm: End")
  exit()

print("Message: Intel Realsense Camera: Initializing -> Success!!!")
# -------------------------------------------------------------------------------------------------------------

print("Message: Environment variables: Initializing...")

# Aiming Star
hor_left1_aim_s = (int(window_width / 8 - 10), int(window_height / 2))
hor_left1_aim_e = (int(window_width / 8 + 10), int(window_height / 2))

hor_left2_aim_s = (int(window_width / 4 - 10), int(window_height / 2))
hor_left2_aim_e = (int(window_width / 4 + 10), int(window_height / 2))

hor_aim_s = (int(window_width / 2 - 10), int(window_height / 2))
hor_aim_e = (int(window_width / 2 + 10), int(window_height / 2))

hor_right1_aim_s = (int(window_width - window_width / 4 - 10), int(window_height / 2))
hor_right1_aim_e = (int(window_width - window_width / 4 + 10), int(window_height / 2))

ver_aim_s = (int(window_width / 2), int(window_height / 2 - 10))
ver_aim_e = (int(window_width / 2), int(window_height / 2 + 10))

hor_right2_aim_s = (int(window_width - window_width / 8 - 10), int(window_height / 2))
hor_right2_aim_e = (int(window_width - window_width / 8 + 10), int(window_height / 2))

# Debug: Display information
print("Information: hor_left1_aim_s: ", hor_left1_aim_s, "\t hor_left1_aim_e: ", hor_left1_aim_e)
print("             hor_left2_aim_s: ", hor_left2_aim_s, "\t hor_left2_aim_e: ", hor_left2_aim_e)
print("             hor_aim_s: ", hor_aim_s, "\t hor_aim_e: ", hor_aim_e)
print("             ver_aim_s: ", ver_aim_s, "\t ver_aim_e: ", ver_aim_e)
print("             hor_right1_aim_s: ", hor_right1_aim_s, "\t hor_right1_aim_e: ", hor_right1_aim_e)
print("             hor_right2_aim_s: ", hor_right2_aim_s, "\t hor_right2_aim_e: ", hor_right2_aim_e)

# Color Space: HSV
object_lower_blue = (low_blue_H, low_blue_S, low_blue_V) = (80, 80, 40)
object_upper_blue = (upper_blue_H, upper_blue_S, upper_blue_V) = (140, 255, 255)

object_lower_yellow = (low_yellow_H, low_yellow_S, low_yellow_V) = (29, 80, 6)
object_upper_yellow = (upper_yellow_H, upper_yellow_S, upper_yellow_V) = (64, 255, 255)

# Debug: Display
print("Information: object_lower_blue = (low_blue_H,low_blue_S, low_blue_V): ", object_lower_blue)
print("             object_upper_blue = (upper_blue_H, upper_blue_S, upper_blue_V): ", object_upper_blue)
print("             object_lower_yellow = (low_yellow_H, low_yellow_S, low_yellow_V): ", object_lower_yellow)
print("             object_upper_yellow = (upper_yellow_H, upper_yellow_S, upper_yellow_V): ", object_upper_yellow)

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
# Debug: Display information
print("Information: Distance: ", distance)

# Esc Button (ASCII code)
escButton = 27
# Debug: Display information
print("Information: Esc: ", escButton)

# Position
# Position:
#           -> Left
#           -> Middle - Left
#           -> Middle
#           -> Middle - Right
#           -> Right
position = None
# Debug: Display information
print("Information: position: ", position)


# Target: Kickball (Rugby ball)
min_size = 10
print("Information: min_size: ", min_size)

# Velocity
# v_x:  1 = Right  0 = Stop  -1 = Left
# v_y:  1 = Front  0 = Stop  -1 = Back
# v_z:  1 = Rotate to Right  0 = Stop  -1 = Rotate to Left
velocity = (v_x, v_y, v_z) = (0, 0, 0)
# Debug: Display information
print("Information: velocity = (v_x, v_y, v_z): ", velocity)

# Window size
window_area_width = window_width / 3

window_left = window_area_width
window_right = window_width - window_area_width

window_mid_left = window_left + window_area_width / 3
window_mid_right = window_right - window_area_width / 3

# Debug: Display information
print("Information: window_area_width: ", window_area_width)
print("             window_left: ", window_left)
print("             window_right: ", window_right)
print("             window_mid_left: ", window_mid_left)
print("             window_mid_right: ", window_mid_right)


print("Message: Environment variables: Initialing -> Success!!!")
# -------------------------------------------------------------------------------------------------------------

print("Message: Camera object detection: Start")

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
    # Depth image must be converted to 8-bit per pixel first
    depth_colormap = cv.applyColorMap(cv.convertScaleAbs(depth_image, alpha = 0.3), cv.COLORMAP_JET)

    # TODO: Find target (kickball)
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

      # Postion
      if x < window_left:
        position = "Left"

      elif x >= window_left and x < window_right:
        if x < window_mid_left:
          position = "Middle - Left"

        elif x >= window_mid_left and x < window_mid_right:
          position = "Middle"

        else:
          position = "Middle - Right"

      else:
        position = "Right"

      # TODO: Velocity

    # Reset variables if target is not found
    else:
      distance = -1.0
      position = "None"
      velocity = (0, 0, 0)

    # Debug: Display contour information
    cv.putText(color_image, "Position: {}".format(position), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
    cv.putText(color_image, "Distance: {}cm".format(distance), (int(window_width) - 200, int(window_height) - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # Debug: Display image
    #        Color_image -> Aiming star
    cv.line(color_image, hor_left1_aim_s, hor_left1_aim_e, (255, 0, 0))
    cv.line(color_image, hor_left2_aim_s, hor_left2_aim_e, (255, 0, 0))
    cv.line(color_image, hor_aim_s, hor_aim_e, (255, 0, 0))
    cv.line(color_image, ver_aim_s, ver_aim_e, (255, 0, 0))
    cv.line(color_image, hor_right1_aim_s, hor_right1_aim_e, (255, 0, 0))
    cv.line(color_image, hor_right2_aim_s, hor_right2_aim_e, (255, 0, 0))
    #        Color_image
    cv.imshow("Intel RealSense: color_image", color_image)
    #        Depth_image
    cv.imshow("Intel RealSense: depth_colormap", depth_colormap)

    if cv.waitKey(1) == escButton:
      break

except Exception as e:
  print("RS -> Error: ", e)
  print("Message: Camera Algorithm: End")
  exit()

finally:
  print("Message: Camera object detection: End")
  # Stop streaming
  pipe.stop()

# End of program
cv.destroyAllWindows()    # Close all the windows create by the program

print("Message: Camera Algorithm: End")
# -------------------------------------------------------------------------------------------------------------