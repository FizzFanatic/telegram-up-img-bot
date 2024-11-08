import requests
import config


# Настройки
api_version = 'v1'
api_server = 'api.iloveimg.com'
url = f'https://{api_server}/{api_version}/'
public_key = 'ВАШ_ПУБЛИЧНЫЙ_КЛЮЧ'
token = ''
task = ''
headers = None
server_filename = ''
status = ''


def auth():
    global token, headers
    response = requests.post(url + 'auth', data={'public_key': config.PUBLIC_KEY_I_LOVE_API})
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        token = response.json()['token']
        print(f"Token: {token}")
        headers = {'Authorization': 'Bearer ' + token}
    else:
        print("Ошибка при аутентификации")


def start(tool="upscaleimage"):
    global task
    response = requests.get(url + f'start/{tool}', headers=headers)
    if response.status_code == 200:
        task = response.json()['task']
        print(f"Task: {task}")
    else:
        print("Ошибка при старте задачи")


def upload(file_data):
    global server_filename
    files = {'file': file_data}
    response = requests.post(url + 'upload', data={'task': task}, headers=headers, files=files)
    print(f"Upload status: {response.status_code}")
    if response.status_code == 200:
        server_filename = response.json()['server_filename']
    else:
        print("Ошибка при загрузке файла")


def process(upscale_multiplier=2):
    params = {
        'task': task,
        'tool': 'upscaleimage',
        'files[0][server_filename]': server_filename,
        'files[0][filename]': server_filename,
        'upscale_multiplier': upscale_multiplier
    }
    response = requests.post(url + 'process', data=params, headers=headers)
    if response.status_code == 200:
        return response.json()['status']
    else:
        print("Ошибка при обработке файла")
        return None


def download():
    response = requests.get(url + f'download/{task}', headers=headers)
    if response.status_code == 200:
        return response.content  # Возвращаем файл как байтовый поток
    else:
        print("Ошибка при скачивании файла")
        return None


def delete_task():
    response = requests.post(url + f'task/{task}', headers=headers)
    if response.status_code != 200:
        print("Ошибка при удалении задачи")


def execute(file_data):
    auth()  # Аутентификация
    start()  # Старт задачи
    upload(file_data)  # Загрузка файла
    status = process()  # Обработка изображения
    if status == "ok":
        enhanced_image = download()  # Скачать обработанное изображение
        if enhanced_image:
            return enhanced_image  # Возвращаем изображение
        else:
            print("Не удалось скачать улучшенное изображение.")
    else:
        print("Ошибка при обработке изображения.")
    delete_task()  # Удаляем задачу после завершения



