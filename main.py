import keras_cv
import tensorflow as tf
from datetime import datetime
import subprocess
from fastapi import FastAPI, UploadFile
from fastapi.responses import PlainTextResponse

app = FastAPI()

model = keras_cv.models.YOLOV8Detector(
    num_classes=20,
    bounding_box_format="xywh",
    backbone=keras_cv.models.YOLOV8Backbone.from_preset(
        "yolo_v8_m_backbone_coco"
    ),
    fpn_depth=2
)

def predict(file):
    image = tf.convert_to_tensor(file)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.cast(image, tf.float32) 
    image = tf.image.resize(image, (416, 416)) # not sure why this size works
    stacked = tf.stack([image])
    start = datetime.now()
    y_pred = model.predict(stacked)
    stop = datetime.now()
    output = {'prediction time': (stop - start).total_seconds()}
    for k, v in y_pred.items():
        output[k] = v.tolist()
    return output

@app.post('/yolo/')
def upload_file(file: UploadFile):
    return predict(file.file.read())

@app.get('/nvidia-smi/', response_class=PlainTextResponse)
def nvidia_smi():
    proc = subprocess.Popen(['nvidia-smi'], stdout=subprocess.PIPE)
    stdout = proc.stdout.read().decode('utf-8')
    return stdout

@app.get('/devices/')
def devices():
    devices = tf.config.list_physical_devices()
    keys = ['name', 'device_type']
    return [{k: getattr(d, k) for k in keys} for d in devices]
