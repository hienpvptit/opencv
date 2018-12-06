import sys
sys.path.insert(0,'person')

import cv2
from person import *

new_name = None
while True:
    new_name = str(input("Enter your name: ")).lower()
    if person.append_data(new_name):
        break

new_id = person.person[0]["nums"]

print "Start generator sample photo!"
print "Please look at the camera until the stop message appears!"
try:
    cam = cv2.VideoCapture(0)
    detector=cv2.CascadeClassifier('Classifiers/face.xml')
    i = 0
    offset = 50
      
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        cv2.imshow('im', gray)
        faces=detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
        for(x,y,w,h) in faces:
            i=i+1
            cv2.imwrite("dataSet/face-"+ str(new_id) +'.'+ str(i) + ".jpg", gray[y-offset:y+h+offset,x-offset:x+w+offset])
            #cv2.rectangle(im,(x-50,y-50),(x+w+50,y+h+50),(225,0,0),2)
            #cv2.imshow('im',im[y-offset:y+h+offset,x-offset:x+w+offset])
            print i,
        if i>=100:
            print "%   OK"
            cam.release()
            cv2.destroyAllWindows()
            break
except:
    print "Error"
    person.pop_data()
    cam.release()
    cv2.destroyAllWindows()

