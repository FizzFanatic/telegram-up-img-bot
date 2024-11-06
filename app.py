import telebot
from flask import Flask, request
import config  # файл конфигурации с настройками
from telebot import types

# Инициализация бота
bot = telebot.TeleBot(config.Token, threaded=False)
app = Flask(__name__)


# Установка вебхука
bot.remove_webhook()
bot.set_webhook(url=config.WEBHOOK_URL + config.SECRET_PATH)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я твой бот и готов к работе!")


# Обработка вебхука от Telegram
@app.route(f'/webhook_update/{config.SECRET_PATH}', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    print("WebHook received")  # Проверка на получение запроса
    return 'ok', 200

# # Запуск приложения
# if __name__ == "__main__":
#     app.run()
