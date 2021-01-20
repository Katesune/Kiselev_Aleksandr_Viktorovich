from mss import mss
import pyautogui as keys
import time
import cv2
import numpy as np

def monitor_part(img): 
    x_dino = 211
    y_dino = 407
    cactus_width = 663       
    cactus_height = 45
     
    cactus = img[y_dino:y_dino+cactus_height, x_dino:x_dino+cactus_width]
    
    return cactus
    
# def watch(sreen_tool):
    
#     img = cv2.imread(sreen_tool.shot())
#     cactus = monitor_part(img)
    
#     #cactus = img[y_dino:y_dino+cactus_height, x_dino:x_dino+cactus_width]
    
#     cactus_gray = cv2.cvtColor(cactus, cv2.COLOR_BGR2HSV)
    
#     ready_cactus = cv2.inRange(cactus_gray, np.array([0, 0, 0]), np.array([255, 255, 100]))
    
#     conts, hier = cv2.findContours(ready_cactus, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
      
#     #cv2.drawContours(cactus, conts, -1, (255,0,0), 3, cv2.LINE_AA, hier, 1 )
    
#     #cv2.imwrite("cactus.png",cactus)
   
#     if len(conts)>0:
#         keys.keyDown('space')
#         return True
           
#     return False
    
    
sreen_tool = mss()

x, y = keys.position()

keys.click(x=442, y=418)

count=0
while x< 1600:
    img = cv2.imread(sreen_tool.shot())
    cactus = monitor_part(img)
    
    cactus_gray = cv2.cvtColor(cactus, cv2.COLOR_BGR2HSV)
    
    ready_cactus = cv2.inRange(cactus_gray, np.array([0, 0, 0]), np.array([255, 255, 100]))
         
    conts, hier = cv2.findContours(ready_cactus, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(conts)>0:
        keys.keyDown('space')
        time.sleep(0.05)
        keys.keyUp('space')
        count+=1
        print("jump ", count)
    
    #watch(sreen_tool)
    #print(x, y)
    # if watch(sreen_tool) == True:
    #     keys.keyDown('space')
              
    x, y = keys.position()         
