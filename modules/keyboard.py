from telebot import types

# Функция для создания главного меню с кнопками
def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Tools")
    button2 = types.KeyboardButton("Аккаунт")
    button3 = types.KeyboardButton("О боте")
    markup.add(button1, button2, button3)
    return markup

# Функция для создания кнопок в inline-режиме (если нужно)
def create_inline_buttons():
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Подробнее", callback_data="details")
    button2 = types.InlineKeyboardButton("Обновить", callback_data="update")
    markup.add(button1, button2)
    return markup
