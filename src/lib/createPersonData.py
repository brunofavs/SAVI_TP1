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
import os
import numpy as np
import yaml

def createPersonData(roi,label,face_model):

    original_path = os.getcwd()

    yaml_path = "../files/yamls"
    photo_path = "../files/images"

    os.chdir(photo_path)

    person_name = face_model.getLabelInfo(label)

    file_name = "image_" + person_name + ".jpg" 

    cv2.imwrite(file_name,roi)

    os.chdir(original_path)

    os.chdir(yaml_path)

    person_dict = {"name":person_name,
                   "file_name":file_name}

    yaml_file_name = person_name + "_data.yaml"

    with open(yaml_file_name, 'w') as file:
        yaml.dump(person_dict, file)
    
    os.chdir(original_path)