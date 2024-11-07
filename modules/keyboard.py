from telebot import types

# Функция для создания главного меню с кнопками
def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Tools")
    button2 = types.KeyboardButton("Аккаунт")
    button3 = types.KeyboardButton("О боте")
    markup.add(button1, button2, button3)
    return markup


# Функция для создания кнопок в inline-режиме
def create_inline_tools_buttons():
    markup = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton("Улучшить фото", callback_data="enhance_photo")
    button2 = types.InlineKeyboardButton("Удалить метаданные", callback_data="remove_metadata")
    button3 = types.InlineKeyboardButton("Водяной знак", callback_data="add_watermark")

    # Добавляем каждую кнопку отдельно, чтобы они шли вертикально
    markup.add(button1)
    markup.add(button2)
    markup.add(button3)

    return markup

