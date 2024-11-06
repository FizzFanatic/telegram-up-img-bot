import telebot
from flask import Flask, request

import config  # файл конфигурации с настройками
import database

from modules import keyboard

# Инициализация бота
bot = telebot.TeleBot(config.Token, threaded=False)
app = Flask(__name__)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    telegram_id = message.from_user.id  # Получаем ID пользователя Telegram

    if database.add_user_to_db(telegram_id):
        message_text = "Вы успешно зарегистрированы!\n\nВам начислено 5 кредитов за первое вступление.\n\n"
        bot.reply_to(message, message_text, reply_markup=keyboard.create_main_menu())
    else:
        message_text = "Вы уже зарегистрированы.\nГлавное меню."
        bot.reply_to(message, message_text, reply_markup=keyboard.create_main_menu())


# Обработчик кнопки "Аккаунт"
@bot.message_handler(func=lambda message: message.text == "Аккаунт")
def show_account_info(message):
    telegram_id = message.from_user.id  # Получаем ID пользователя Telegram
    balance = database.get_user_balance(telegram_id)  # Получаем баланс из базы

    if balance is not None:
        bot.reply_to(message, f"Ваш ID: {telegram_id}\nБаланс кредитов: {balance}", reply_markup=keyboard.create_main_menu())
    else:
        bot.reply_to(message, "Ошибка при получении данных о балансе.", reply_markup=keyboard.create_main_menu())


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
