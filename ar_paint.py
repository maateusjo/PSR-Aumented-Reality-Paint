#!/usr/bin/env python3
# ----------------------------------------------------
# Mateus Araujo (116290) e Rafael Mendes (116336)
# PSR Aumented Reality Paint, December 2022
# ----------------------------------------------------

import cv2 
import argparse
import time
import json
import math

import numpy as np

from copy import deepcopy
from PIL import Image

# Window size
height, width = 640, 360

# Variable Initialization
drawing_window = []
color = (0, 0, 255)
drawing = np.array([[0,0,0,0]])
coordX = []
coordY = []
pencil_thickness = 5
flag = False
flag_square = False
squareDiagonal = False
cont = False
cont2 = False
x_aux = -1
y_aux = -1
x_aux2 = -1
y_aux2 = -1

canva = []

timeDay = time.ctime().replace(' ','_')
fileName = 'drawing_' + str(timeDay) + '.png'

def use_mouse(event,x,y,flags,userdata):

    global drawing_window, color, flag

    key = cv2.waitKey(1) & 0xFF
    
    # Press 'r' to change color to red
    if key == ord('r'):
        color = (0, 0, 255)
        print("Pencil color changed to RED")
    # Press 'g' to change color to green
    elif key == ord('g'):
        color = (0, 255, 0)
        print("Pencil color changed to GREEN")
    # Press 'b' to change color to blue
    elif key == ord('b'):
        color = (255, 0, 0)
        print("Pencil color changed to BLUE")

    # Left click to draw
    if event == cv2.EVENT_LBUTTONDOWN:
        if flag == True:
            flag = False
        else:
            flag = True
            del coordX[:]
            del coordY[:]

    # Mouse movement detection to draw
    if event == cv2.EVENT_MOUSEMOVE:
        if flag and color != (0,0,0):
            coordX.append(x)
            coordY.append(y)
            for n in range(0,len(coordX)-1):
                x1 = coordX[n]
                y1 = coordY[n]
                x2 = coordX[n+1]
                y2 = coordY[n+1]
                cv2.line(drawing_window, (x1,y1), (x2,y2), color, pencil_thickness)


def draw(x, y, frame, shakePrevention, video, numberPainting):
    
    global color, fileName, coordX, coordY, pencil_thickness, squareDiagonal, x_aux, y_aux, cont, cont2, drawing_window, flag_square, x_aux2, y_aux2

    key = cv2.waitKey(1) & 0xFF
    
    # Press 'r' to change color to red
    if key == ord('r'):
        color = (0, 0, 255)
        print("Pencil color changed to RED")
    # Press 'g' to change color to green
    elif key == ord('g'):
        color = (0, 255, 0)
        print("Pencil color changed to GREEN")
    # Press 'b' to change color to blue
    elif key == ord('b'):
        color = (255, 0, 0)
        print("Pencil color changed to BLUE")
    # Press '+' to increase pencil size
    elif key == ord('+'):
        if pencil_thickness < 50:
            pencil_thickness = pencil_thickness + 5
            print("Pencil size INCREASED: ", pencil_thickness)
        else:
            print("Pencil reached MAXIMUM SIZE")
    # Press '-' to decrease pencil size
    elif key == ord('-'):
        if pencil_thickness > 5:
            pencil_thickness = pencil_thickness - 5
            print("Pencil size DECREASED: ", pencil_thickness)
        else:
            print("Pencil reached MINIMUM SIZE")
    # Press 'c' to clear the Whiteboard
    elif key == ord('c'):
        if numberPainting == True:
            print("Whiteboard CLEARED")
            drawing_window = cv2.imread('ball.jpg')
        else:
            print("Whiteboard CLEARED")
            frame.fill(255)
    # Press 'w' to save the canvas
    elif key == ord('w'):
        if numberPainting == True:
            print("Whiteboard SAVED")
            cv2.imwrite('ball_test.jpg', drawing_window)
        else:
            print("Whiteboard SAVED")
            cv2.imwrite(fileName, frame)

    frame_aux = deepcopy(frame)

    # Press 's' to draw a Square on canvas
    if key == ord('s'):
        squareDiagonal = True
        x_aux = x
        y_aux = y
        if squareDiagonal == True:
            cv2.rectangle(frame_aux, (int(x_aux),int(y_aux)), (int(x), int(y)), color, pencil_thickness)
            cont = True
    elif not key == ord('s'):
        if cont == True:
            cv2.rectangle(frame_aux, (int(x_aux),int(y_aux)), (int(x), int(y)), color, pencil_thickness)
            squareDiagonal = False
            if key == ord('f'):
                cont = False
                drawing_window = deepcopy(frame_aux)

    # Press 'e' to draw a Square on canvas
    if key == ord('e'):
        radius = True
        x_aux2 = x
        y_aux2 = y
        if radius == True:
            cv2.circle(frame_aux, (int(x_aux2),int(y_aux2)), int(math.dist(((x_aux2,y_aux2)),(x,y))), color, pencil_thickness)
            cont2 = True
    elif not key == ord('e'):
        if cont2 == True:
            cv2.circle(frame_aux, (int(x_aux2),int(y_aux2)), int(math.dist(((x_aux2,y_aux2)),(x,y))), color, pencil_thickness)
            radius = False
            if key == ord('f'):
                cont2 = False
                drawing_window = deepcopy(frame_aux)

    # X and Y coordinates of the pencil
    coordX.append(x)
    coordY.append(y)
    
    if len(coordX) > 1 and len(coordY) > 1:
        x1 = int(coordX[len(coordX) - 2])
        y1 = int(coordY[len(coordY) - 2])

        x2 = int(coordX[len(coordX) - 1])
        y2 = int(coordY[len(coordY) - 1])

        # Shake prevention mechanism
        if shakePrevention:
            if math.dist((x1,y1),(x2,y2)) < 50:
                if cont == False and cont2 == False:
                    cv2.line(frame,(x1,y1),(x2,y2),color,pencil_thickness)
        # Video paint mechanism (Not working properly)
        elif video:
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2BGRA)
            gui_image_h,gui_image_w,gui_image_c = frame.shape
            for i in range(0,gui_image_h):
                for j in range(0,gui_image_w):
                    if frame[i,j][3] != 255:
                        frame[i,j] = frame[i,j]
            cv2.imshow('AR Video Paint',frame)
        elif cont == True or cont2 == True:
            cv2.imshow('AR Paint Whiteboard', cv2.flip(frame_aux,1))
        else:
            cv2.line(frame,(x1,y1),(x2,y2),color,pencil_thickness)
            
        if not squareDiagonal:
            cv2.imshow('AR Paint Whiteboard', cv2.flip(frame_aux,1))
        else:
            cv2.imshow('AR Paint Whiteboard', cv2.flip(drawing_window,1))


def setupBGR(path):
    
    # Read JSON file
    with open(path) as jsonFile:
        data = json.load(jsonFile)

        # Get BGR values
        B = {'min': int(data['limits']['B']['min']), 'max': int(data['limits']['B']['max'])}
        G = {'min': int(data['limits']['G']['min']), 'max': int(data['limits']['G']['max'])}
        R = {'min': int(data['limits']['R']['min']), 'max': int(data['limits']['R']['max'])}
        
        jsonFile.close()

    return B, G, R


def inicialization():

    global drawing_window

    # Argument parser
    parser = argparse.ArgumentParser(description='PSR Aumented Reality Paint | Mateus Araujo e Rafael Mendes')
    parser.add_argument('-j','--json', type=str, required=True, 
                        help='JSON File with RGB settings.')
    parser.add_argument('-usp','--use_shake_prevention', action='store_true', 
                        help='Use shake Prevention Mode')
    parser.add_argument('-m','--mouse', action='store_true', 
                        help='Mouse Use Mode')
    parser.add_argument('-v','--video',action='store_true', 
                        help='Use video mode')
    parser.add_argument('-n','--number_painting', action='store_true', 
                        help='Use zone mode')

    args = vars(parser.parse_args())

    pathJson = args['json']
    shakePrevention = args['use_shake_prevention']
    mouse = args['mouse']
    video = args['video']
    numberPainting = args['number_painting']

    # Gets B G R settings of JSON file
    B, G, R = setupBGR(pathJson)

    # Capture video from webcam
    vid = cv2.VideoCapture(0)

    if numberPainting == False:
        # Creating Whiteboard
        drawing_window = np.zeros((width,height,4))
        drawing_window.fill(255)
    else:
        drawing_window = cv2.imread('ball.jpg')
        print()

    return B, G, R, vid, shakePrevention, mouse, video, numberPainting


def main():

    global drawing_window

    B, G, R, vid, shakePrevention, mouse, video, numberPainting = inicialization()

    # Creating windows 
    cv2.namedWindow('AR Paint', cv2.WINDOW_NORMAL)
    cv2.namedWindow('AR Paint Segmented',cv2.WINDOW_NORMAL)
    cv2.namedWindow('AR Paint Whiteboard', cv2.WINDOW_NORMAL)

    while True:

        # Get keyboard input
        key = cv2.waitKey(1) & 0xFF

        # Get frame from webcam
        _, frame = vid.read()
        frame = cv2.resize(frame, (height, width)) 

        # Get segementation limits of BGR
        segmented = cv2.inRange(frame,(B['min'],G['min'],R['min']), (B['max'],G['max'],R['max']))

        # Connected Components
        connectivity = 4
        output = cv2.connectedComponentsWithStats(segmented, connectivity, cv2.CV_32S)

        # Get the results
        num_labels = output[0]
        stats = output[2]
        centroids = output[3]

        # Shake prevention and Mouse MODES
        if shakePrevention and mouse == True:
            cv2.setMouseCallback('AR Paint Whiteboard',use_mouse)
        # Otherwise, use the Normal MODE
        else:
            # Loop over the number of labels
            for k in range(1,num_labels):
                
                # Deepcopy of frame
                frame_copy = deepcopy(frame)
                
                # Identify the area of each object
                area = stats[k, cv2.CC_STAT_AREA]

                # Limit the are of the object
                if area < 150:
                    continue
                
                # Coordinates of the rectangle
                rect_x = stats[k, cv2.CC_STAT_LEFT] 
                rect_y = stats[k, cv2.CC_STAT_TOP] 

                # Width and height of the object
                width_c = stats[k, cv2.CC_STAT_WIDTH] 
                height_c = stats[k, cv2.CC_STAT_HEIGHT]

                # Rectangle corners
                rect_corner1 = (rect_x, rect_y)
                rect_corner2 = (rect_x + width_c, rect_y + height_c)

                # Centroid coordinates
                centroid_x, centroid_y = centroids[k]
                
                # Draw rectangle
                cv2.rectangle(frame_copy,rect_corner1,rect_corner2,(100, 255, 100), 1) 
                
                # Draw centroid cross
                cv2.line(frame_copy,(int(centroid_x)-2,int(centroid_y)+2),(int(centroid_x)+2,int(centroid_y)-2),color,1)
                cv2.line(frame_copy,(int(centroid_x)-2,int(centroid_y)-2),(int(centroid_x)+2,int(centroid_y)+2),color,1)

                # Show frame
                cv2.imshow('AR Paint', cv2.flip(frame_copy,1))
                
                if video == True:
                    draw(centroid_x, centroid_y, frame_copy, shakePrevention, video, numberPainting)
                else:
                    draw(centroid_x, centroid_y, drawing_window, shakePrevention, video, numberPainting)
                
        # Show segmented frame
        cv2.imshow('AR Paint Segmented', cv2.flip(segmented,1))

        if shakePrevention and mouse == True:
            cv2.imshow('AR Paint Whiteboard', drawing_window)        

        # Press 'q' to exit
        if key == ord('q'):
            break
        # Press 't' to evaluate the painting
        elif key == ord('t'):

            # Save the painting
            image1 = Image.open("ball_painted.jpg")
            image2 = Image.open("ball_test.jpg")

            # Convert the images to grayscale
            image1 = image1.convert("L")
            image2 = image2.convert("L")

            # Get the width and height of the images
            w_test, h_test = image1.size

            # Set the counter for the number of matching pixels
            correct_pixels = 0

            # Loop through the pixels of the images
            for x in range(w_test):
                for y in range(h_test):

                    # Get the pixel values at (x, y)
                    pixel1 = image1.getpixel((x, y))
                    pixel2 = image2.getpixel((x, y))

                    if pixel1 == pixel2:
                        correct_pixels = correct_pixels + 1

            # Calculate the percentage of correct painting
            percent_correct = (correct_pixels / (w_test * h_test)) * 100

            # Print the percentage of correct painting
            print("Percent correct: {:.2f}%".format(percent_correct))        

    # Destroys all window
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()