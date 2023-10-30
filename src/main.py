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
import os
import cv2
from copy import deepcopy
from functools import partial
import numpy as np
import imutils
import time

from lib.keyboardActions import *
from lib.trackers import Trackers
from lib.createPersonData import createPersonData
from lib.audio_pessoa_desconhecida import play_welcome,name_prompt
from lib.audio_pessoa_conhecida import hello_again
from lib.computeIOU import computeIOU

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
    parser.add_argument('-v', '--verbose',action='store_true', help='Prints debugging information')
    args = vars(parser.parse_args())

    # * Add adjustment parameters here
    trackers_algorigthms = {
        "csrt": cv2.TrackerCSRT_create,  # Slower but more accurate
        "kcf": cv2.TrackerKCF_create,   # A bit faster than csrt but less accurate
        "mosse": cv2.legacy.TrackerMOSSE_create}  # Fastest

    # * Creating tracker based on argument parsed
    tracker_type = trackers_algorigthms[args["tracker"]]


    trackers = Trackers()

    cascade_paths = ["../files/cascades/haarcascade_frontalface_default.xml",
                     "../files/cascades/haarcascade_frontalface_alt.xml",
                     "../files/cascades/haarcascade_frontalface_alt2.xml"
                     ]

    config = {"playback_speed": 30,
              "cascade": {"path": cascade_paths[args["cascade"]],
                          "scale_factor": 1.1,  # Smaller is more accurate but slower
                          "min_neighbours": 17},  # More neighbours means more accurate detections
              "new_face_threshold": 75,
              "IOU_threshold": 0.4,
              "min_size_face_roi":90}

    yamls_path = '../files/yamls'
    imgs_path = '../files/images'

    # * Cleaning old execution files
    for yaml_file in os.listdir(yamls_path):
        yaml_file_path = f'{yamls_path}/{yaml_file}'

        os.remove(yaml_file_path)

    for img_file in os.listdir(imgs_path):
        img_file_path = f'{imgs_path}/{img_file}'

        os.remove(img_file_path)

    for sound_file in os.listdir("."):
       if sound_file.endswith(".mp3"):
            os.remove(sound_file)

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
        faces_rect = haar_cascade.detectMultiScale(image_gray, config["cascade"]["scale_factor"], config["cascade"]["min_neighbours"])

        # Iterating through rectangles of detected faces
        for (x, y, w, h) in faces_rect:
            cv2.rectangle(image_gui, (x, y), (x+w, y+h), (0, 255, 0), 2)


            if w < config["min_size_face_roi"] or h < config["min_size_face_roi"]:
                continue

            faces_rois.append(image_gray[y:y+h, x:x+w])


        if len(faces_rect) != 0 :
        # * The first face will be on a completly untrained model, which crashes, so the first one has necessarily to be training
            if first_train:
                # person_name = input("Hello, whats your name\n") 
                play_welcome()
                person_name = name_prompt()

                if person_name:
                    train_labels.append(last_new_label)
                    train_images.append(faces_rois[0])

                    face_recognizer_model.train(train_images, np.array(train_labels))


                    face_recognizer_model.setLabelInfo(last_new_label,person_name)

                    bbox = faces_rect[0]
                    trackers.add(tracker_type,image_source,bbox,last_new_label)

                    createPersonData(faces_rois[0],last_new_label,face_recognizer_model)
                    
                    print(f'Saving {person_name} information') 

                    
                    last_new_label += 1

                    first_train = False
                else:
                    print("False positive, skipping")



            # * Use the LPB model to predict which face it should be

            for face_roi,face_rect in zip(faces_rois,faces_rect):
                
                if first_train:
                    break

                label, confidence = face_recognizer_model.predict(face_roi)
                if args["verbose"]:
                    print(f'\n\nLoss is {confidence}')
                    print(f'Person identified is {face_recognizer_model.getLabelInfo(label)}')


                for tracker_dict in trackers.trackers:

                    # * Check if the detection overlaps any tracker


                    # * Iterate through trackers and see if any non active one matches the label
                    if not tracker_dict["ready2reInit"]:
                        continue

                    tracker_label = tracker_dict["label"]

                    # * Reinitialize tracker
                    if tracker_label == label:
                        tracker_dict["tracker"] = tracker_type()
                        tracker_dict["tracker"].init(image_source,face_rect)

                        person_name = face_recognizer_model.getLabelInfo(tracker_label)
                        hello_again(person_name)

                        tracker_dict["reInit_counter"] = 0
                        tracker_dict["ready2reInit"] = False

                # * Initially the untrained model shall not make confident predictions
                # * Thus we can assume all predictions with less than a certain confidence are new faces

                #*  Find tracker with label detected
                #*  Check its IOU
                #*  DOnt forget the case if it doens tfind any
                for tracker_dict in trackers.trackers:

                    intersection_over_union = 0 # if it does not find any
                    
                    if tracker_dict["label"] != label:
                        continue

                    intersection_over_union = computeIOU(face_rect,tracker_dict["bbox"])


                if args["verbose"]:
                    print(f'IOU of detection and tracking is : {intersection_over_union}')

                if confidence > config["new_face_threshold"] and intersection_over_union < config["IOU_threshold"]:
                # if confidence > config["new_face_threshold"]:


                    play_welcome()
                    person_name = name_prompt()
                    
                    if person_name:
                        print("Adding new face")
                        bbox = face_rect
                        trackers.add(tracker_type,image_source,bbox,last_new_label)


                        face_recognizer_model.setLabelInfo(last_new_label,person_name)

                        face_recognizer_model.update([face_roi], np.asarray([last_new_label]))  

                        createPersonData(face_roi,last_new_label,face_recognizer_model)
                        
                        print(f'Saving {person_name} information') 

                        last_new_label +=1
                    else:
                        print("False positive, skipping")


        # * Tracking
        # check to see if we are currently tracking an object
        if trackers.latest_bboxs is not None:
            # grab the new bounding box coordinates of the object
            (successes, boxes) = trackers.update(image_source,face_recognizer_model)

            for track_idx,(success,box) in enumerate(zip(successes,boxes)): 
                # check to see if the tracking was a success

                if success:
                    (x, y, w, h) = [int(v) for v in box]
                    tracking_rois.append(image_gray[y:y+h, x:x+w])
                    
                    # * The tracked face should belong to the same person, hence all the tracked ROI's should be used to train the model
                    # * to update the initially random weights
                    train_labels.append(trackers.trackers[track_idx]["label"])
                    train_images.append(tracking_rois[-1])
                    
                    # ! TRAIN STARTS FROM SCRATCH, I WANT UPDATE()
                    face_recognizer_model.update([tracking_rois[-1]], np.array([trackers.trackers[track_idx]["label"]]))
                    
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
