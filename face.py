import numpy as np
import cv2
import os
import pickle
import face_recognition


def predict_face(rgb):
    boxes = face_recognition.face_locations(rgb,model="hog",number_of_times_to_upsample=3) 
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []
    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"],encoding, tolerance=0.45)
        name = "unknown"
        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
                name = max(counts, key=counts.get)
        return name

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_default.xml')
	
with open("encodings.pickle", 'rb') as f:
	data = pickle.load(f)
cap = cv2.VideoCapture(0)
while(True):
	ret, frame = cap.read()
	image  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	faces = face_cascade.detectMultiScale(image, scaleFactor=1.5, minNeighbors=5)
	for (x, y, w, h) in faces:
    
		rgb = image[y:y+h, x:x+w]
		name = predict_face(rgb)
		font = cv2.FONT_HERSHEY_SIMPLEX
		color = (255, 255, 255)
		stroke = 2
		cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
		color = (255, 0, 0) #BGR 0-255 
		stroke = 2
		end_cord_x = x + w
		end_cord_y = y + h
		cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
	cv2.imshow('frame',frame)
	if cv2.waitKey(20) & 0xFF == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()