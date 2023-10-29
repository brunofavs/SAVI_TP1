#!/usr/bin/env python3

import yaml
import os
import cv2

data_path = './Face_samples_dataset/yamls'

names=[]
paths=[]
images={}
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
                # print(data)
                
                names.append(data[0])
                paths.append(data[1])
        print(names,paths)
        
        for x in range(len(names)):
            images["img{0}".format(x)] = cv2.imread(path[x])
            
        print(images)
            
                

                   
                    
                    


if __name__ == '__main__':
    main()


