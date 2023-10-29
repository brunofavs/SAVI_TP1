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
# -----------------------------
# Conventions
# -----------------------------

import argparse
import cv2
from copy import deepcopy
from functools import partial
import numpy as np
import imutils
import time

from lib.keyboardActions import *
from lib.trackers import Trackers


def main():
    # -----------------------------
    # Initialization
    # -----------------------------
    # * ---Configuration of argparse----
    parser = argparse.ArgumentParser(description='Human Identifier')
    parser.add_argument('-c', '--cascade', type=int, required=False,
                        default=0, help='Defines which Haars cascade to use for detection')
    parser.add_argument('-t', '--tracker', type=str, required=False,
                        default="kcf", help='Defines which tracker method to use for tracking')
    args = vars(parser.parse_args())

    # * Add adjustment parameters here
    trackers_algorigthms = {
        "csrt": cv2.TrackerCSRT_create,  # Slower but more accurate
        "kcf": cv2.TrackerKCF_create,   # A bit faster than csrt but less accurate
        "mosse": cv2.legacy.TrackerMOSSE_create}  # Fastest

    # * Creating tracker based on argument parsed
    tracker_type = trackers_algorigthms[args["tracker"]]


    trackers = Trackers()

    cascade_paths = ["../files/haarcascade_frontalface_default.xml",
                     "../files/haarcascade_frontalface_alt.xml",
                     "../files/haarcascade_frontalface_alt2.xml"
                     ]

    config = {"playback_speed": 30,
              "cascade": {"path": cascade_paths[args["cascade"]],
                          "scale_factor": 1.1,  # Smaller is more accurate but slower
                          "min_neighbours": 15},  # More neighbours means more accurate detections
              "new_face_threshold": 75}

    # Camera ID 0 is usually webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    prev_frame_time = 0
    next_frame_time = 0
    fps = 0

    cv2.namedWindow("Image GUI", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Image GUI", 600, 500)
    # cv2.moveWindow("Image GUI",1080,0)

    face_recognizer_model = cv2.face.LBPHFaceRecognizer_create()
    first_train = True

    train_labels = []
    train_images = []

    last_new_label = 1

    # -----------------------------
    # Processing
    # -----------------------------
    while True:

        ret, image_source = cap.read()

        if not ret:
            print("Can't receive frame from camera. Exiting ...")
            break

        # Resizing image for easier handling
        image_source = imutils.resize(image_source, width=600)
        h, w, _ = image_source.shape

        image_gui = deepcopy(image_source)

        # Converting image to grayscale
        image_gray = cv2.cvtColor(image_source, cv2.COLOR_BGR2GRAY)

        # * Detecting
        faces_rois = []

        #* Tracked faces each frame
        tracking_rois = []
        # Loading the required haar-cascade xml classifier file
        haar_cascade = cv2.CascadeClassifier(config["cascade"]["path"])

        # Applying the face detection method on the grayscale image
        faces_rect = haar_cascade.detectMultiScale(
            image_gray, config["cascade"]["scale_factor"], config["cascade"]["min_neighbours"])

        # Iterating through rectangles of detected faces
        for (x, y, w, h) in faces_rect:
            cv2.rectangle(image_gui, (x, y), (x+w, y+h), (0, 255, 0), 2)
            faces_rois.append(image_gray[y:y+h, x:x+w])

        # TODO Preprocessing of the NN inputs

        if len(faces_rect) != 0 :
        # * The first face will be on a completly untrained model, which crashes, so the first one has necessarily to be training
            if first_train:
                train_labels.append(1)
                train_images.append(faces_rois[0])

                face_recognizer_model.train(train_images, np.array(train_labels))

                person_name = input("Hello, whats your name\n") 
                # TODO Cancel prompt if false positive
                face_recognizer_model.setLabelInfo(last_new_label,person_name)

                bbox = faces_rect[0]
                trackers.add(tracker_type,image_source,bbox,last_new_label)

                
                last_new_label += 1


                first_train = False



            # * Use the LPB model to predict which face it should be
            # face_roi = faces_rois[0]

            for face_roi,face_rect in zip(faces_rois,faces_rect):
                
                label, confidence = face_recognizer_model.predict(face_roi)
                print(f'Confidence is {confidence}')
                print(f'Label is {label}')

                # * Initially the untrained model shall not make confident predictions
                # * Thus we can assume all predictions with less than a certain confidence are new faces

                if confidence > config["new_face_threshold"]:
                    print("Adding new face")
                    bbox = face_rect
                    trackers.add(tracker_type,image_source,bbox,last_new_label)

                    person_name = input("Hello, whats your name\n") 
                    face_recognizer_model.setLabelInfo(last_new_label,person_name)

                    face_recognizer_model.update([face_roi], np.asarray([2]))  
                    last_new_label +=1






        # * Tracking
        # check to see if we are currently tracking an object
        if trackers.latest_bboxs is not None:
            # grab the new bounding box coordinates of the object
            (successes, boxes) = trackers.update(image_source)

            for track_idx,(success,box) in enumerate(zip(successes,boxes)): 
                # check to see if the tracking was a success

                if success:
                    (x, y, w, h) = [int(v) for v in box]
                    tracking_rois.append(image_gray[y:y+h, x:x+w])

                    cv2.rectangle(image_gui, (x, y), (x + w, y + h),
                                (255, 255, 0), 2)
                    
                    # * The tracked face should belong to the same person, hence all the tracked ROI's should be used to train the model
                    # * to update the initially random weights
                    train_labels.append(trackers.trackers[track_idx]["label"])
                    train_images.append(tracking_rois[-1])
                    
                    # ! TRAIN STARTS FROM SCRATCH, I WANT UPDATE()
                    # face_recognizer_model.update([np.array(train_images[-1])], np.array(train_labels[-1]))
                    
                    # face_recognizer_model.update(np.asarray(train_images)[-1,:,:], trackers.trackers[track_idx]["label"]) 
                    # face_recognizer_model.update([tracking_rois[-1]], np.asarray([trackers.trackers[track_idx]["label"]]))  


                    label2, confidence2 = face_recognizer_model.predict(tracking_rois[-1])
                    label1, confidence1 = face_recognizer_model.predict(face_roi)
                    # cv2.imshow("Ti1",train_images[-1])
                    # cv2.imshow("fr1",face_roi)


                    # print(f'Tracker ROI')
                    # print(f'Confidence is {confidence2}')
                    # print(f'Label is {label2}')

                    # print(f'Face ROI')
                    # print(f'Confidence is {confidence1}')
                    # print(f'Label is {label1}')
                    
            


                    

        # -----------------------------
        # Visualization
        # -----------------------------

        # *Calculating fps
        next_frame_time = time.time()
        fps = 1/(next_frame_time-prev_frame_time)
        prev_frame_time = next_frame_time

        image_gui = cv2.putText(image_gui, f'{fps:.1f} FPS', (20, 20), cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (0, 255, 0), 2, cv2.LINE_AA)

        trackers.draw(image_gui,face_recognizer_model)
        cv2.imshow('Image GUI', image_gui)

        keyboardActions(config, image_gui)

    # -----------------------------
    # Termination
    # -----------------------------
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
