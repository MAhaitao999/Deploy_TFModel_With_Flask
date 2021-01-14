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


def preprocess_image(image, target_size):
    if image.mode != 'RGB':
        image = image.convert('RGB')
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
        print('Loading model...')

        with tf.io.gfile.GFile(model_filepath, 'rb') as f:  # tf.gfile.GFile
            graph_def = tf.compat.v1.GraphDef()  # tf.GraphDef
            graph_def.ParseFromString(f.read())

        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')
        self.graph.finalize()

        print('Model loading complete!')
        self.sess = tf.compat.v1.Session(graph=self.graph)  # tf.Session

    def forward(self, feet_data):
        if len(feet_data) != len(self.input_names):
            raise Exception('The number of feed_data must satisfy with the length of list input_names!')
        input_ = {}
        for i in range(len(self.input_names)):
            input_[self.graph.get_tensor_by_name(self.input_names[i])] = feet_data[i]
        output_ = []
        for i in range(len(self.output_names)):
            output_.append(self.graph.get_tensor_by_name(self.output_names[i]))

        results = self.sess.run(output_, feed_dict=input_)
        # print(results[0].shape)

        return results


model_name = './models/frozen_darknet_yolov3_model.pb'
face_mask = BaseAPP(model_name, input_names=['inputs:0'],
                    output_names=['output_boxes:0'])

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    message = request.get_json(force=True)
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    processed_image = preprocess_image(image, target_size=(416, 416))
    outputs = face_mask.forward([processed_image])
    
    return jsonify({'result': outputs[0][0].tolist()})


if __name__ == '__main__':
    app.run(debug=False, threaded=True, processes=1)
