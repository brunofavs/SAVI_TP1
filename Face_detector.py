#!/usr/bin/env python3


import cv2

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('/home/mestre/Desktop/SAVI/REPO_eu_SAVI/testeclone/SAVI_TP1/Training_data.yml')

def face_detector(img):

    global x,y,w,h
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier('/home/mestre/Desktop/SAVI/REPO_eu_SAVI/testeclone/SAVI_TP1/haarcascade_frontalface_default.xml')
    faces = face_classifier.detectMultiScale(gray_img, scaleFactor=1.3, minNeighbors=7)

    if faces == ():
        return img,[]

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
        roi = img[y:y+h,x:x+w]
        roi = cv2.resize(roi,(500,500))

    return img,roi

name = {0:'Mestre',1:'Virat Kohli'}


def main():
    cap = cv2.VideoCapture(0)
    while True:
        ret,img_frame = cap.read()

        image,req_face = face_detector(img_frame)


        try:
            req_face = cv2.cvtColor(req_face, cv2.COLOR_BGR2GRAY)
            label, confidence = face_recognizer.predict(req_face)
            print('Confidence :',confidence)
            print('Label :',label)

            l = label

            face_label = name[label]
            #print(face_label)

            if (label == l) and (confidence < 50):
                print('Face Recognized !!!')
                cv2.putText(image, face_label, (x, y), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)
                cv2.imshow('Face Recognizer', image)

            else:
                print('Unknown Face !!!')
                cv2.putText(image, 'Unknown', (x, y), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
                cv2.imshow('Face Recognizer', image)

        except:
            print('Face not found')
            cv2.putText(image, 'X X X ! Face Not Found ! X X X', (50, 450), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Face Recognizer', image)
            pass

        if cv2.waitKey(1)==13:
            break

    cap.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()


