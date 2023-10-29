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
from lib.audio_pessoa_conhecida import hello_again,goodbye


class Trackers():

    # Class Variable
    trackers_algorigthms = {
        "csrt": cv2.TrackerCSRT_create,  # Slower but more accurate
        "kcf": cv2.TrackerKCF_create,   # A bit faster than csrt but less accurate
        "mosse": cv2.legacy.TrackerMOSSE_create}  # Fastest

    reInit_counter_threshold = 10

    def __init__(self, trackers=[]):
        self.trackers = trackers
        self.latest_bboxs = []
        self.latest_sucesses = []
        

    def add(self, tracker, img, bbox, label):

        assert tracker in Trackers.trackers_algorigthms.values()

        self.trackers.append({"tracker": tracker(),
                              "bbox": bbox,
                              "label": label,
                              "ready2reInit" : False,
                              "reInit_counter":0})

        self.trackers[-1]["tracker"].init(img, bbox)

        self.latest_bboxs.append(bbox)

    def update(self, image,face_model):

        sucesses = []
        bboxs = []

        for tracker_dict in self.trackers:

            tracker = tracker_dict["tracker"]

            sucess, bbox = tracker.update(image)

            tracker_dict["bbox"] = bbox

            sucesses.append(sucess)
            bboxs.append(bbox)

        # * Seeing if trackers are not active and getting them ready for reInitialization
        for track_idx, success, in enumerate(self.latest_sucesses):
            # check to see if the tracking was a success
            person_name = face_model.getLabelInfo(self.trackers[track_idx]["label"])
            
            if not success:
                if self.trackers[track_idx]["ready2reInit"] == False:
                
                    self.trackers[track_idx]["reInit_counter"] += 1

                    if self.trackers[track_idx]["reInit_counter"] == Trackers.reInit_counter_threshold:
                        self.trackers[track_idx]["ready2reInit"] = True

                        goodbye(person_name)

            else:
                if self.trackers[track_idx]["ready2reInit"] == True:
                    hello_again(person_name)

                # If it gets re detected reset
                self.trackers[track_idx]["reInit_counter"] = 0
                self.trackers[track_idx]["ready2reInit"] = False
                

        self.latest_bboxs = bboxs
        self.latest_sucesses = sucesses

        return self.latest_sucesses, self.latest_bboxs

    def draw(self, image, face_model):

        for track_idx, (success, box) in enumerate(zip(self.latest_sucesses, self.latest_bboxs)):
            # check to see if the tracking was a success
            if success:
                (x, y, w, h) = [int(v) for v in box]

                person_name = face_model.getLabelInfo(self.trackers[track_idx]["label"])

                cv2.rectangle(image, (x, y), (x + w, y + h),
                              (255, 255, 0), 2)
                image = cv2.putText(image, f'{person_name}', (x+20,y-10), cv2.FONT_HERSHEY_SIMPLEX,
                                        0.7, (0, 0, 255), 2, cv2.LINE_AA)
