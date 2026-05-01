import numpy as np
import cv2
import imutils
from skimage.filters import threshold_local
from perspectivetransform import four_point_transform
def documentScanner(imgFilepath):
    print("THIS IMAGE FILE PATHL:",imgFilepath)
    image = cv2.imread(imgFilepath)
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height = 500)

    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(5,5),0)
    thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]


    cnts,_ = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    area_thresh=0
    for c in cnts:
        area = cv2.contourArea(c)

        if area > area_thresh:
            area_thresh= area
            big_countour = c
    peri= cv2.arcLength(big_countour,True)
    corners = cv2.approxPolyDP(big_countour,0.02*peri,True)

    warped=four_point_transform(orig,corners.reshape(4,2)*ratio)
    warped = cv2.cvtColor(warped,cv2.COLOR_BGR2GRAY)
    T= threshold_local(warped, 11 , offset=10 , method= "gaussian")
    warped = (warped >T).astype("uint8") * 255

    return warped
if __name__ == "__main__":
    doc=documentScanner("IMG_20260430_130908.jpg")
    
    cv2.imshow("LABRADOR",doc)
    cv2.waitKey(0)