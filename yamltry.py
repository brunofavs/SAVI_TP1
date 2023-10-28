#!/usr/bin/env python3

import yaml
import os
import cv2

data_path = '/home/mestre/Desktop/SAVI/REPO_eu_SAVI/testeclone/SAVI_TP1/Face_samples_dataset/'

def main():
    for path, subdirname, filenames in os.walk(data_path):
        print('path:',path)
        print('subdirname:',subdirname)
        print('filenames:',filenames)



        for file_name in filenames:
            if file_name.startswith('.'):
                print('Skipping system file')
                continue
            
            if file_name.endswith('l'):
                print(file_name)
                with open(file_name, 'r') as file:
                    data_yaml = yaml.safe_load(file)
                    print(data_yaml)
                    print(data_yaml[0])
                    print(data_yaml[1])
                    name = data_yaml [0]
                    img_path = data_yaml[1]
                    test_img = cv2.imread(img_path)
                    cv2.imshow('pedro',test_img)
                    cv2.waitKey(0)
                    
                    


if __name__ == '__main__':
    main()


