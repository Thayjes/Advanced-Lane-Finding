# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 16:07:15 2017
The python file will describe the functions for the pipeline, used in 
the Advanced Lane Finding project of Udacity's Self Driving Car Nanodegree Program
@author: lenovo
"""
import cv2
import pickle
from matplotlib import pyplot as plt 
def region_of_interest(img, vertices):
    """
    Applies an image mask.
    
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def undistort(img):
    with open("C:/Users/lenovo/Documents/SDCND/Advanced-Lane-Finding/dist_pickle.p", "rb") as fname:
        dp = pickle.load(fname)
        mtx = dp["Camera_Matrix"] 
        dist = dp["Distortion_Coefficients"]
        dst = cv2.undistort(img, mtx, dist, None ,mtx)
        f, (ax1, ax2) = plt.subplots(1, 2, figsize = (20, 10))
        ax1.set_title("Original Image")
        ax1.imshow(img, cmap = "gray")
        ax2.set_title("Undistorted Image")
        ax2.imshow(dst, cmap = "gray")
        return dst
# An example
#dst = undistort(img_test)