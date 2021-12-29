import numpy as np
import cv2
import os
from imageai.Detection.Custom import CustomObjectDetection
from PIL import Image
import scipy.misc

execution_path = os.getcwd()

detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path , "dataset//models//detection_model-ex-051--loss-0002.067.h5")) 
detector.setJsonPath(os.path.join(execution_path , "dataset//json//detection_config.json"))
detector.loadModel()

cap = cv2.VideoCapture(0)
while(True):
	ret, frame = cap.read()
	image  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	output,detections = detector.detectObjectsFromImage(input_type="array",input_image=image,output_type="array")
	for eachObject in detections:
		print(eachObject["name"] , " : " , eachObject["percentage_probability"] , " : ", eachObject["box_points"] )
	cv2.imshow("frame",cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
	if cv2.waitKey(20) & 0xFF == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()