import matplotlib.pyplot as plt
import numpy as np
import cv2

flimit = 250
slimit = 255

def drawRectAbove(c, image):
     rect = cv2.minAreaRect(c) 
     box = cv2.boxPoints(rect) 
     box = np.int0(box)
     cv2.drawContours(image,[box],0,(0,0,255),8)
     
def changeAlph(gray):
    
    new_gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edged = cv2.Canny(new_gray, 100, 50)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    
    return closed
     
def fupdate(value):
    global flimit
    flimit = value
    
def subdate(value):
    global slimit 
    slimit = value

cam = cv2.VideoCapture(0)

cv2.namedWindow('Camera', cv2.WINDOW_KEEPRATIO)
cv2.namedWindow('Mask', cv2.WINDOW_KEEPRATIO)
cv2.namedWindow('Paper', cv2.WINDOW_KEEPRATIO)

cv2.createTrackbar("F", "Mask", flimit, 255, fupdate)
cv2.createTrackbar("S", "Mask", flimit, 255, fupdate)

kernel = np.ones((15, 15))

while cam.isOpened():
    ret, frame = cam.read()
    converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    mask = cv2.inRange(converted, np.array([20, flimit, 0]), np.array([160, slimit, 100])) 

    mask = cv2.erode(mask, kernel)
    mask = cv2.dilate(mask, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.GaussianBlur(mask, (3, 3), 0)
    
    countours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    if len(countours)>0:
        paper = max(countours, key=cv2.contourArea)
        rect = cv2.minAreaRect(paper)
        box = cv2.boxPoints(rect)
        box_x = []
        box_y = []
        for p in box:
            cv2.circle(frame, tuple(p), 6, (0, 0, 255), 2)
            box_x.append(int(p[0]))
            box_y.append(int(p[1]))
            if box_x:
                paper_image = frame[min(box_y):max(box_y), min(box_x):max(box_x)]

                if paper_image.size > 0:
                     print(paper)
                     drawRectAbove(paper, frame)
                     #cv2.drawContours(frame,[paper],0,(0,0,255),8)
                     cv2.imshow("Paper", paper_image)
    
    #     hull = cv2.convexHull(paper)
    #     for i in range(1, len(hull)):
    #         cv2.line(frame, tuple(*hull[i-1]), tuple(*hull[i]), (0, 255, 0), 2)
    #     cv2.line(frame, tuple(*hull[i-1]), tuple(*hull[i]), (0, 255, 0), 2)
        
        #cv2.drawContours(frame, [paper], -1, (0, 255,0), 3)
    
    cv2.imshow('Camera', frame)
    cv2.imshow('Mask', mask)
    key = cv2.waitKey(1)
    if key == ord('p'):
        print("Take screenshot")
        cv2.imwrite("screen.png", mask)
        cv2.imwrite("new.png", frame)
        
    if key == ord('q'):
        break
    
cam.release()
cv2.destroyAllWindows()
