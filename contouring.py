import numpy as np
import cv2
import random

img = cv2.imread("BGP.png",1)
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges=cv2.Canny(img,50,300)

thresh=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,175,1)
#cv2.imshow("Binary",thresh)
sumimg=thresh-edges

edges2=cv2.Canny(sumimg,50,200)
difimg=sumimg-edges2
edges3=cv2.Canny(difimg,30,200)
dmg=difimg-edges3
edges4=cv2.Canny(dmg,30,200)
dmh=dmg-edges4
#cv2.imshow("Canny",edges4)
edges5=cv2.Canny(dmh,30,200)
dmi=dmh-edges5
edges6=cv2.Canny(dmi,40,200)
dmj=dmi-edges6
contours, hierarchy = cv2.findContours(dmj,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
print(len(contours))
cv2.imshow("Diff",dmj)
filtered=[]
for c in contours:
    if cv2.contourArea(c)<100:continue
    filtered.append(c)

print(len(filtered))

objects=np.zeros([img.shape[0],img.shape[1],3],'uint8')
for c in filtered:
    col=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    cv2.drawContours(objects,[c],-1,col,-1)
    area=cv2.contourArea(c)
    p=cv2.arcLength(c,True)
    print(area,p)

cv2.imshow("Contours",objects)

cv2.waitKey(0)
cv2.destroyAllWindows()