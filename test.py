import cv2
import numpy as np
import math
import detection.config as config

# this script is to test the detection region parameters so you can set up
# the configuration according to your background

"""
    detection region is the region of frame capture where we actually
    detect the contours. Based on your background, screen size, where and
    how you're sitting in front of your screen you might actually want to
    change the detection region boundaries. Changing the values on the trackbar
    edits the configuration file so you can setup the values for the real file
    which just reads the configuration to setup

    SUB_START_X - the x-axis value of the top left point of the detection region
    SUB_START_Y - the y-axis value of the top left point of the detection region
    SUB_END_X - the x-axis value of the bottom right point of the detection region
    SUB_END_Y - the y-axis value of the bottom right point of the detection region

    MAX_AREA - defines the max permissible area, this to avoid reading larger areas
                such as walls when there's nothing in the region (no hand)

"""

# get configuration data from config file
SUB_START_X = int(config.getConfig('config', 'SUB_START_X'))
SUB_START_Y = int(config.getConfig('config', 'SUB_START_Y'))
SUB_END_X = int(config.getConfig('config', 'SUB_END_X'))
SUB_END_Y = int(config.getConfig('config', 'SUB_END_Y'))
MAX_AREA = int(config.getConfig('config', 'MAX_AREA'))

# initialize camera
capture = cv2.VideoCapture(0)

while(True):

    # read frame
    ret, frame = capture.read()

    # get cropped area (detection region)
    cv2.rectangle(frame, (SUB_START_X,SUB_START_Y), (SUB_END_X,SUB_END_Y), (0,255,0), 0)
    detection_region = frame[SUB_START_X:SUB_END_X, SUB_START_Y:SUB_END_Y]

    # get detection region's grayscale and apply GaussianBlur, 35 is the standard
    # deviation of the gaussian kernel
    detection_gray = cv2.cvtColor(detection_region, cv2.COLOR_BGR2GRAY)
    detection_blur = cv2.GaussianBlur(detection_gray, (35, 35), 0)

    # using Otsu's thresholding at center of the 8-bit scale
    _, detection_thresh = cv2.threshold(detection_blur, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    cv2.imshow('detection_threshold', detection_thresh)

    # find all Contours
    _, contours, hierarchy = cv2.findContours(detection_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # find max area index, the area should be less than MAX_AREA though
    max_area = 200
    ci = 0
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        if(area > max_area and area < MAX_AREA):
            max_area = area
            ci = i

    # Largest area contour
    try:
        cnts = contours[ci]
    except IndexError:
        cnts = 0

    # find convex hull for largest area countour
    hull = cv2.convexHull(cnts)

    # drawing contours for debugging
    detection_draw = np.zeros(detection_region.shape,np.uint8)
    cv2.drawContours(detection_draw, [cnts], 0, (0, 255, 0), 0)
    cv2.drawContours(detection_draw, [hull], 0,(0, 0, 255), 0)

    # find convex hull for largest area countour with no returnPoints
    hull = cv2.convexHull(cnts, returnPoints=False)

    # find convexity defects
    defects = cv2.convexityDefects(cnts, hull)
    count_defects = 0
    cv2.drawContours(detection_thresh, contours, -1, (0, 255, 0), 3)

    # use cosine rule to check for angles between fingers
    if type(defects) != type(None):
        count_defects += 1
        for i in range(defects.shape[0]):
            start_def, end_def, mid_def, d = defects[i,0]

            start = tuple(cnts[start_def][0])
            end = tuple(cnts[end_def][0])
            mid = tuple(cnts[mid_def][0])

            # start, mid and end make a triangle (btw fingers), only register
            # if angle between sides from finger centers to finger tips is less
            # than 90
            # side_b and side_c are fingera
            side_a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            side_b = math.sqrt((mid[0] - start[0])**2 + (mid[1] - start[1])**2)
            side_c = math.sqrt((end[0] - mid[0])**2 + (end[1] - mid[1])**2)

            # get angle, convert to degrees
            fin_angle = math.acos((side_b**2 + side_c**2 - side_a**2)/(2*side_b*side_c)) * 57

            # ignore angles > 90
            if fin_angle <= 90:
                count_defects += 1
                cv2.circle(detection_region, mid, 1, [0,0,255], -1)

            # draw a line from start to end
            cv2.line(detection_region,start, end, [0,255,0], 2)

    cv2.putText(frame, count_defects.__str__(), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)

    # show images
    cv2.imshow('test-display', frame)
    test = np.hstack((detection_draw, detection_region))
    cv2.imshow('test.py', test)

    k = cv2.waitKey(5)
    if k == 27:
        break
