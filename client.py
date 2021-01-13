import sys
import json
import os
import time
import base64

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
            "image": image_databytes.decode('utf-8'),
        }
    else:
        post_data = {
            "image": image_databytes
        }

    send_data = post_data

    # jsonify the image
    json_data = json.dumps(send_data, ensure_ascii=False)
    conn.request('POST', '/stream_predict', json_data, header)
    response = conn.getresponse()
    # print("response is: ", response)

    res = response.read()
    res = json.loads(res.decode('utf-8'))  # loads not load
    print(res)
