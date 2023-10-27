#!/usr/bin/env python3


import cv2
import glob
import numpy as np


def main():
    image_paths1 = glob.glob("Face_samples_dataset/0/*.jpeg")
    result_image = np.zeros((200, 200, 1), dtype=np.uint8)
    #for image_path in image_paths1:
    #    image = cv2.imread(image_path)
        # Add the image to the resulting image
        #result_image = cv2.addWeighted(result_image, 1, image, 1, 0)
    #image = cv2.imshow('result_image.jpg',result_image)
    # cv2.imwrite("imagem", result_image)
    #cv2.waitKey(0)

    image1 = cv2.imread('/home/mestre/Desktop/SAVI/REPO_eu_SAVI/testeclone/SAVI_TP1/Face_samples_dataset/0/WhatsApp Image 2023-10-26 at 23.10.45.jpeg', 1) 
  
# Read image2 
    image2 = cv2.imread('/home/mestre/Desktop/SAVI/REPO_eu_SAVI/testeclone/SAVI_TP1/Face_samples_dataset/0/WhatsApp Image 2023-10-26 at 23.11.17.jpeg', 1) 
    image1=np.resize(image1,image2.shape)
# Add the images 
    img = cv2.add(image1, image2) 
  
# Show the image 
    cv2.imshow('image', img) 
    cv2.waitKey(0)
if __name__ == '__main__':
    main()


