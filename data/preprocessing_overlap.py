# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 16:33:42 2020

@author: Gangmin
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 14:22:53 2020

@author: Gangmin
"""
# list for the number of image split
overlaps = [0,20,40,60,80]



import os
path = "C:/Users/Gangmin/Desktop/SLIC/논문작업/sourcecode/BSR/BSDS500/data/images/train"
file_list = os.listdir(path)
file_list_img = [file for file in file_list if file.endswith(".jpg")]

#save to csv file.
import pandas as pd
from PIL import Image
temp = 0
for overlap in overlaps:
    percent = int(overlap/2)
    split = 8
    for img_name in file_list_img:
        # load the image and apply SLIC and extract (approximately)
        # the supplied number of segments
        img = Image.open(path +'/'+ img_name)
        size = img.size
        temp = size[1]//split
        remain = size[1]%split
        split_list =[]
        for i in range(split):
            split_list.insert(0,temp)
            if remain is not 0:
                split_list[0] = split_list[0]+1
                remain -=1
        index_start = 0
        
        #print(split_list)
        
        for i in range(0,split):
            extension = int(split_list[i]*percent/100)
            #i만큼 붙여서 j번 반복
            index_end =0
            for k in range(0,i+1):
                index_end += split_list[k]
            area = (0,max(0,index_start-extension),size[0],min(index_end+extension,size[1]))
            print(area)
            #print(img_name)
            #print(area)
            #cropped_img = img.crop(area)
            #cropped_img.save("C:/Users/Gangmin/Desktop/SLIC/논문작업/sourcecode/overlap_image/"+str(overlap)+"/"+img_name[:-4]+'_'+str(i)+".jpg")
            index_start += split_list[i]
        
        
        
        break
    break
    
    
'''
index = 0
final_list = []
for i in range(split):
    final_list.append(index)
    index += split_list[i]
area = ()
'''

    