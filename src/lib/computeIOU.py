#!/usr/bin/env python3

import yaml
import os
import cv2
import numpy as np

def main():
    
    pass

def computeIOU(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    
    # Calculate the coordinates of the intersection rectangle
    x_intersection = max(x1, x2)
    y_intersection = max(y1, y2)
    w_intersection = min(x1 + w1, x2 + w2) - x_intersection
    h_intersection = min(y1 + h1, y2 + h2) - y_intersection
    
    # If there's no intersection, IoU is 0
    if w_intersection <= 0 or h_intersection <= 0:
        return 0.0
    
    # Calculate area of intersection
    area_intersection = w_intersection * h_intersection
    
    # Calculate area of both bounding boxes
    area_box1 = w1 * h1
    area_box2 = w2 * h2
    
    # Calculate area of union
    area_union = area_box1 + area_box2 - area_intersection
    
    # Calculate IoU
    iou = area_intersection / area_union
    
    return iou


if __name__ == '__main__':
    main()


