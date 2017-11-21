import cv2
import numpy as np
import math
import detection.config as config

FREQ_THRESHOLD = 50

# returns finger count
def getCount(size):
    # size is used to define the array size which stores the last few counts
    # this is to improve accuracy

    # initialize camera
    capture = cv2.VideoCapture(0)

    result = 0

    # initialize array to keep detected values
    countArray = []
    for i in range(size):
        countArray.append(result)

    # setup the parameters configured in test.py
    SUB_START_X = int(config.getConfig('config', 'SUB_START_X'))
    SUB_START_Y = int(config.getConfig('config', 'SUB_START_Y'))
    SUB_END_X = int(config.getConfig('config', 'SUB_END_X'))
    SUB_END_Y = int(config.getConfig('config', 'SUB_END_Y'))
    MAX_AREA = int(config.getConfig('config', 'MAX_AREA'))
    MIN_AREA = int(config.getConfig('config', 'MIN_AREA'))

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

        # find all Contours
        _, contours, hierarchy = cv2.findContours(detection_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        # find max area index, the area should be less than MAX_AREA though
        max_area = MIN_AREA
        ci = 0
        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            if (area > max_area and area < MAX_AREA):
                max_area = area
                ci = i

        # Largest area contour
        try:
            cnts = contours[ci]
        except IndexError:
            cnts = 0

        count_defects = 0

        if (max_area > MIN_AREA and max_area < MAX_AREA):
            # find convex hull for largest area countour
            hull = cv2.convexHull(cnts)

            # find convex hull for largest area countour with no returnPoints
            hull = cv2.convexHull(cnts, returnPoints=False)

            # find convexity defects
            defects = cv2.convexityDefects(cnts, hull)
            count_defects = 0

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

        # add count_defects to countArray
        countArray.append(count_defects)
        countArray.pop(0)

        # check for most frequent value
        if (np.bincount(countArray).argmax() != 0):
            unique_elements, counts_elements = np.unique(countArray, return_counts=True)
            i = 0
            while(unique_elements[i] != np.bincount(countArray).argmax()):
                i += 1

            if ((counts_elements[i] / len(countArray)) > FREQ_THRESHOLD/100):
                break


        k = cv2.waitKey(5)
        if k == 27:
            break

    # return final value
    return np.bincount(countArray).argmax()

# just to test
# while(True):
#     res = getCount(5)
#     print(res)
