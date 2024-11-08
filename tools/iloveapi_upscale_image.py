import requests
from io import BytesIO

class ILoveIMG:
    def __init__(self, public_key, tool="upscaleimage"):
        self.public_key = public_key
        self.api_version = 'v1'
        self.api_server = 'api.iloveimg.com'
        self.url = f'https://{self.api_server}/{self.api_version}/'
        self.tool = tool
        self.token = ''
        self.task = ''
        self.headers = None

    def auth(self):
        response = requests.post(self.url + 'auth', data={'public_key': self.public_key})
        if response.status_code == 200:
            self.token = response.json()['token']
            self.headers = {'Authorization': 'Bearer ' + self.token}
        else:
            print("Ошибка при аутентификации")

    def start(self):
        response = requests.get(self.url + f'start/{self.tool}', headers=self.headers)
        if response.status_code == 200:
            self.task = response.json()['task']
        else:
            print("Ошибка при старте задачи")

    def upload(self, input_file):
        with open(input_file, 'rb') as f:
            response = requests.post(self.url + 'upload', data={'task': self.task}, headers=self.headers, files={'file': f})
        if response.status_code == 200:
            return response.json()['server_filename']
        else:
            print("Ошибка при загрузке файла")
            return None

    def process(self, server_filename, upscale_multiplier=2):
        params = {
            'task': self.task,
            'tool': self.tool,
            'files[0][server_filename]': server_filename,
            'files[0][filename]': server_filename,
            'upscale_multiplier': upscale_multiplier
        }
        response = requests.post(self.url + 'process', data=params, headers=self.headers)
        if response.status_code == 200:
            return response.json()['status']
        else:
            print("Ошибка при обработке файла")
            return None

    def download(self):
        response = requests.get(self.url + f'download/{self.task}', headers=self.headers)
        if response.status_code == 200:
            return BytesIO(response.content)  # Возвращаем файл как байтовый поток
        else:
            print("Ошибка при скачивании файла")
            return None
