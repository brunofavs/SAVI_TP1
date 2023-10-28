#!/usr/bin/env python3

import yaml
import os
import cv2

data_path = '/home/mestre/Desktop/SAVI/REPO_eu_SAVI/testeclone/SAVI_TP1/Face_samples_dataset/yamls'

def main():
    for path, subdirname, filenames in os.walk(data_path):
        print('path:',path)
        print('subdirname:',subdirname)
        print('filenames:',filenames)



        for file_name in filenames:
            if file_name.startswith('.'):
                print('Skipping system file')
                continue
            
            
            print(file_name)
            
            with open('Face_samples_dataset/yamls/data.yaml', 'r') as file:
                data_yaml = yaml.safe_load(file)
                print(data_yaml)
                   
                    
                    


if __name__ == '__main__':
    main()


