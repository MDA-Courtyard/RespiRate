# -*- coding: utf-8 -*
# Copyright (C) 2017 Ashlar Ruby
# Licensed under the MIT license. See COPYING.md for details.

import numpy as np
import cv2
import matplotlib as mpl


"""
Various instructions for handling the external OpenCV windows.
"""


class frameReader:
    '''
    Read frames from a video, with options to display,
    deinterlace, and rectify the images.
    '''
    def __init__(self, videoFile, **kwargs):
        self.video = cv2.VideoCapture(videoFile)
        self.videoFile = videoFile

        if not self.video.isOpened():
            print('Error opening video file!')

        # Set this to False if you don't want to display frames on-screen
        self.show = False

        for key, value in kwargs.items():
            setattr(self, key, value)

    def getFrame(self, number):
        self.video.set(1, number)
        img = self.video.read()[1]

        if self.show:
            if img.dtype == np.dtype('uint8') or np.dtype('int32'):
                norm = 1
            else:
                norm = 255.

            cv2.imshow(self.videoFile, img / norm)

        return img

    def t2f(self, minutes, seconds):
        return round(self.video.get(5)) * (60 * minutes + seconds)

# ------------------------------------------------------------------------------


clickPoints = []


def contour(image):
    '''Draw a contour on a grayscale image using mouse clicks.'''

    global clickPoints
    clickPoints = []
    winName = 'Click the outline of your ROI:'
    image = np.uint8(image)
    clone = image.copy()

    # Mouse callback function for OpenCV display window
    def click(event, x, y, flags, params):
        global clickPoints

        # Left click draws a point and a line connecting the previous point
        if event == cv2.EVENT_LBUTTONDOWN:
            clickPoints.append((x, y))
            cv2.circle(image, clickPoints[-1], 4, (0, 0, 255))

            if len(clickPoints) >= 2:
                cv2.line(image, clickPoints[-2], clickPoints[-1], (0, 0, 255))

            cv2.imshow(winName, image)
            cv2.waitKey(1)

        # Right click draws a line from the previous point to the first point,
        # closing the contour
        elif event == cv2.EVENT_RBUTTONDOWN:
            cv2.line(image, clickPoints[0], clickPoints[-1], (0, 0, 255))
            clickPoints.append(clickPoints[0])
            cv2.imshow(winName, image)
            cv2.waitKey(1)

    cv2.namedWindow(winName)
    cv2.setMouseCallback(winName, click)

    # Continuously refresh the image while looking for mouse and keyboard input
    while True:
        cv2.imshow(winName, image)
        key = cv2.waitKey(1)

        # Press 'u' to remove the previous point and line
        if key == ord('u'):
            if len(clickPoints) == 0:
                continue

            image = clone.copy()
            del clickPoints[-1]

            for p in clickPoints:
                cv2.circle(image, p, 4, (0, 0, 255))

            for p1, p2 in zip(clickPoints[:-1], clickPoints[1:]):
                cv2.line(image, p1, p2, (0, 0, 255))

        # Press 'r' to remove all points and line
        elif key == ord('r'):
            image = clone.copy()
            clickPoints = []

        # Press 'q' to quit
        elif key == ord('q'):
            return np.array(clickPoints)

# -----------------------------------------------------------------------------


def insideContour(outline, image):
    '''Find all pixels inside a contour.'''

    path = mpl.path.Path(outline)
    x, y = np.meshgrid(range(image.shape[1]), range(image.shape[0]))
    points = np.vstack((x.reshape((1, -1)), y.reshape((1, -1)))).T
    isInside = path.contains_points(points).reshape(image.shape[:2])

    return np.uint8(isInside)
