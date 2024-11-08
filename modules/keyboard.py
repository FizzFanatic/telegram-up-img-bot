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
    # button2 = types.InlineKeyboardButton("Удалить метаданные", callback_data="remove_metadata")
    # button3 = types.InlineKeyboardButton("Водяной знак", callback_data="add_watermark")
    button4 = types.InlineKeyboardButton("🔙 В главное меню", callback_data="back_to_menu")

    # Добавляем каждую кнопку отдельно, чтобы они шли вертикально
    markup.add(button1)
    # markup.add(button2)
    # markup.add(button3)
    markup.add(button4)

    return markup


# Функция для создания кнопки возврата
def create_inline_back_buttons():
    markup = types.InlineKeyboardMarkup()

    # Кнопка "В главное меню"
    button1 = types.InlineKeyboardButton("🔙 В главное меню", callback_data="back_to_menu")

    # Добавляем кнопку в клавиатуру
    markup.add(button1)

    return markup


# Функция для создания кнопок в inline-режиме
def create_inline_upscaling_foto_buttons():
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Улучшить", callback_data="upgrade_foto")
    button2 = types.InlineKeyboardButton("🔙 В главное меню", callback_data="back_to_menu")

    # Добавляем кнопку в клавиатуру
    markup.add(button1)
    markup.add(button2)

    return markup