import sys
sys.path.insert(0,'person')

from person import *
import cv2,os
import numpy as np
from PIL import Image 
import pickle
import time


recognizer = cv2.createLBPHFaceRecognizer()
recognizer.load('trainer/trainer.yml')
cascadePath = "Classifiers/face.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
path = 'dataSet'

cam = cv2.VideoCapture(0)
font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1) #Creates a font

last_time = time.time()

count = range(0, person.person[0]["nums"]+1)
for i in range(0, person.person[0]["nums"]+1):
	count[i] = 0

while True:
	ret, im =cam.read()
	gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	faces=faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
	for(x,y,w,h) in faces:
		nbr_predicted, conf = recognizer.predict(gray[y:y+h,x:x+w])
		cv2.rectangle(im,(x-50,y-50),(x+w+50,y+h+50),(225,0,0),2)
		if conf<100:
			count[nbr_predicted] += 1
			nbr_predicted=person.person[nbr_predicted]["name"]
		else:
			count[0] += 1
			nbr_predicted = "Unknow"
		
		for i in range(0, person.person[0]["nums"]+1):
			if count[i]>100:
				if i==0:
					print "Unknow"
					cmd = """mosquitto_pub -h localhost -t "person/status" -m "unknown" """
				else:
					print person.person[i]["name"]
					cmd = """mosquitto_pub -h localhost -t "person/status" -m "%s" """ %(person.person[i]["name"])
				os.system(cmd)
				cam.release()
				cv2.destroyAllWindows()
				exit(0)
		
		cv2.cv.PutText(cv2.cv.fromarray(im),str(nbr_predicted)+"--"+str(conf), (x,y+h),font, 255) #Draw the text
	cv2.imshow('im',im)
       
	if cv2.waitKey(1)&0xFF == ord('q'):
		cam.release()
		cv2.destroyAllWindows()
		exit(0)









