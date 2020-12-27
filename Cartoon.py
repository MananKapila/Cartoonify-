#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import os


basedir = os.path.abspath(os.path.dirname(__file__))
UPLOADED_PHOTOS_DEST = os.path.join(basedir,'static','uploads')


def cartoonify(filename,s):    

    img_rgb = cv2.imread(os.path.join(UPLOADED_PHOTOS_DEST,filename)) #img inp
    numBilateralFilters = 4
    result_file = 'result_' + filename
    result_dest = os.path.join(UPLOADED_PHOTOS_DEST,result_file)
    img_color = img_rgb
    #cv2.imshow("Orignal",img_color)
    #cv2.waitKey(0)
    for _ in range(numBilateralFilters):
        img_color = cv2.bilateralFilter(img_color, 15, 30, 20)
        #cv2.imshow("Bilateral Filter",img_color)       
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.medianBlur(img_gray, 7)
    if(s=="Black&White"):
        cv2.imwrite(result_dest,img_blur)
    
    img_edge = cv2.adaptiveThreshold(img_blur, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 3, 2)
    if(s=="Sketch"):
        cv2.imwrite(result_dest,img_edge)
    #cv2.imshow("Sketch",img_edge)
    #cv2.waitKey(0)
    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
    output=cv2.bitwise_and(img_color, img_edge)
    if(s=="Painting"):
        cv2.imwrite(result_dest,output) #img storage




