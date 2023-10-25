#!/usr/bin/env python3

# --------------------------------------------------
# Alexandre, Bruno, Pedro
# SAVI, Outubro 2023.
# --------------------------------------------------

"""
Conventions

Functions    -> camelCase

Variables    -> snake_case

Class        -> PascalCase

Class objets -> camelCase

"""
#-----------------------------
# Conventions
#-----------------------------

import argparse
import cv2
from copy import deepcopy
from functools import partial
import numpy as np
from imutils.video import FPS
import imutils

from lib.keyboardActions import *


def main():
    #-----------------------------
    # Initialization
    #-----------------------------
    #* ---Configuration of argparse----
    parser = argparse.ArgumentParser(description='Human Identifier') 
    parser.add_argument('-c','--cascade',type=int,required= False,default=0,help='Defines which Haars cascade to use for detection') 
    parser.add_argument('-t','--tracker',type=str,required= False,default="kcf",help='Defines which tracker method to use for tracking') 
    args = vars(parser.parse_args())
    
    #* Add adjustment parameters here
    trackers = {
		"csrt": cv2.TrackerCSRT_create, # Slower but more accurate
		"kcf": cv2.TrackerKCF_create,   # A bit faster than csrt but less accurate
		"mosse": cv2.legacy.TrackerMOSSE_create} # Fastest
 
    # * Creating tracker based on argument parsed
    tracker = trackers[args["tracker"]]()

    tracker_info = {"tracker" : tracker,
                    "initBB": None}

    cascade_paths = ["../files/haarcascade_frontalface_default.xml",
                      "../files/haarcascade_frontalface_alt.xml",
                      "../files/haarcascade_frontalface_alt2.xml"
                ]


    config = {"playback_speed": 30,
              "cascade" : {"path" : cascade_paths[args["cascade"]],
                            "scale_factor"   :1.1,
                            "min_neighbours" : 9}}
     
    # Camera ID 0 is usually webcam
    cap = cv2.VideoCapture(0)
    fps = None

    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    #-----------------------------
    # Processing
    #-----------------------------
    while True:
        
        ret, image_source = cap.read()

        if not ret:
            print("Can't receive frame from camera. Exiting ...")
            break
        
        # Resizing image for easier handling
        image_source = imutils.resize(image_source, width=600)
        h,w,_ = image_source.shape
        
        image_gui = deepcopy(image_source)
        
        # Converting image to grayscale 
        gray_img = cv2.cvtColor(image_source, cv2.COLOR_BGR2GRAY) 
        
        # Loading the required haar-cascade xml classifier file 
        haar_cascade = cv2.CascadeClassifier(config["cascade"]["path"]) 
        
        # Applying the face detection method on the grayscale image 
        faces_rect = haar_cascade.detectMultiScale(gray_img, config["cascade"]["scale_factor"], config["cascade"]["min_neighbours"]) 
        
        # Iterating through rectangles of detected faces 
        for (x, y, w, h) in faces_rect: 
            cv2.rectangle(image_gui, (x, y), (x+w, y+h), (0, 255, 0), 2) 
        #-----------------------------
        # Visualization
        #-----------------------------
        cv2.imshow('frame', image_gui)

        keyboardActions(config,image_gui)

        
    #-----------------------------
    # Termination
    #-----------------------------
    cap.release()
    cv2.destroyAllWindows()


if __name__=="__main__":
    main()
