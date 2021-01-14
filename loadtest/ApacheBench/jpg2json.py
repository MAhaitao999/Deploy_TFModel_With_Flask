import base64
import json


f = open('./dog.jpg', 'rb')
jpg = f.read()
image_databytes = base64.b64encode(jpg)
post_data = {"image": image_databytes.decode('utf-8')}
with open("dog_req.json", 'w', encoding='utf-8') as json_file:
    json.dump(post_data, json_file, ensure_ascii=False)

