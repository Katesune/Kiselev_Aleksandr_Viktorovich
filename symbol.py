import matplotlib.pyplot as plt
import numpy as np
import cv2

def changeAlph(gray):
    
    new_gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edged = cv2.Canny(new_gray, 100, 50)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(edged, cv2.MORPH_GRADIENT, kernel)
    
    return closed

def changeImg(gray):
    
    new_gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edged = cv2.Canny(new_gray, 10, 100, 5)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    closed = cv2.morphologyEx(edged, cv2.MORPH_GRADIENT, kernel)
    
    return closed

def drawRectAboveSymb(symb, image):
     rect = cv2.minAreaRect(symb) 
     box = cv2.boxPoints(rect) 
     box = np.int0(box)
     cv2.drawContours(image,[box],0,(0,0,255),8)
 
def getAreaRect(symb):
    rect = cv2.minAreaRect(symb) 
    box = cv2.boxPoints(rect) 
    box = np.int0(box)

    return rect


def getAreaDiff(letter, alph):
    # koef = 6.875
    # koef = 1
    koef = 1.4
    area_maybe = pow(cv2.contourArea(letter),koef)
    area_alph = cv2.contourArea(alph)
    
    diff = area_alph - area_maybe
    diff = abs(diff)
    
    return diff

def getLengthFromDict(my_dict):
    count = 0
    for i in range(len(my_dict)):
        count+=my_dict[i][1]
        
    return count
    

def printAreaReckts(letter, alph):
    letter_rect = getAreaRect(letter)
    alph_rect = getAreaRect(alph)
    
    one_arearect = letter_rect[1][0]*letter_rect[1][1]
    two_arearect = alph_rect[1][0]*alph_rect[1][1]
    
    print(" letter_rect = ", one_arearect - two_arearect)

def getBetterMatch(letter, alphs):
    minRes=0
    
    for alph in alphs:
        res = cv2.matchShapes(alph,letter,cv2.CONTOURS_MATCH_I1,1)

def checkSymb(letter, alphs, image, image2):
    
    area_diff = 1000
    right_letter = 0
    count=0
    
    #смотрим совпадения с шаблоном, если совпадение меньше двух, 
    #оно не засчитывается
    
    low_res = 2
    
    
    for alph in alphs:
        res = cv2.matchShapes(alph,letter,cv2.CONTOURS_MATCH_I1,1)
         
        if res<low_res:
            
            right_letter = count
            low_res = res
            area_diff = getAreaDiff(letter, alph)
            
        elif res == low_res:
            
            if getAreaDiff(letter, alph)<area_diff:
                area_diff = getAreaDiff(letter, alph)
                right_letter = count
    
        count+=1
        
    #для отладки, чтобы найденный символ
    #обводился на изображении с алфавитом
    
    # count = 0
    # for alph in alphs:
    #     if count == right_letter:
    #         drawRectAboveSymb(alph, image2)
    #     count+=1
        
    return right_letter

alphabet = cv2.imread("alphabet_ext.png")
image = cv2.imread("symbols.png")
static_img = cv2.imread("symbols.png")

alphabet_gray = cv2.cvtColor(alphabet, cv2.COLOR_BGR2GRAY)
nice_alphabet = changeAlph(alphabet_gray)

img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
nice_img = changeImg(img_gray)

conts, hier = cv2.findContours(nice_alphabet, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
conts1, hier1 = cv2.findContours(nice_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

my_dict = [['-', 0],['D',0], ['P',0], ['/',0], [ '*',0], [ 'X',0], [ 'W',0],  
           ['1',0], [ 'B',0], [ 'A',0], [ '0',0], [ '8',0]]


count=0

for c in conts1:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    
    alph_num = checkSymb(c, conts, image, alphabet)
    my_dict[alph_num][1]+=1
    drawRectAboveSymb(c, image)
    count+=1
        
   
print(my_dict)
print(len(conts1))
print(getLengthFromDict(my_dict))
print(getLengthFromDict(my_dict)/len(conts1)*100)

im = cv2.resize(nice_img, (1000, 1000))  
cv2.imwrite("Input.png", image)
cv2.imwrite("NiceImg.png", nice_img)
cv2.imshow("Input", im)
im2 = cv2.resize(alphabet, (600, 300))  
cv2.imshow("static_img", im2)
cv2.waitKey(0)
cv2.destroyAllWindows()
