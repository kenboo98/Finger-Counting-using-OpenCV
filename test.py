import cv2
import numpy as np
import math
import detection.config as config

# this script is to test the detection region parameters so you can set up
# the configuration according to your background

"""
    Use the trackbar to play around and set values

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

    these limits are necessary to omit background defects

    MAX_AREA - the biggest size of contour that should be detectable
    MIN_AREA - the smallest size of contour that should be detectable

"""
class params():

    # get configuration data from config file
    SUB_START_X = int(config.getConfig('config', 'SUB_START_X'))
    SUB_START_Y = int(config.getConfig('config', 'SUB_START_Y'))
    SUB_END_X = int(config.getConfig('config', 'SUB_END_X'))
    SUB_END_Y = int(config.getConfig('config', 'SUB_END_Y'))
    MAX_AREA = int(config.getConfig('config', 'MAX_AREA'))
    MIN_AREA = int(config.getConfig('config', 'MIN_AREA'))

    def setStartX(self, val):
        self.SUB_START_X = int(val)
        config.writeConfig('config', 'SUB_START_X', val)

    def setStartY(self, val):
        self.SUB_START_Y = int(val)
        config.writeConfig('config', 'SUB_START_Y', val)

    def setEndX(self, val):
        self.SUB_END_X = int(val)
        config.writeConfig('config', 'SUB_END_X', val)

    def setEndY(self, val):
        self.SUB_END_Y = int(val)
        config.writeConfig('config', 'SUB_END_Y', val)

    def setMaxArea(self, val):
        self.MAX_AREA = int(val)
        config.writeConfig('config', 'SUB_MAX_AREA', val)

    def setMinArea(self, val):
        self.MIN_AREA = int(val)
        config.writeConfig('config', 'SUB_MIN_AREA', val)

config_params = params()

cv2.namedWindow('Testing')
cv2.createTrackbar('start_x', 'Testing', config_params.SUB_START_X, 625, config_params.setStartX)
cv2.createTrackbar('start_y', 'Testing', config_params.SUB_START_Y, 500, config_params.setStartY)
cv2.createTrackbar('end_x', 'Testing', config_params.SUB_END_X, 1350, config_params.setEndX)
cv2.createTrackbar('end_y', 'Testing', config_params.SUB_END_Y, 720, config_params.setEndY)
cv2.createTrackbar('max_area', 'Testing', config_params.MAX_AREA, 350000, config_params.setMaxArea)
cv2.createTrackbar('min_area', 'Testing', config_params.MIN_AREA, 20000, config_params.setMinArea)

# initialize camera
capture = cv2.VideoCapture(0)

while(True):

    # read frame
    ret, frame = capture.read()

    # get cropped area (detection region)
    cv2.rectangle(frame, (config_params.SUB_START_X,config_params.SUB_START_Y), \
        (config_params.SUB_END_X,config_params.SUB_END_Y), (0,255,0), 0)
    detection_region = frame[config_params.SUB_START_X:config_params.SUB_END_X, \
    config_params.SUB_START_Y:config_params.SUB_END_Y]

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
    max_area = 10000
    ci = 0
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        if(area > max_area and area < 170000):
            max_area = area
            print(max_area)
            ci = i
            print(ci)

    # Largest area contour
    try:
        cnts = contours[ci]
    except IndexError:
        cnts = 0

    detection_draw = np.zeros(detection_region.shape,np.uint8)
    count_defects = 0

    if(max_area > 10000 and max_area < 170000):
        # find convex hull for largest area countour
        hull = cv2.convexHull(cnts)

        # drawing contours for debugging
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
