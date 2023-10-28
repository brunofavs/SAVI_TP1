#!/usr/bin/env python3



import cv2
import glob
import numpy as np
import imutils
import os


labels = []
data_path = '/home/mestre/Desktop/SAVI/REPO_eu_SAVI/testeclone/SAVI_TP1/Face_samples_dataset/'
scale = 0.25

def main():
    
    
    
    
    img1 = cv2.imread('/home/mestre/Desktop/SAVI/REPO_eu_SAVI/testeclone/SAVI_TP1/Face_samples_dataset/0/WhatsApp Image 2023-10-26 at 23.10.45.jpeg')
    img2 = cv2.imread('/home/mestre/Desktop/SAVI/REPO_eu_SAVI/testeclone/SAVI_TP1/Face_samples_dataset/0/WhatsApp Image 2023-10-26 at 23.11.17.jpeg')
    
    width = int(img1.shape[1]*scale)
    height = int(img1.shape[0]*scale)
    dim = (width, height)
    dim1 = (200, 250)
    
    resized1 = cv2.resize(img1, dim1, interpolation = cv2.INTER_AREA)
    resized2 = cv2.resize(img2, dim1, interpolation = cv2.INTER_AREA)
    
    aspected1 = cv2.resize(img1, dim, interpolation = cv2.INTER_AREA)
    aspected2 = cv2.resize(img2, dim, interpolation = cv2.INTER_AREA)
    
    vis1 = np.concatenate((img1, img2), axis = 1)
    vis2 = np.concatenate((resized1,resized2), axis = 1)
    vis3 = np.concatenate((aspected1,aspected2), axis = 1)
    
    cv2.imshow('originais',vis1)
    cv2.imshow('sempreservaraspectratio',vis2)
    cv2.imshow('preservandoaspectratio',vis3)
    cv2.waitKey(0)
    




if __name__ == '__main__':
    main()


