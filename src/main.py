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

import cv2
from copy import deepcopy
from functools import partial
import numpy as np

from lib.keyboardActions import *


def main():
    #-----------------------------
    # Initialization
    #-----------------------------
    # * Add adjustment parameters here

    cascade_paths = ["../files/haarcascade_frontalface_default.xml",
                      "../files/haarcascade_frontalface_alt.xml",
                      "../files/haarcascade_frontalface_alt2.xml"
                ]


    config = {"playback_speed": 30,
              "cascades" : {"paths" : cascade_paths,
                            "scale_factor"   :1.1,
                            "min_neighbours" : 9}}
     
    # Camera ID 0 is usually webcam
    cap = cv2.VideoCapture(0)

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
        
        image_gui = deepcopy(image_source)
        
        # Converting image to grayscale 
        gray_img = cv2.cvtColor(image_source, cv2.COLOR_BGR2GRAY) 
        
        # Loading the required haar-cascade xml classifier file 
        haar_cascade = cv2.CascadeClassifier(config["cascades"]["paths"][0]) 
        
        # Applying the face detection method on the grayscale image 
        faces_rect = haar_cascade.detectMultiScale(gray_img, config["cascades"]["scale_factor"], config["cascades"]["min_neighbours"]) 
        
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
