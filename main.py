#Main Purpose:  1. Start the camera
#               2. Read the frame from the camera
#               3. Locate the object: rugby ball
#               4. Keep Calculating the position between the camera and the object
import cv2 as cv
import imutils
import numpy as np

#Variable
escButton = 27   #Esc
object_HSVLower = (29, 86, 6)
object_HSVUpper = (64, 255, 255)

#Initialize the camera
cam = cv.VideoCapture(0)    #Open the default camera
if not cam.isOpened():       #If the program cannot open the camera
    print("Error: Cannot open camera!!!")   #Print message and exit the program
    exit()

#Main Loop: Keep reading frame from the camera and locate the object
while True:
    #Get the frame from the camera
    retval, frame = cam.read()

    frame_blurred = cv.GaussianBlur(frame, (11, 11), 0)       #Blur the frame
    frame_hsv = cv.cvtColor(frame_blurred, cv.COLOR_BGR2HSV)  #Convert the color space to HSV

    #Construct a mask for the object color
    frame_mask = cv.inRange(frame_hsv, object_HSVLower, object_HSVUpper)
    frame_mask = cv.erode(frame_mask, None, iterations = 2)
    frame_mask = cv.dilate(frame_mask, None, iterations = 2)

    #Find the contours in the mask
    object_contours = cv.findContours(frame_mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    object_contours = imutils.grab_contours(object_contours)


    #Display the result to the screen
    cv.imshow("Camera", frame)

    #Wait "Esc" is press and break the loop
    if cv.waitKey(1) == escButton:
        break

cv.destroyAllWindows()