import matplotlib.pyplot as plt
import numpy as np
import cv2

flimit = 250
slimit = 255


def changeImg(gray):
    
    new_gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edged = cv2.Canny(new_gray, 100, 50)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(edged, cv2.MORPH_GRADIENT, kernel)
    
    return closed

def getTemplate(image):
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    template = changeImg(image_gray)
    return template


def drawContourTemplate(template, screen):
    conts, hier = cv2.findContours(template, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in conts:
        peri = cv2.arcLength(c, True)
        print("peri", peri)
        if peri > 900 and peri < 1200:
            drawRectAbove(c, screen)
            return c
        #cv2.drawContours(screen, conts, -1, (0, 255,0), 3)
    
def drawRectAbove(c, image):
     rect = cv2.minAreaRect(c) 
     box = cv2.boxPoints(rect) 
     box = np.int0(box)
     cv2.drawContours(image,[box],0,(0,0,255),8)
     
def fupdate(value):
    global flimit
    flimit = value
    
def subdate(value):
    global slimit 
    slimit = value
    
def createWindows():
    cv2.namedWindow('Camera', cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow('Mask', cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow('Image', cv2.WINDOW_KEEPRATIO)
    
    cv2.createTrackbar("F", "Mask", flimit, 255, fupdate)
    cv2.createTrackbar("S", "Mask", flimit, 255, fupdate)
    
    kernel = np.ones((15, 15))
    
cam = cv2.VideoCapture(0)

#загружаем скриншот образца нашего изображения и ищем нужный контур
screen = cv2.imread("template.png")
template = getTemplate(screen)
frog_cont = drawContourTemplate(template, screen) 
print(frog_cont)

createWindows()

low_res = 0.1

while cam.isOpened():
    ret, frame = cam.read()
    mask = getTemplate(frame)
    conts1, hier = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in conts1:
        frame_with_im = frame
        
        res = cv2.matchShapes(frog_cont,c,cv2.CONTOURS_MATCH_I1,1)
        peri = cv2.arcLength(c, True)
        
        if res<low_res and peri > 700:
            print("Find my image")
            print(res)
            drawRectAbove(c, frame_with_im)
            
    
    # if len(conts1)>0:
    #     paper = max(conts1, key=cv2.contourArea)
    #     rect = cv2.minAreaRect(paper)
    #     box = cv2.boxPoints(rect)
    #     box_x = []
    #     box_y = []
    #     for p in box:
    #         cv2.circle(frame, tuple(p), 6, (0, 0, 255), 2)
    #         box_x.append(int(p[0]))
    #         box_y.append(int(p[1]))
    #         if box_x:
    #             paper_image = frame[min(box_y):max(box_y), min(box_x):max(box_x)]

    #             if paper_image.size > 0:
    #                  drawRectAbove(paper, frame)
    #                  #cv2.drawContours(frame,[paper],0,(0,0,255),8)
    #                  cv2.imshow("Paper", paper_image)
                     
                     
    cv2.imshow('Camera', frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('Image', frame_with_im)
   
    key = cv2.waitKey(1)
    if key == ord('p'):
        print("Take screenshot")
        cv2.imwrite("screen.png", mask)
        cv2.imwrite("new.png", frame)
            
    if key == ord('q'):
        break
    
cam.release()
cv2.destroyAllWindows()
