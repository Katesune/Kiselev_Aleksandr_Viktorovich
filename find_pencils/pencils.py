from os import listdir
import matplotlib.pyplot as plt
import numpy as np
import cv2
from skimage.filters import sobel

def getNumPencils(files):
    res = 0
    for file in files:
        res += getPencilsInFile(file)
    return res
        
def getPencilsInFile(file):
    image = cv2.imread("images/"+file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edged = cv2.Canny(gray, 0, 50)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)\
        
    cont, hier = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    total = 0
    total2=0

    for c in cont:  
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
       
        rect = cv2.minAreaRect(c) #зарисовываем в прямоугльник
        box = cv2.boxPoints(rect) 
        box = np.int0(box)
        
        if checkArea(rect, c)==True:
            #смотрим, проходит ли контур по параметрам площади
            total+=1
            
    # im = cv2.resize(image, (350, 500))  
    # cv2.imshow("closed.jpg", im)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return total

def checkArea(rect, c):
    area1 = int(rect[1][0]*rect[1][1])
    area2 = cv2.contourArea(c)
    
    if area1>350000 and area1<660000:
        if area2<392000:
            #cv2.drawContours(image,[box],0,(255,0,0),8) 
            return True
    return False


files = listdir("images")
result = getNumPencils(files)
print(result)
