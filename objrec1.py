from __future__ import print_function
import numpy as np
import cv2
import random
import argparse

random.seed(12345)
Thresh=100

blou=[200,0,0]
raed=[0,0,200]
grien=[0,200,0]
kimg = cv2.imread("3can.png",1)
img=cv2.resize(kimg,(700,700))

red = img.copy()
blue= img.copy()
green= img.copy()
height, width = img.shape[0:2]

redmask=cv2.inRange(red,(0,0,30),(80,80,255))
redmask=redmask.astype('bool')

k=np.zeros([img.shape[0],img.shape[1],3],'uint8')
kh=cv2.cvtColor(k,cv2.COLOR_BGR2HSV)

redh=cv2.cvtColor(red, cv2.COLOR_BGR2HSV)
for row in range(0,height):
    for col in range(0, width):
        if (redh[row][col][1]>=100 and redh[row][col][1]<=255) and (redh[row][col][2]>=0 and redh[row][col][2]<=255) and ((redh[row][col][0]<=10 and redh[row][col][0]>=0) or (redh[row][col][0]>=170 and redh[row][col][0]<=180)):
            continue
        else:
            redh[row][col]=[0.0,0.0,0.0]
redmu=cv2.cvtColor(redh,cv2.COLOR_HSV2BGR)

for row in range(0,height):
    for col in range(0, width):
        if redmu[row][col][0]<60 and redmu[row][col][1]<60 and redmu[row][col][2]>115:
            red[row][col]=redmu[row][col]
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
        if img[row][col][0]<80 and img[row][col][1]>105 and img[row][col][2]<80:
            green[row][col]=img[row][col]
        else:
            green[row][col]=[0,0,0]

bg=cv2.cvtColor(blue, cv2.COLOR_BGR2GRAY)
blug = cv2.blur(bg, (3,3))
bledges=cv2.Canny(blug,80,100)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(10,10))
dilated = cv2.dilate(bledges, kernel)
contours,_=cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours_poly = [None]*len(contours)
boundRect = [None]*len(contours)
for i, c in enumerate(contours):
    contours_poly[i] = cv2.approxPolyDP(c, 3, True)
    boundRect[i] = cv2.boundingRect(contours_poly[i])

objects=np.zeros([img.shape[0],img.shape[1],3],'uint8')
bxx=[]
byy=[]
for c in contours:
    color = blou
    cv2.drawContours(objects, contours_poly, -1, color, 2)
    area=cv2.contourArea(c)
    if area>40:
        M=cv2.moments(c)
        bx=int(M['m10']/M['m00'])
        by=int(M['m01']/M['m00'])
        cv2.rectangle(objects, (int(boundRect[i][0]), int(boundRect[i][1])), \
        (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
        bxx.append(bx)
        byy.append(by)
    else:
        continue

rg=cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)
rbug = cv2.blur(rg, (3,3))
edges2=cv2.Canny(rbug,80,100)
kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT,(10,10))
dilated2 = cv2.dilate(edges2, kernel2)
contours2,_=cv2.findContours(dilated2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours_poly2 = [None]*len(contours2)
boundRect2 = [None]*len(contours2)
for i, c in enumerate(contours2):
    contours_poly2[i] = cv2.approxPolyDP(c, 3, True)
    boundRect2[i] = cv2.boundingRect(contours_poly2[i])

objects2=np.zeros([img.shape[0],img.shape[1],3],'uint8')

radx=[]
rady=[]
for c in contours2:
    color = raed
    cv2.drawContours(objects2, contours_poly2, -1, color, 2)
    area=cv2.contourArea(c)
    if area>40:
        M2=cv2.moments(c)
        rx=int(M2['m10']/M2['m00'])
        ry=int(M2['m01']/M2['m00'])
        cv2.rectangle(objects2, (int(boundRect2[i][0]), int(boundRect2[i][1])), \
        (int(boundRect2[i][0]+boundRect2[i][2]), int(boundRect2[i][1]+boundRect2[i][3])), color, 2)
        radx.append(rx)
        rady.append(ry)
    else:
        continue

gg=cv2.cvtColor(green, cv2.COLOR_BGR2GRAY)
gbug = cv2.blur(gg, (3,3))
edges3=cv2.Canny(gbug,80,100)
kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT,(10,10))
dilated3 = cv2.dilate(edges3, kernel3)
contours3,_=cv2.findContours(dilated3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours_poly3 = [None]*len(contours3)
boundRect3 = [None]*len(contours3)

for i, c in enumerate(contours3):
    contours_poly3[i] = cv2.approxPolyDP(c, 3, True)
    boundRect3[i] = cv2.boundingRect(contours_poly3[i])

objects3=np.zeros([img.shape[0],img.shape[1],3],'uint8')

grx=[]
gry=[]
for c in contours3:
    color = grien
    cv2.drawContours(objects3, contours_poly3, -1, color, 2)
    area=cv2.contourArea(c)
    if area>40:
        M3=cv2.moments(c)
        gx=int(M3['m10']/M3['m00'])
        gy=int(M3['m01']/M3['m00'])
        cv2.rectangle(objects3, (int(boundRect3[i][0]), int(boundRect3[i][1])), \
        (int(boundRect3[i][0]+boundRect3[i][2]), int(boundRect3[i][1]+boundRect3[i][3])), color, 2)
        grx.append(gx)
        gry.append(gy)
    else:
        continue

for i in range(3):
    for k in range(3):
        for m in range(3):
            if radx[m]==bxx[k] and radx[m]==grx[i]:
                if rady[m]<byy[k] and rady[m]<gry[i]:
                    if byy[k]<gry[i]:
                        print("RBG")
                    else:
                        print("RGB")
                if gry[i]<byy[k] and gry[i]<rady[m]:
                    if rady[m]<byy[k]:
                        print("GRB")
                    else:
                        print("GBR")
                if byy[k]<gry[i] and byy[k]<rady[m]:
                    if rady[m]<gry[i]:
                        print("BRG")
                    else:
                        print("BGR")

cv2.waitKey(0)
cv2.destroyAllWindows()