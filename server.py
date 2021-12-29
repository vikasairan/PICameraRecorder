from flask import Flask, render_template, Response, jsonify, request
from camera import VideoCamera
import cv2
import threading
import numpy as np
import os
import pickle
import face_recognition
from imageai.Detection.Custom import CustomObjectDetection
from PIL import Image
import scipy.misc


video_camera = None
global_frame = None

identify = False

app = Flask(__name__)

def init():
    global face_cascade,data,detector
    face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_default.xml')
    with open("encodings.pickle", 'rb') as f:
        data = pickle.load(f)
    execution_path = os.getcwd()
    detector = CustomObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(os.path.join(execution_path , "dataset//models//detection_model-ex-051--loss-0002.067.h5")) 
    detector.setJsonPath(os.path.join(execution_path , "dataset//json//detection_config.json"))
    detector.loadModel()

@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/record_status', methods=['POST'])

def record_status():
    global video_camera 
    if video_camera == None:
        video_camera = VideoCamera()

    json = request.get_json()

    status = json['status']
    
    if status == "true":
        video_camera.start_record()
        return jsonify(result="started")
    else:
        video_camera.stop_record()
        return jsonify(result="stopped")

@app.route('/identify_status', methods=['POST'])

def identify_status():
    global video_camera 
    if video_camera == None:
        video_camera = VideoCamera()

    json = request.get_json()

    status = json['status']
    
    global identify
    
    if status == "true":
        identify = True
        return jsonify(result="started")
    else:
        identify = False
        return jsonify(result="stopped")

def video_stream():
    global video_camera 
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()
    
    rate = 0
    while True:
        if rate%3==0:
            frame = video_camera.get_frame(rate,identify,face_cascade,data,detector)
        rate = rate + 1
        
        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    init()
    app.run(debug=True, host='0.0.0.0', threaded=True, use_reloader=False)