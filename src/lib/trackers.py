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

    # Class Variable
    trackers_algorigthms = {
        "csrt": cv2.TrackerCSRT_create,  # Slower but more accurate
        "kcf": cv2.TrackerKCF_create,   # A bit faster than csrt but less accurate
        "mosse": cv2.legacy.TrackerMOSSE_create}  # Fastest

    def __init__(self, trackers=[]):
        self.trackers = trackers
        self.latest_bboxs = []

    # TODO add label too to know what the tracker is tracking
    def add(self, tracker, img, bbox, label):

        assert tracker in Trackers.trackers_algorigthms.values()

        self.trackers.append({"tracker": tracker(),
                              "bbox": bbox,
                              "label": label})

        self.trackers[-1]["tracker"].init(img, bbox)

        self.latest_bboxs.append(bbox)

    def update(self, image):

        sucesses = []
        bboxs = []

        for tracker_dict in self.trackers:

            # print(tracker_dict)

            tracker = tracker_dict["tracker"]

            sucess, bbox = tracker.update(image)

            tracker_dict["bbox"] = bbox

            sucesses.append(sucess)
            bboxs.append(bbox)

        self.latest_bboxs = bboxs

        return sucesses, self.latest_bboxs

    def draw(self):
        pass
