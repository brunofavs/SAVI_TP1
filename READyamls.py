#!/usr/bin/env python3

import yaml
import os
import cv2

data_path = './Face_samples_dataset/yamls'

def main():
    for path, subdirname, filenames in os.walk(data_path):
        # print('path:',path)
        # print('subdirname:',subdirname)
        print('filenames:',filenames)



        for file_name in filenames:
            if file_name.startswith('.'):
                print('Skipping system file')
                continue
            
            path2open = f'{data_path}/{file_name}'
            
            
            with open(path2open, 'r') as file:
                data = yaml.safe_load(file)
                print(data)
                   
                    
                    


if __name__ == '__main__':
    main()


