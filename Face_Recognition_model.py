#!/usr/bin/env python3

import cv2
import numpy as np
import os


face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

data_path = '/home/mestre/Desktop/SAVI/REPO_eu_SAVI/testeclone/SAVI_TP1/Face_samples_dataset/'

training_data, labels = [], []
    


def main():
    

    
    for path, subdirname, filenames in os.walk(data_path):
        print('path:',path)
        print('subdirname:',subdirname)
        print('filenames:',filenames)

        for file_name in filenames:
            if file_name.startswith('.'):
                print('Skipping system file')
                continue

            f_id = os.path.basename(path)
            img_path = os.path.join(path,file_name)
            print('img_path:',img_path)
            print('f_id:',f_id)

            test_img = cv2.imread(img_path)
            if test_img is None:
                print('Image not loaded properly !!!')
                continue

            test_gray = cv2.cvtColor(test_img,cv2.COLOR_BGR2GRAY)

            faces = face_classifier.detectMultiScale(test_gray,scaleFactor=1.3,minNeighbors=5)


            if len(faces) != 1:
                continue

            for (x,y,w,h) in faces:
                roi_gray = test_gray[y:y+h,x:x+w]
                print('roi:',roi_gray)

            roi_gray = cv2.resize(roi_gray,(500,500))

            training_data.append(roi_gray)
            labels.append((f_id))

            model = cv2.face.LBPHFaceRecognizer_create()
            model.train(np.asarray(training_data),np.asarray(labels))
            model.save('/home/mestre/Desktop/SAVI/REPO_eu_SAVI/testeclone/SAVI_TP1/Training_data.yml')


if __name__ == '__main__':
    main()




