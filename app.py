import telebot
from flask import Flask, request

import config  # файл конфигурации с настройками
import database

from modules import keyboard
from tools import upscaling_image

# Инициализация бота
bot = telebot.TeleBot(config.Token, threaded=False)
app = Flask(__name__)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    telegram_id = message.from_user.id  # Получаем ID пользователя Telegram

    if database.add_user_to_db(telegram_id):
        message_text = "Вы успешно зарегистрированы!"
        bot.reply_to(message, message_text, reply_markup=keyboard.create_main_menu())
        bot.send_message(message.from_user.id, f"Вам начислено {config.ADD_CREDIT_TO_START} кредитов за первое вступление.")
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


# Обработчик кнопки "Tools"
@bot.message_handler(func=lambda message: message.text == "Tools")
def tools_button(message):
    message_text = "Цены на услуги:\n\nУлучшение фото: 3 кредита\nУдаление метаданных: 1 кредит\nДобавление водяного знака: 1 кредит\n\nВыберите инструмент:"
    bot.reply_to(message, message_text,
                 reply_markup=keyboard.create_inline_tools_buttons()) # клавиатура с инструментами


# Обработчик кнопки "About"
@bot.message_handler(func=lambda message: message.text == "О боте")
def about_button(message):
    message_text = "О боте, раздел в доработке."
    bot.reply_to(message, message_text)


# Обработка вебхука от Telegram
@app.route(f'/webhook_update/{config.SECRET_PATH}', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    print("WebHook получен")  # Проверка на получение запроса
    return 'ok', 200


# Обработчик callback-запросов
@bot.callback_query_handler(func=lambda call: call.data == "enhance_photo")
def handle_enhance_photo(call):
    # Запрашиваем пользователя отправить фото
    # bot.send_message(call.message.chat.id, "Пожалуйста, отправьте фото для улучшения. Форматы: PNG, JPG.")

    # Удаляем предыдущее сообщение
    bot.delete_message(call.message.chat.id, call.message.message_id)

    message_text = ("Улучшение качества фото\n\n"
                    "Мы используем передовой API для повышения качества ваших фотографий.\n\n"
                    "Стоимость услуги: 5 кредитов\n\n"
                    "Если вы хотите улучшить фото, нажмите кнопку «Улучшить». В случае успешного завершения операции с вашего баланса будет списано 5 кредитов.")

    bot.send_message(call.message.chat.id, message_text, reply_markup=keyboard.create_inline_upscaling_foto_buttons())



# После того как фото будет отправлено, вызываем обработчик
@bot.message_handler(content_types=['photo'])
def get_photo_and_process(message):
    message_text = "Обработка началась, с вас списано 5 кредитов"
    bot.reply_to(message, message_text)


# Обработчик callback-запросов
@bot.callback_query_handler(func=lambda call: call.data == "back_to_menu")
def back_to_menu(call):
    # Удаляем предыдущее сообщение
    bot.delete_message(call.message.chat.id, call.message.message_id)

    # Отправляем новое сообщение с кнопками главного меню
    bot.send_message(call.message.chat.id, "Главное меню", reply_markup=keyboard.create_main_menu())



# # Запуск приложения
# if __name__ == "__main__":
#     app.run()
