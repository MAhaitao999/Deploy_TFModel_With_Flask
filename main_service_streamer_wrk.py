"""
Created by HenryMa on 2021/1/12
"""

__author__ = 'HenryMa'


import io
import base64
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from builtins import *

import cv2
import numpy as np
import tensorflow as tf
from flask import Flask
from flask import request
from flask import jsonify
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

from service_streamer import ThreadedStreamer


def preprocess_image(image, target_size):
    if image.mode != 'RGB':
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    return image


class BaseAPP(object):
    def __init__(self, model_filepath, input_names, output_names):
        # The file path model
        self.model_filepath = model_filepath
        # Create a new a graph
        self.graph = tf.Graph()
        self.sess = None
        # The name list of inputs
        self.input_names = input_names
        # The output list of outputs
        self.output_names = output_names
        # Initialize the model
        self.load_graph(model_filepath=self.model_filepath)

    def load_graph(self, model_filepath):
        """
        Load trained model.
        """
        print("Loading model...")

        with tf.io.gfile.GFile(model_filepath, 'rb') as f:  # tf.gfile.GFile
            graph_def = tf.compat.v1.GraphDef()  # tf.GraphDef
            graph_def.ParseFromString(f.read())

        with self.graph.as_default():
            tf.import_graph_def(graph_def, name="")
        self.graph.finalize()

        print("Model loading complete!")
        self.sess = tf.compat.v1.Session(graph=self.graph)  # tf.Session

    def forward(self, feet_data):
        print("feet_data is:===========================")
        print(feet_data[0].shape)
        if len(feet_data) != len(self.input_names):
            raise Exception("输入个数和喂给的数据个数必须一致")
        input_ = {}
        for i in range(len(self.input_names)):
            input_[self.graph.get_tensor_by_name(self.input_names[i])] = feet_data[i]
        output_ = []
        for i in range(len(self.output_names)):
            output_.append(self.graph.get_tensor_by_name(self.output_names[i]))

        results = self.sess.run(output_, feed_dict=input_)
        print(results)

        return results


model_name = "frozen_darknet_yolov3_model.pb"
test_image = "dog.jpg"
face_mask = BaseAPP(model_name, input_names=['inputs:0'],
                    output_names=['output_boxes:0'])

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == "POST":
        file = request.files['file']
        img_bytes = file.read()
    image = Image.open(io.BytesIO(img_bytes))
    processed_image = preprocess_image(image, target_size=(416, 416))
    print("=================", os.getpid())
    print("Hello world")
    face_mask.forward([processed_image])
    return jsonify("hello world")


def batch_prediction(image_bytes_batch):
    image_tensors = [preprocess_image(image, target_size=(416, 416)) for image in image_bytes_batch]
    tensor = np.concatenate(image_tensors, axis=0)
    print("tensor's shape is: ", tensor.shape)
    outputs = face_mask.forward([tensor])
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print("本批次有多少个output: ", len(outputs))
    print("非常重要的结果outputs is: ", outputs[0].shape)
    print(outputs[0][0].shape)
    return [outputs[0][i] for i in range(len(outputs[0]))]
    # return ["hello world" for i in range(len(outputs[0]))]


streamer = ThreadedStreamer(batch_prediction, batch_size=8)


@app.route('/stream_predict', methods=['POST'])
def stream_predict():
    if request.method == "POST":
        file = request.files['file']
        img_bytes = file.read()
    image = Image.open(io.BytesIO(img_bytes))
    results = streamer.predict([image])[0]
    print("*********************results is:", results.shape)

    return jsonify({"result": results.tolist()})


@app.route('/', methods=['GET'])
def index():
    return jsonify("Hello index!")


if __name__ == "__main__":
    with open(r"dog.jpg", "rb") as f:
        image_bytes = f.read()
    image = Image.open(io.BytesIO(image_bytes))
    batch_result = batch_prediction([image] * 8)
    app.run(debug=False, threaded=True, port=5000)