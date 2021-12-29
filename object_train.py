from imageai.Detection.Custom import DetectionModelTrainer

trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()
trainer.setDataDirectory(data_directory="dataset")
trainer.setTrainConfig(object_names_array=["gun","knife"], batch_size=4, num_experiments=100, train_from_pretrained_model="pretrained-yolov3.h5")
trainer.trainModel()

trainer.evaluateModel(model_path="dataset/models", json_path="dataset/json/detection_config.json", iou_threshold=0.5, object_threshold=0.3, nms_threshold=0.5)
