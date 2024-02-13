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