import matplotlib.pyplot as plt
from skimage.filters import sobel, threshold_otsu, try_all_threshold
from skimage.morphology import binary_closing
from skimage.measure import label, regionprops
import numpy as np
from skimage import color

def getDict(colors):
    my_dict = {0:0}
    count = 0
    
    for i in range(len(colors)-1):
        
        my_dict[count] += 1
        diff = colors[i+1]-colors[i]
       
        if diff>0.005:
            count += 1
            my_dict[count] = 0
            
    return my_dict
    
def areaDiff(aB, aR):
  if aB!=aR:
    return True
  else:
    return False
    
image = plt.imread("balls_and_rects.png")#[:, :, :-1]
binary = image.copy()[:, :, 0]
binary[binary > 0] = 1
image = color.rgb2hsv(image)[:, :, 0]

labeled = label(binary)

balls_colors = []
rects_colors = []
colors = []

for region in regionprops(labeled):
    bb = region.bbox
    val = np.max(image[bb[0]: bb[2], bb[1]:bb[3]])
    area_rect = region.bbox_area
    
    if (areaDiff(area_rect, region.area)):
      balls_colors.append(val)
    else:
      rects_colors.append(val)

rects_colors.sort()
balls_colors.sort()

rects_colors_dict = getDict(rects_colors)
balls_colors_dict = getDict(balls_colors)

print(" Словарь для квадратов: " ,rects_colors_dict) 
print(" Словарь для кругов: " ,balls_colors_dict) 

plt.figure()
plt.plot(np.unique(image), 'o')
plt.figure()
plt.imshow(image)
plt.show()
