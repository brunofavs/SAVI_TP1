#!/usr/bin/env python3

# --------------------------------------------------
# Alexandre, Bruno, Pedro
# SAVI, Outubro 2023.
# --------------------------------------------------

"""
Convetions

Functions    -> camelCase

Variables    -> snake_case

Class        -> PascalCase

Class objets -> camelCase

"""

import cv2
import numpy as np


class Trackers():

    def __init__(self,trackers = []):
        self.trackers = trackers
        self.latest_bboxs = []

    def add(self,tracker,img,bbox):
        
        assert isinstance(tracker,cv2.Tracker),"Added a non tracker to trackers"

        self.trackers.append(tracker)

        self.trackers[-1].init(img,bbox)

        self.latest_bboxs.append(bbox)

        

    def update(self,image):
        
        sucesses = []
        bboxs = []

        print(self.trackers)
        for tracker in self.trackers:
            sucess,bbox = tracker.update(image) 
            print(sucess,bbox)
            sucesses.append(sucess)
            bboxs.append(bbox)

        self.latest_bboxs = bboxs

        return sucesses,self.latest_bboxs
    
    def draw(self):
        pass