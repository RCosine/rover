import cv2
import numpy as np

def thresholding(image):
    imgHsv = cv2.cutColor(img,cvs.COLOR_BGR2HSV)
    lowerWhite = np.array([0,0,0])
    upperWhite = np.array([179,255,255])
    maskWhite = cv2.inRange(imgHsv,lowerWhite,upperWhite)
    return maskWhite