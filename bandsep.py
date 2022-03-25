from __future__ import print_function
import numpy as np
import cv2
import random
import argparse

random.seed(12345)
Thresh=100 #for canny edge detection

blou=[200,0,0]
raed=[0,0,200]
grien=[0,200,0]
kimg = cv2.imread("BRG.png",1)
img=cv2.resize(kimg,(700,700)) #resizing to fit window
#Note: Use this line only when running code for the first time.
#cv2.imwrite("Half.png",img)

#color separation
red = img.copy()
blue= img.copy()
green= img.copy()
height, width = img.shape[0:2]
#cv2.imshow("Original",img)

redmask=cv2.inRange(red,(0,0,30),(80,80,255))
redmask=redmask.astype('bool')

k=np.zeros([img.shape[0],img.shape[1],3],'uint8')
kh=cv2.cvtColor(k,cv2.COLOR_BGR2HSV)
#cv2.imshow("Firstsep",red)



'''for row in range(0,height):
    for col in range(0, width):
        if img[row][col][0]<80 and img[row][col][1]<80 and img[row][col][2]>85:
            red[row][col]=img[row][col]
        else:
            red[row][col]=[0,0,0]'''
'''redmask=cv2.inRange(redh,(0,100,0),(10,255,255))
redmask=redmask.astype('bool')
redmask2=cv2.inRange(redh,(170,100,0),(180,255,255))
redmask2=redmask2.astype('bool')'''
#redmaskf=redmask+redmask2

redh=cv2.cvtColor(red, cv2.COLOR_BGR2HSV)
for row in range(0,height):
    for col in range(0, width):
        if (redh[row][col][1]>=100 and redh[row][col][1]<=255) and (redh[row][col][2]>=0 and redh[row][col][2]<=255) and ((redh[row][col][0]<=10 and redh[row][col][0]>=0) or (redh[row][col][0]>=170 and redh[row][col][0]<=180)):
            continue
            #redh[row][col]=redh[row][col]
        else:
            redh[row][col]=[0.0,0.0,0.0]
#cayman=img*np.dstack((redmaskf,redmaskf,redmaskf))
#cv2.imshow("Redhsv",redh)
redmu=cv2.cvtColor(redh,cv2.COLOR_HSV2BGR)
cv2.imshow("Final Red",redmu)

for row in range(0,height):
    for col in range(0, width):
        if redmu[row][col][0]<80 and redmu[row][col][1]<80 and redmu[row][col][2]>85:
            red[row][col]=redmu[row][col]
        else:
            red[row][col]=[0,0,0]


cv2.imshow("Final",red)
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


#cv2.imshow("Red",redh_result)
bands=red+blue+green
cv2.imwrite("Bands.png",bands)
cv2.imshow("Bands",bands)
bg=cv2.cvtColor(blue, cv2.COLOR_BGR2GRAY)
blug = cv2.blur(bg, (9,9))
edges=cv2.Canny(blug,80,100)
#cv2.imshow("Edges",edges)
#bounding rectangles
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(20,20))
dilated = cv2.dilate(edges, kernel)
contours,_=cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours_poly = [None]*len(contours)
boundRect = [None]*len(contours)
for i, c in enumerate(contours):
    contours_poly[i] = cv2.approxPolyDP(c, 3, True)
    boundRect[i] = cv2.boundingRect(contours_poly[i])

objects=np.zeros([img.shape[0],img.shape[1],3],'uint8')

for c in contours:
    area=cv2.contourArea(c)
    if area>100:
        color = blou
        cv2.drawContours(objects, contours_poly, i, color)
        cv2.rectangle(objects, (int(boundRect[i][0]), int(boundRect[i][1])), \
        (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
        #print("Area: {}".format(area))
        M=cv2.moments(c)
        bx=int(M['m10']/M['m00'])
        by=int(M['m01']/M['m00'])
        #cv2.circle(objects, (bx, by), 7, (255, 255, 255), -1)
    else:
        continue


rg=cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)
rbug = cv2.blur(rg, (5,5))
edges2=cv2.Canny(rbug,80,100)
#cv2.imshow("Edges2",edges2)
#bounding rectangles
kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT,(20,20))
dilated2 = cv2.dilate(edges2, kernel2)
contours2,_=cv2.findContours(dilated2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours_poly2 = [None]*len(contours2)
boundRect2 = [None]*len(contours2)

for i, c in enumerate(contours2):
    contours_poly2[i] = cv2.approxPolyDP(c, 3, True)
    boundRect2[i] = cv2.boundingRect(contours_poly2[i])

objects2=np.zeros([img.shape[0],img.shape[1],3],'uint8')

for c in contours2:
    area=cv2.contourArea(c)
    color = raed
    cv2.drawContours(objects2, contours_poly2, i, color)
    cv2.rectangle(objects2, (int(boundRect2[i][0]), int(boundRect2[i][1])), \
    (int(boundRect2[i][0]+boundRect2[i][2]), int(boundRect2[i][1]+boundRect2[i][3])), color, 2)
    #print("Area: {}".format(area))
    M2=cv2.moments(c)
    rx=int(M2['m10']/M2['m00'])
    ry=int(M2['m01']/M2['m00'])
    #cv2.circle(objects2, (rx, ry), 7, (255, 255, 255), -1)


gg=cv2.cvtColor(green, cv2.COLOR_BGR2GRAY)
gbug = cv2.blur(gg, (9,9))
edges3=cv2.Canny(gbug,80,100)
#cv2.imshow("Edges3",edges3)
#bounding rectangles
kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT,(20,20))
dilated3 = cv2.dilate(edges3, kernel3)
contours3,_=cv2.findContours(dilated3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours_poly3 = [None]*len(contours3)
boundRect3 = [None]*len(contours3)

for i, c in enumerate(contours3):
    contours_poly3[i] = cv2.approxPolyDP(c, 3, True)
    boundRect3[i] = cv2.boundingRect(contours_poly3[i])

objects3=np.zeros([img.shape[0],img.shape[1],3],'uint8')

for c in contours3:
    area=cv2.contourArea(c)
    color = grien
    cv2.drawContours(objects3, contours_poly3, i, color)
    cv2.rectangle(objects3, (int(boundRect3[i][0]), int(boundRect3[i][1])), \
    (int(boundRect3[i][0]+boundRect3[i][2]), int(boundRect3[i][1]+boundRect3[i][3])), color, 2)
    #print("Area: {}".format(area))
    M3=cv2.moments(c)
    gx=int(M3['m10']/M3['m00'])
    gy=int(M3['m01']/M3['m00'])
    #cv2.circle(objects3, (gx, gy), 7, (255, 255, 255), -1)

'''cv2.imshow("Contours",objects)
cv2.imshow("Contours2",objects2)
cv2.imshow("Contours3",objects3)'''
bandscon=objects+objects2+objects3
cv2.imshow("Bounded Bands",bandscon)

'''if rx>bx and rx>gx:
    print("Red at top")
elif bx>rx and bx>gx:
    print("Blue at top")
elif gx>rx and gx>bx:
    print("Green at top")'''
if ry<by and ry<gy: #and abs(ry-by)<100 and abs(ry-gy)<100:
    if by<gy:
        print("RBG")
    else:
        print("RGB")
elif gy<ry and gy<by: #and abs(ry-by)<100 and abs(ry-gy)<100:
    if by<ry:
        print("GBR")
    else:
        print("GRB")
elif by<ry and by<gy: #and abs(ry-by)<100 and abs(ry-gy)<100:
    if ry<gy:
        print("BRG")
    else:
        print("BGR")
else:
    print("Object could not be found")


cv2.waitKey(0)
cv2.destroyAllWindows()