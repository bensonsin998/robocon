# Main Purpose: Aimming System
#               -> From carbase to Goal
import cv2 as cv

print("Message: Aimming System: Start...")

# -------------------------------------------------------------------------------------------------------------

# Variable
# Camera variable
cam = cv.VideoCapture(0)

if not cam.isOpened():
  print("Error: Camera is not connected!!!")
  print("Error: Aimming System: Start -> End")
  exit()

window_width = cam.get(cv.CAP_PROP_FRAME_WIDTH)
window_height = cam.get(cv.CAP_PROP_FRAME_HEIGHT)

window_area_width = window_width / 3

window_left = window_area_width
window_right = window_width - window_area_width

# Aiming Star
hor_aim_l2_s = (int(window_width / 8 - 10), int(window_height / 2))
hor_aim_l2_e = (int(window_width / 8 + 10), int(window_height / 2))

hor_aim_l1_s = (int(window_width / 4 - 10), int(window_height / 2))
hor_aim_l1_e = (int(window_width / 4 + 10), int(window_height / 2))

hor_aim_main_s = (int(window_width / 2 - 10), int(window_height / 2))
hor_aim_main_e = (int(window_width / 2 + 10), int(window_height / 2))
ver_aim_main_s = (int(window_width / 2), int(window_height / 2 - 10))
ver_aim_main_e = (int(window_width / 2), int(window_height / 2 + 10))

hor_aim_r1_s = (int(window_width - window_width / 4 - 10), int(window_height / 2))
hor_aim_r1_e = (int(window_width - window_width / 4 + 10), int(window_height / 2))

hor_aim_r2_s = (int(window_width - window_width / 8 - 10), int(window_height / 2))
hor_aim_r2_e = (int(window_width - window_width / 8 + 10), int(window_height / 2))

# Aiming line thickness
aim_line_thickness = 2

# Region
region_l1_s = (int(window_left), 0)
region_l1_e = (int(window_left), int(window_height))

region_r1_s = (int(window_right), 0)
region_r1_e = (int(window_right), int(window_height))

# Testing -> 10
width10 = window_width / 10

support_l4_s = (int(width10), 0)
support_l4_e = (int(width10), int(window_height))

support_l3_s = (int(width10 * 2), 0)
support_l3_e = (int(width10 * 2), int(window_height))

support_l2_s = (int(width10 * 3), 0)
support_l2_e = (int(width10 * 3), int(window_height))

support_l1_s = (int(width10 * 4), 0)
support_l1_e = (int(width10 * 4), int(window_height))

support_r1_s = (int(width10 * 6), 0)
support_r1_e = (int(width10 * 6), int(window_height))

support_r2_s = (int(width10 * 7), 0)
support_r2_e = (int(width10 * 7), int(window_height))

support_r3_s = (int(width10 * 8), 0)
support_r3_e = (int(width10 * 8), int(window_height))

support_r4_s = (int(width10 * 9), 0)
support_r4_e = (int(width10 * 9), int(window_height))

# Esc button
escButton = 27

# -------------------------------------------------------------------------------------------------------------

while True:
  #Get frames from cam
  retval, frame = cam.read()

  # Aimming
  cv.line(frame, hor_aim_main_s, hor_aim_main_e, (255, 0, 0), aim_line_thickness)
  cv.line(frame, ver_aim_main_s, ver_aim_main_e, (255, 0, 0), aim_line_thickness)

  # cv.line(frame, hor_aim_l2_s, hor_aim_l2_e, (255, 0, 0), aim_line_thickness)
  # cv.line(frame, hor_aim_l1_s, hor_aim_l1_e, (255, 0, 0), aim_line_thickness)
  # cv.line(frame, hor_aim_r1_s, hor_aim_r1_e, (255, 0, 0), aim_line_thickness)
  # cv.line(frame, hor_aim_r2_s, hor_aim_r2_e, (255, 0, 0), aim_line_thickness)


  # Region
  #cv.line(frame, region_l1_s, region_l1_e, (0, 0, 255), 1)
  #cv.line(frame, region_r1_s, region_r1_e, (0, 0, 255), 1)

  # Support
  cv.line(frame, support_l4_s, support_l4_e, (0, 255, 0), aim_line_thickness)
  cv.line(frame, support_l3_s, support_l3_e, (0, 255, 0), aim_line_thickness)
  cv.line(frame, support_l2_s, support_l2_e, (0, 255, 0), aim_line_thickness)
  cv.line(frame, support_l1_s, support_l1_e, (0, 255, 0), aim_line_thickness)
  cv.line(frame, support_r1_s, support_r1_e, (0, 255, 0), aim_line_thickness)
  cv.line(frame, support_r2_s, support_r2_e, (0, 255, 0), aim_line_thickness)
  cv.line(frame, support_r3_s, support_r3_e, (0, 255, 0), aim_line_thickness)
  cv.line(frame, support_r4_s, support_r4_e, (0, 255, 0), aim_line_thickness)

  # Dispaly
  cv.imshow("Aimming", frame)

  #Wait "Esc" is press and break the loop
  if cv.waitKey(1) == escButton:
    break

#End of program
cam.release()             #Release camera control
cv.destroyAllWindows()    #Close all the windows create by the program / opencv
print("Message: Aimming System: Start -> End")
