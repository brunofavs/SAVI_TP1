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
    config = {"playback_speed": 30}

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    #-----------------------------
    # Processing
    #-----------------------------
    while True:
        
        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame from camera. Exiting ...")
            break
        
        image_gui = deepcopy(frame)

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
