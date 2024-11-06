import telebot
from flask import Flask, request
import config  # файл конфигурации с настройками
from telebot import types
import psycopg2

# Инициализация бота
bot = telebot.TeleBot(config.Token, threaded=False)
app = Flask(__name__)


# Установка вебхука
bot.remove_webhook()
bot.set_webhook(url=config.WEBHOOK_URL + config.SECRET_PATH)

# Подключение к базе данных PostgreSQL
try:
    conn = psycopg2.connect(config.url_database_telegram)
    cursor = conn.cursor()
    print("Подключение к PostgreSQL успешно!")
except Exception as e:
    print("Ошибка при подключении к базе данных:", e)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я твой бот и готов к работе!")


# Обработка вебхука от Telegram
@app.route('/webhook_update' + config.WEBHOOK_URL, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200

# # Запуск приложения
# if __name__ == "__main__":
#     app.run()
