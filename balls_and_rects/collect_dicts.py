import matplotlib.pyplot as plt
import numpy as np
import cv2

def changeImg(gray):
    
    new_gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edged = cv2.Canny(new_gray, 10, 100, 5)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    closed = cv2.morphologyEx(edged, cv2.MORPH_GRADIENT, kernel)
    
    return closed

def getKey(color):
    
    key = str(color[0])+" " + str(color[1])+" " + str(color[2])
    return key
    
def getObject(c):
    
     my_obj[1],my_obj[0] = c[0][0][0], c[0][0][1]
     return my_obj
 
def isRect(contour):
    
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
    
    if(len(approx)==4):
        return True
    
    return False

def addKeyInDict(dict_colors, key):
    
    if (dict_colors.get(key)!=None):
            dict_colors[key] += 1
    else:
            dict_colors[key] = 1
            
    return dict_colors

def getDicts(contours, image):
    
    balls_colors ={}
    rects_colors = {}
    
    for contour in contours:
        
        my_obj = getObject(contour)
        my_color = image[my_obj[0]][my_obj[1]]
        
        key = getKey(my_color) 
        
        if isRect(contour)==True:
            addKeyInDict(rects_colors, key)
        else: 
            addKeyInDict(balls_colors, key)
        
    return balls_colors, rects_colors

def getNumberObjects(balls_colors, rects_colors):
    numBalls = 0
    numRects = 0
    
    for ball in balls_colors:
        numBalls += balls_colors.get(ball)
        
    for rect in rects_colors:
        numRects += rects_colors.get(rect)
        
    return numBalls, numRects


def printResult(balls_colors, rects_colors):
    
    numBalls, numRects= getNumberObjects(balls_colors, rects_colors)
    
    print("Словарь цветов кругов", balls_colors, "\n")
    print("Всего кругов ", numBalls)

    print("______________________________\n")

    print("Словарь цветов прямоугольников", rects_colors, "\n")
    print("Всего прямоугольников ", numRects)
    

image = cv2.imread("balls_and_rects.png")

hsv_min = np.array((1, 1, 1), np.uint8)
hsv_max = np.array((255, 255, 255), np.uint8)

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
thresh = cv2.inRange( hsv,hsv_min, hsv_max) 

contours, hier = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

count = 0
my_obj = [2, 4]
for contour in contours:

    if count == 0:
        my_obj[0],my_obj[1] = contour[0][0][0], contour[0][0][1]
        count +=1
        
balls_colors, rects_colors = getDicts(contours, image)

printResult(balls_colors, rects_colors)
    
cv2.drawContours(image, contours, -1, (255,0,0), 3, cv2.LINE_AA, hier, 1 )

im = cv2.resize(image, (500, 500))  
gr = cv2.resize(thresh, (500, 500)) 

cv2.imshow("Image", im)
cv2.imshow("Gray", gr)

cv2.waitKey(0)
cv2.destroyAllWindows()
