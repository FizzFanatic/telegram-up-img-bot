import telebot
from flask import Flask, request
from psycopg2 import connect

import config  # файл конфигурации с настройками
from telebot import types
import database


# Инициализация бота
bot = telebot.TeleBot(config.Token, threaded=False)
app = Flask(__name__)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    connection = database.get_db_connection()
    if connection:
        bot.reply_to(message, "Бот успешно связался с базой данных")
    else:
        bot.reply_to(message, "Ошибка")


# Обработка вебхука от Telegram
@app.route(f'/webhook_update/{config.SECRET_PATH}', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    print("WebHook получен")  # Проверка на получение запроса
    return 'ok', 200


# # Запуск приложения
# if __name__ == "__main__":
#     app.run()
