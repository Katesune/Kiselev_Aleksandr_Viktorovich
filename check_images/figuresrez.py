# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 01:26:20 2020

@author: Adm
"""

def getData(file):
    datas = []
    with open (file, 'r') as f:
        f.readline()
        f.readline()
        while f.readline():
            datas.append(f.readline())
    return datas

def getLine(img1):
    for line in img1:
        for num in line:
            if num=='1':
                return line
    return "The picture does not exist"

def clearLine(line):
    i=0
    j=len(line)-1
    
    while line[i]!='1' and i!=len(line)-1:
        i+=1
        
    while line[j]!='1' and j!=-1:
        j-=1
        
    line = line[i:j+1]
    
    return line
    
def getImg(img):
    all_img = []
    for line in img:
        line = clearLine(line)
        if (line):
            all_img.append(line)
    return all_img

def checkImages(img1, img2):
    for i in range(len(img1)):
        if img1[i]!=img2[i]:
            return -1
    return 1

def findX(line):
    count=0
    while line[count]!='1':
        count+=1
    return count
    
def getBias(img):
    y=0
    for line in img:
        x=0
        for l in line:
            x+=1
            if l=='1':
                return x, y
        y+=1
    return x, y
    

files = ["img1.txt", "img2.txt"]

img1 = getData(files[0])
img2 = getData(files[1])


img1_1 = getImg(img1)
img2_1 = getImg(img2)


if checkImages(img1_1,img2_1)==-1:
    print("The images does not match")
else :
    x1, y1 = getBias(img1)
    x2, y2 = getBias(img2)
    print('x1 = ', x1, ' y1 = ', y1)
    print('x2 = ', x2,' y2 = ', y2)
    print('Result: ',' offset from x -', abs(x2-x1), '; offset from y -', abs(y2-y1) )