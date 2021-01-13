from locust import HttpLocust, TaskSet, task
import json
import base64


def img2json(path):
    f = open(path, 'rb')
    jpg = f.read()
    image_databytes = base64.b64encode(jpg)
    post_data = {"image": image_databytes.decode('utf-8')}
    send_data = post_data
    json_data = json.dumps(send_data, ensure_ascii=False)

    return json_data


jsonData = img2json('dog.jpg')


class MyTaskSet(TaskSet):

    @task(99)  # 99代表权重
    def create_post(self):
        global jsonData
        response = self.client.request(
            method="POST",
            url='/stream_predict',
            data=jsonData,
            headers={'Content-type': 'application/json', "Connection": "keep-alive"})
        print("LOGIN RESULT:", response.status_code, response.content)
        if response.status_code == 200:
            print(response)
            

    @task(1)  # 1代表权重
    def create_get(self):
        response = self.client.get("/")
        print("Response status code:", response.status_code)
        print("Response content:", response.text)


class MyLocust(HttpLocust):
    task_set = MyTaskSet
    min_wait = 1   # 同一个用户隔最短多长时间再发送一次请求 
    max_wait = 10  # 同一个用户隔最长多长时间再发送一次请求
