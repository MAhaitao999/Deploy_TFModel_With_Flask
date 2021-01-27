#! /usr/bin/python
import sys
import json
import os
import time
import base64
from builtins import *

import numpy as np


if sys.version_info > (3, 0):
    import http.client as httplib
else:
    import httplib


if __name__ == '__main__':

    # create connection
    conn = httplib.HTTPConnection('127.0.0.1', 5000)
    header = {'Content-type': 'application/json', "Connection": "keep-alive"}

    # read the image
    f = open('./dog.jpg', 'rb')
    jpg = f.read()
    image_databytes = base64.b64encode(jpg)

    if sys.version_info > (3, 0):
        post_data = {
            "client_id": "xxx",
            "params": [
                {
                    'id': '0',
                    'type': 'jpeg',
                    'data': image_databytes.decode('utf-8'),
                },
                {
                    'id': '1',
                    'type': 'jpeg',
                    'data': image_databytes.decode('utf-8'),
                },
                {
                    'id': '2',
                    'type': 'jpeg',
                    'data': image_databytes.decode('utf-8'),
                },
                {
                    'id': '3',
                    'type': 'jpeg',
                    'data': image_databytes.decode('utf-8'),
                },
                {
                    'id': '3',
                    'type': 'jpeg',
                    'data': image_databytes.decode('utf-8'),
                },
                {
                    'id': '3',
                    'type': 'jpeg',
                    'data': image_databytes.decode('utf-8'),
                },
                {
                    'id': '3',
                    'type': 'jpeg',
                    'data': image_databytes.decode('utf-8'),
                },
                {
                    'id': '3',
                    'type': 'jpeg',
                    'data': image_databytes.decode('utf-8'),
                },
                {
                    'id': '3',
                    'type': 'jpeg',
                    'data': image_databytes.decode('utf-8'),
                },
                {
                    'id': '3',
                    'type': 'jpeg',
                    'data': image_databytes.decode('utf-8'),
                },
                {
                    'id': '3',
                    'type': 'jpeg',
                    'data': image_databytes.decode('utf-8'),
                },
                {
                    'id': '3',
                    'type': 'jpeg',
                    'data': image_databytes.decode('utf-8'),
                },



            ]
        }
    else:
        post_data = {
            "client_id": "xxx",
            "params": [
                {
                    'id': '0',
                    'type': 'jpeg',
                    'data': image_databytes,
                },
                {
                    'id': '1',
                    'type': 'jpeg',
                    'data': image_databytes,
                },
                {
                    'id': '2',
                    'type': 'jpeg',
                    'data': image_databytes,
                },
                {
                    'id': '3',
                    'type': 'jpeg',
                    'data': image_databytes,
                },
                {
                    'id': '3',
                    'type': 'jpeg',
                    'data': image_databytes,
                },
                {
                    'id': '3',
                    'type': 'jpeg',
                    'data': image_databytes,
                },
                {
                    'id': '3',
                    'type': 'jpeg',
                    'data': image_databytes,
                },
                {
                    'id': '3',
                    'type': 'jpeg',
                    'data': image_databytes,
                },
                {
                    'id': '3',
                    'type': 'jpeg',
                    'data': image_databytes,
                },
                {
                    'id': '3',
                    'type': 'jpeg',
                    'data': image_databytes,
                },
                {
                    'id': '3',
                    'type': 'jpeg',
                    'data': image_databytes,
                },
                {
                    'id': '3',
                    'type': 'jpeg',
                    'data': image_databytes,
                },
                {
                    'id': '3',
                    'type': 'jpeg',
                    'data': image_databytes,
                },
                {
                    'id': '3',
                    'type': 'jpeg',
                    'data': image_databytes,
                },
                {
                    'id': '3',
                    'type': 'jpeg',
                    'data': image_databytes,
                },
                {
                    'id': '3',
                    'type': 'jpeg',
                    'data': image_databytes,
                },
            ]
        }

    send_data = post_data

    # jsonify the image
    json_data = json.dumps(send_data, ensure_ascii=False)
    conn.request('POST', '/stream_predict', json_data, header)
    response = conn.getresponse()
    # print("response is: ", response)

    res = response.read()
    res = json.loads(res.decode('utf-8'))  # loads not load
    results = np.array(res['result'])
    # results = results.reshape((6, -1, 85))
    print(results.shape)
