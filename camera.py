import cv2
import threading
import numpy as np
import os
import pickle
import face_recognition
from imageai.Detection.Custom import CustomObjectDetection
from PIL import Image
import scipy.misc


def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)


class RecordingThread (threading.Thread):
    def __init__(self, name, camera):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True

        self.cap = camera
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter('./static/video.avi',fourcc, 20.0, (640,480))

    def run(self):
        while self.isRunning:
            ret, frame = self.cap.read()
            if ret:
                self.out.write(frame)

        self.out.release()

    def stop(self):
        self.isRunning = False

    def __del__(self):
        self.out.release()

class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        
        self.is_record = False
        self.out = None

        self.recordingThread = None
    
    def __del__(self):
        self.cap.release()
	
    def predict_face(self,rgb,data):
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
	
    def get_frame(self,rate,identify,face_cascade,data,detector):
        ret, frame = self.cap.read()
        frame = rescale_frame(frame, percent=70)
          
        if ret:
            if identify == False:
                ret, jpeg = cv2.imencode('.jpg',frame)
                return jpeg.tobytes()
            image  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)
            for (x, y, w, h) in faces:
                rgb = image[y:y+h, x:x+w]
                name = self.predict_face(rgb,data)
                font = cv2.FONT_HERSHEY_SIMPLEX
                color = (255, 255, 255)
                stroke = 2
                cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                color = (255, 0, 0)
                stroke = 2
                end_cord_x = x + w
                end_cord_y = y + h
                cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
            image  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if rate%6 == 0:
                output,detections = detector.detectObjectsFromImage(input_type="array",input_image=image,output_type="array",thread_safe=True)
                ret, jpeg = cv2.imencode('.jpg', cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
                return jpeg.tobytes()
            else:
                ret, jpeg = cv2.imencode('.jpg', cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                return jpeg.tobytes()
        else:
            return None

    def start_record(self):
        self.is_record = True
        self.recordingThread = RecordingThread("Video Recording Thread", self.cap)
        self.recordingThread.start()

    def stop_record(self):
        self.is_record = False

        if self.recordingThread != None:
            self.recordingThread.stop()

            