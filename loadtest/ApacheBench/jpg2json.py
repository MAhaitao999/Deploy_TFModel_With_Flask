import base64
import json


f = open('./dog.jpg', 'rb')
jpg = f.read()
image_databytes = base64.b64encode(jpg)
params = [{'id': '0', 'type': 'jpeg', 'data': image_databytes.decode('utf-8')}]
n_obj = 4
params = n_obj * params
post_data = {'client_id': 'xxx', 'params': params}
with open("dog_req.json", 'w', encoding='utf-8') as json_file:
    json.dump(post_data, json_file, ensure_ascii=False)

