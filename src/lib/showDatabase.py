#!/usr/bin/env python3

import yaml
import os
import cv2

yaml_path = '../files/yamls'
img_path = '../files/images'

main_path = "../"

os.chdir(main_path)

names=[]
paths=[]
images={}
def main():
    
    for yaml_file in os.listdir(yaml_path):
        print('filenames:',yaml_file)
        continue



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


