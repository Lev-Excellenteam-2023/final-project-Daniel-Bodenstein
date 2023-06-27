import time

import requests
import json
from datetime import datetime
from status import Status


class FileUploadClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def upload(self, file_path):
        url = self.base_url + '/upload'
        with open(file_path, 'rb') as file:
            response = requests.post(url, files={'file': file})
            if response.status_code == 200:
                response = json.loads(response.text)
                uid = response['UID']
                return uid
            else:
                raise Exception(f"File upload failed with status code: {response.status_code}")

    def status(self, uid):
        url = self.base_url + '/status'
        params = {'uid': uid}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = json.loads(response.text)
            status = data['status']

            if status == 'pending':
                return Status(status, None, None, None, uid)
            filename = data['original name']
            timestamp = datetime.strptime(data['timestamp'], '%H-%M-%S')
            explanation = data['data']
            return Status(status, filename, timestamp, explanation, uid)
        else:
            raise Exception(f"Status retrieval failed with status code: {response.status_code}/"
                            f"{response.text}")


if __name__ == '__main__':
    client = FileUploadClient('http://127.0.0.1:5000')
    uid = client.upload('C:\\Users\\User\\Desktop\\exelenteam\\project\\End of course exercise - kickof - upload')

    s = client.status(uid)

    while not s.is_done():
        print('send')
        time.sleep(5)
        s = client.status(uid)

    print(s)
