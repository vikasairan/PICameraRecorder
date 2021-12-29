import numpy as np
import cv2
import os
import pickle
import face_recognition
    
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "images")

y_train = []
x_train = []

for root, dirs, files in os.walk(image_dir):

	for file in files:
		if file.endswith("png") or file.endswith("jpg"):
		
			path = os.path.join(root, file)
			label = file[:file.find('.')]
			image = cv2.imread(path)
			rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			boxes = face_recognition.face_locations(rgb,model="hog", number_of_times_to_upsample=1)
			encodings = face_recognition.face_encodings(rgb, boxes, num_jitters=3)
			for encoding in encodings:
				x_train.append(encoding)
				y_train.append(label)

data = {"encodings": x_train, "names": y_train}
f = open("encodings.pickle", "wb")
f.write(pickle.dumps(data))
f.close()