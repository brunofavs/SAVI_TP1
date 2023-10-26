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
import imutils
import time 

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

    tracker_vars = {"tracker" : tracker,
                    "initBB": None}

    cascade_paths = ["../files/haarcascade_frontalface_default.xml",
                      "../files/haarcascade_frontalface_alt.xml",
                      "../files/haarcascade_frontalface_alt2.xml"
                ]


    config = {"playback_speed": 30,
              "cascade" : {"path" : cascade_paths[args["cascade"]],
                            "scale_factor"   :1.1, # Smaller is more accurate but slower
                            "min_neighbours" : 13}} # More neighbours means more accurate detections
     
    # Camera ID 0 is usually webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    prev_frame_time = 0
    next_frame_time = 0
    fps = 0

    cv2.namedWindow("Image GUI",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Image GUI",600,500)
    # cv2.moveWindow("Image GUI",1080,0)
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


        if tracker_vars["initBB"] is None and len(faces_rect) != 0:
            tracker_vars["initBB"] = faces_rect[0]
            tracker_vars["tracker"].init(image_source,tracker_vars["initBB"])
        
        # * Tracking
        # check to see if we are currently tracking an object
        if tracker_vars["initBB"] is not None:
            # grab the new bounding box coordinates of the object
            (success, box) = tracker.update(image_source)
            print(success)
                
                # check to see if the tracking was a success
            if success:
                (x, y, w, h) = [int(v) for v in box]
                cv2.rectangle(image_gui, (x, y), (x + w, y + h),
                    (255, 255, 0), 2)

        #-----------------------------
        # Visualization
        #-----------------------------

        # *Calculating fps
        next_frame_time = time.time()
        fps = 1/(next_frame_time-prev_frame_time)
        prev_frame_time = next_frame_time

        image_gui = cv2.putText(image_gui,f'{fps:.1f} FPS' , (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.7, (0,255,0), 2, cv2.LINE_AA)

        cv2.imshow('Image GUI', image_gui)

        keyboardActions(config,image_gui)

        
    #-----------------------------
    # Termination
    #-----------------------------
    cap.release()
    cv2.destroyAllWindows()


if __name__=="__main__":
    main()
