#!/usr/bin/env python3

import yaml
import os
import cv2
import numpy as np

def main():
    
    # !TEMP
    main_path = "../"
    os.chdir(main_path)

    createImgGrid()

def createImgGrid():
    
    yamls_path = '../files/yamls'
    imgs_path = '../files/images'

    image_filename_array = []
    names_array = []
    images_array = []


    for yaml_file in os.listdir(yamls_path):
        # print('filenames:',yaml_file)

        if yaml_file.startswith('.'):
            print('Skipping system file')
            continue
        
        yaml_file_path = f'{yamls_path}/{yaml_file}'
        
        
        with open(yaml_file_path, 'r') as file:
            data_dict = yaml.safe_load(file)
            
            names_array.append(data_dict["name"])
            image_filename_array.append(data_dict["file_name"])


    for image_filename,name in zip(image_filename_array,names_array):
        img_path = f'{imgs_path}/{image_filename}'

        pre_processed_img = cv2.imread(img_path) 

        img = cv2.resize(pre_processed_img,(200,200), interpolation= cv2.INTER_AREA)
        cv2.putText(img,name , (20,30), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)

        images_array.append(img)


    for idx,image in enumerate(images_array):

        if idx==0:
            grid = image
            continue

        grid = np.concatenate((grid,image),axis=1) 

    cv2.namedWindow("Grid", cv2.WINDOW_NORMAL)
    cv2.imshow("Grid",grid)


    # for idx,image in enumerate(images_array):
        # cv2.imshow(str(idx),image)

if __name__ == '__main__':
    main()


