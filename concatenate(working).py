#!/usr/bin/env python3



import cv2
import glob
import numpy as np
import imutils

def main():
    import cv2
    import numpy as np
    img1 = cv2.imread('/home/mestre/Desktop/SAVI/REPO_eu_SAVI/testeclone/SAVI_TP1/Face_samples_dataset/0/WhatsApp Image 2023-10-26 at 23.10.45.jpeg')
    img2 = cv2.imread('/home/mestre/Desktop/SAVI/REPO_eu_SAVI/testeclone/SAVI_TP1/Face_samples_dataset/0/WhatsApp Image 2023-10-26 at 23.11.17.jpeg')
    vis1 = np.concatenate((img1, img2), axis=1)
    cv2.imwrite('out.png', vis1)
    cv2.imshow('database',vis1)
    cv2.waitKey(0)
    
    #h1, w1 = img1.shape[:2]
    #h2, w2 = img2.shape[:2]
#
    ##create empty matrix
    #vis = np.zeros((max(h1, h2), w1+w2,3), np.uint8)
#
    ##combine 2 images
    #vis[:h1, :w1,:3] = img1
    #vis[:h2, w1:w1+w2,:3] = img2
    #cv2.imshow('ol',vis)
    #
    #cv2.waitKey(0)


if __name__ == '__main__':
    main()


