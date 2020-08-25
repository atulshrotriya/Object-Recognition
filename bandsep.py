import numpy as np
import cv2
import random

img = cv2.imread("RBG.png",1)
red = img.copy()
blue= img.copy()
green= img.copy()
height, width = img.shape[0:2]
cv2.imshow("Original",img)

for row in range(0,height):
    for col in range(0, width):
        if img[row][col][0]<80 and img[row][col][1]<80 and img[row][col][2]>125:
            red[row][col]=img[row][col]
        else:
            red[row][col]=[0,0,0]

for row in range(0,height):
    for col in range(0, width):
        if img[row][col][0]>85 and img[row][col][1]<80 and img[row][col][2]<80:
            blue[row][col]=img[row][col]
        else:
            blue[row][col]=[0,0,0]

for row in range(0,height):
    for col in range(0, width):
        if img[row][col][0]<80 and img[row][col][1]>125 and img[row][col][2]<80:
            green[row][col]=img[row][col]
        else:
            green[row][col]=[0,0,0]

cv2.imshow("Red",red)
cv2.imshow("Blue",blue)
cv2.imshow("Green",green)

bands=red+blue+green
cv2.imshow("Bands",bands)

cv2.waitKey(0)
cv2.destroyAllWindows()