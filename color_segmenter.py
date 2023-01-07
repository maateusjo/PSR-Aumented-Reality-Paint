#!/usr/bin/env python3
# ----------------------------------------------------
# Mateus Araujo (116290) e Rafael Mendes (116336)
# PSR Aumented Reality Paint, December 2022
# ----------------------------------------------------

# Import opencv and numpy
import cv2  
import numpy as np
import json


def main():

    # Trackbar callback fucntion does nothing but required for trackbar
    def nothing(x):
        pass

    # Create a seperate window named 'Trackbars' for trackbar
    cv2.namedWindow('Trackbars',cv2.WINDOW_NORMAL)

    cv2.createTrackbar('R min','Trackbars',0,255,nothing)
    cv2.createTrackbar('R max','Trackbars',255,255,nothing)
    cv2.createTrackbar('G min','Trackbars',0,255,nothing)
    cv2.createTrackbar('G max','Trackbars',255,255,nothing)
    cv2.createTrackbar('B min','Trackbars',0,255,nothing)
    cv2.createTrackbar('B max','Trackbars',255,255,nothing)

    # Capture video from webcam
    vid = cv2.VideoCapture(0)

    # Create a while loop act as refresh for the view 
    while True:

        # Read the video frame by frame
        ret, frame = vid.read()
        frame = cv2.resize(frame, (640, 360))

        # Get the current position of all the trackbars
        rmin = cv2.getTrackbarPos('R min','Trackbars')
        rmax = cv2.getTrackbarPos('R max','Trackbars')
        gmin = cv2.getTrackbarPos('G min','Trackbars')
        gmax = cv2.getTrackbarPos('G max','Trackbars')
        bmin = cv2.getTrackbarPos('B min','Trackbars')
        bmax = cv2.getTrackbarPos('B max','Trackbars')

        # Create a numpy array for lower bound and upper bound
        lower = np.array([bmin,gmin,rmin])
        upper = np.array([bmax,gmax,rmax])

        # Returns current position/value of trackbar 
        mask = cv2.inRange(frame,lower,upper)

        # Show the image window
        cv2.imshow('Trackbars',cv2.flip(mask,1))

        # Show the image window
        cv2.namedWindow('Video',cv2.WINDOW_NORMAL)
        cv2.imshow('Video',cv2.flip(frame,1))

        # Waitfor the user to press 'q' and break the while loop 
        key = cv2.waitKey(1) & 0xFF 

        if key == ord('q'):
            print("Quitting...") 
            break
        elif key == ord('w'):
            print('File saved with Limits!')

            dictionary = { "limits":{"B":{ "max": str(bmax) ,"min":  str(bmin)}, "G":{ "max":str(gmax),"min": str(gmin) }, "R":{ "max":str(rmax),"min": str(rmin) } }}
            with open("limits.json", "w") as file:
                json.dump(dictionary, file)

            break

    #destroys all window
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()