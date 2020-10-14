# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 21:12:16 2020

@author: Adm
"""
def main(files):
    result = []
    for file in files:
        mm, datas = getData(file)
        count = getCountOnes(datas)
        result.append(getResult(mm, count))
    return result
    
def getData(file):
    with open (file, 'r') as f:
        mm = f.readline()
        f.readline()
        datas = f.read()
    return mm, datas
    
def getCountOnes(datas):
    count=0
    for data in datas:
        if data=='1':
            count+=1
    return count
    
def getResult(mm, count):
    mm = float(mm)
    if count==0:
        return "Еhe figure does not exist"
    else:
        return mm/count
 
files = ["figure1.txt", "figure2.txt","figure3.txt", "figure4.txt", "figure5.txt", "figure6.txt"]   
result = main(files)

for res in result:
    print(res)
