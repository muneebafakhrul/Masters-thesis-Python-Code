# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 14:20:03 2022

@author: muneeba
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 13:50:51 2022

@author: muneeba
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 13:05:34 2022

@author: muneeba
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage
from skimage import measure, color, io

#STEP1 - Read image and define pixel size
img = cv2.imread("images/image022 (2).jpg", 0)

pixels_to_um = 0.00940438724 # (1 px = 500 nm)
cropped_img = img[0:962, 0:1280]

ret, thresh = cv2.threshold(cropped_img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)


mask = thresh == 255

s = [[1,1,1],[1,1,1],[1,1,1]]
labeled_mask, num_labels = ndimage.label(mask, structure=s)

clusters = measure.regionprops(labeled_mask, cropped_img) 
propList = ['Area',
            'equivalent_diameter', #Added... verify if it works
            'orientation', #Added, verify if it works. Angle btwn x-axis and major axis.
            'MajorAxisLength',
            'MinorAxisLength',
            'Perimeter',
            'MinIntensity',
            'MeanIntensity',
            'MaxIntensity']    
    

output_file = open('image_measurements.csv', 'w')
output_file.write(',' + ",".join(propList) + '\n') #join strings in array by commas, leave first cell blank
#First cell blank to leave room for header (column names)

for cluster_props in clusters:
    #output cluster properties to the excel file
    output_file.write(str(cluster_props['Label']))
    for i,prop in enumerate(propList):
        if(prop == 'Area'): 
            to_print = cluster_props[prop]*pixels_to_um**2   #Convert pixel square to um square
        elif(prop == 'orientation'): 
            to_print = cluster_props[prop]*57.2958  #Convert to degrees from radians
        elif(prop.find('Intensity') < 0):          # Any prop without Intensity in its name
            to_print = cluster_props[prop]*pixels_to_um
        else: 
            to_print = cluster_props[prop]     #Reamining props, basically the ones with Intensity in its name
        output_file.write(',' + str(to_print))
    output_file.write('\n')
output_file.close()   #Closes the file, otherwise it would be read only. 
