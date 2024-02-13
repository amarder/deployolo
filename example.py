import keras_cv
import tensorflow as tf
from keras_cv import visualization

model = keras_cv.models.YOLOV8Detector(
    num_classes=20,
    bounding_box_format="xywh",
    backbone=keras_cv.models.YOLOV8Backbone.from_preset(
        "yolo_v8_m_backbone_coco"
    ),
    fpn_depth=2
)

def load_image(image_path):
    image = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(image, channels=3)
    return tf.cast(image, tf.float32) 

image = load_image('maxresdefault.jpg')
image = tf.image.resize(image, (416, 416)) # not sure why this size works
stacked = tf.stack([image, image])
print(stacked.shape)
y_pred = model.predict(stacked)
y_pred = keras_cv.bounding_box.to_ragged(y_pred)
visualization.plot_bounding_box_gallery(
    stacked,
    value_range=(0, 255),
    bounding_box_format="xywh",
    y_pred=y_pred,
    scale=4,
    rows=1,
    cols=2,
    show=True,
    font_scale=0.7,
    # class_mapping=class_mapping,
)


# visualize_detections(model, dataset=val_ds, bounding_box_format="xywh")
