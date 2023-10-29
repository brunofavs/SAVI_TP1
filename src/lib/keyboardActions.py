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
from lib.showDatabase import createImgGrid

def keyboardActions(config, image_gui):

    # To prevent NumLock issue
    pressed_key = cv2.waitKey(config['playback_speed']) & 0xFF

    if pressed_key == ord('q'):
        print("Quitting program")
        cv2.destroyAllWindows
        exit()

    if pressed_key == ord('d'):
        grid = createImgGrid()
        cv2.imshow("Database",grid)