import requests
import os

API_KEY = os.getenv("LMWR_API_TOKEN")

# Функция для апскейлинга изображения
def upscale_image(image_file):
    url = "https://api.limewire.com/api/image/upscaling"
    headers = {
        "X-Api-Version": "v1",
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    files = {'image': image_file}
    data = {'upscale_factor': '2'}

    response = requests.post(url, headers=headers, files=files, data=data)
    response_data = response.json()

    if response.status_code == 200 and response_data.get('status') == 'COMPLETED':
        return response_data['data'][0]['asset_url'], response_data.get('credits_used')
    else:
        return None, None

# Основная функция для обработки изображения
def process_image(message, bot):
    try:
        # Загружаем фото пользователя
        file_info = bot.get_file(message.photo[-1].file_id)
        file = bot.download_file(file_info.file_path)

        with open("temp_image.jpg", "wb") as image_file:
            image_file.write(file)

        # Отправляем фото на апскейлинг
        with open("temp_image.jpg", "rb") as img:
            image_url, credits_used = upscale_image(img)

        if image_url:
            # Загружаем улучшенное изображение
            improved_image = requests.get(image_url).content

            # Отправляем улучшенное изображение пользователю
            bot.send_photo(message.chat.id, improved_image, caption=f"Фото улучшено! Кредиты использованы: {credits_used}")
            return "Ваше фото улучшено!"
        else:
            return "Произошла ошибка при улучшении фото."
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"

