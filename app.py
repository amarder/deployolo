# https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import keras_cv
import tensorflow as tf
from keras_cv import visualization
import json
from datetime import datetime
import subprocess

model = keras_cv.models.YOLOV8Detector(
    num_classes=20,
    bounding_box_format="xywh",
    backbone=keras_cv.models.YOLOV8Backbone.from_preset(
        "yolo_v8_m_backbone_coco"
    ),
    fpn_depth=2
)

def predict(image_path):
    image = tf.io.read_file(image_path)
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

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            y_pred = predict(path)
            info = f'<pre>{json.dumps(y_pred, indent=4)}</pre>'
            return info
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/nvidia-smi/')
def nvidia_smi():
    proc = subprocess.Popen(['nvidia-smi'], stdout=subprocess.PIPE)
    stdout = proc.stdout.read().decode('utf-8')
    return f'<pre>{stdout}</pre>'

@app.route('/devices/')
def devices():
    devices = tf.config.list_physical_devices()
    return f'<pre>{devices}</pre>'
