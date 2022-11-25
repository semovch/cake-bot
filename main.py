import telebot
from telebot import types

from sql_functions import (
    SQL_register_new_user,
    SQL_get_user_data
    )


TOKEN = '5811022670:AAGnEXWfmIgbYxJQ0DHH8mJXTJjtqjhhddI'  # Semen_bot
# TOKEN = '5778281282:AAHAPOtzeP7_qofFxkkb0KxgSJzhMarWn-Y'  # Sergey_bot

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):

    user_name = message.from_user.full_name
    user_login = message.from_user.username
    user_tg_id = message.from_user.id

    user = SQL_get_user_data(user_tg_id)
    if user:    # Если не новый пользователь
        bot.send_message(
            message.chat.id,
            f"Welcome back {user['login']}!",
            )
    else:       # Если пользователь новый
        bot.send_message(
            message.chat.id,
            f"Привет, {user_login}! Самые вкусные торты тут! 🍰",
            )
        SQL_register_new_user(user_name, user_login, user_tg_id)
    button_message(message)


@bot.message_handler(commands=['button'])
def button_message(message):

    catalog = types.KeyboardButton('Каталог')
    contacts = types.KeyboardButton('Контакты')
    basket = types.KeyboardButton('Корзина')
    make_cake = types.KeyboardButton('Создать торт')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(catalog, contacts, basket, make_cake)
    bot.send_message(message.chat.id, 'Главное меню:', reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):

    if message.text == 'Вернуться в основное меню':

        catalog = types.KeyboardButton('Каталог')
        contacts = types.KeyboardButton('Контакты')
        basket = types.KeyboardButton('Корзина')
        make_cake = types.KeyboardButton('Создать торт')

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(catalog, contacts, basket, make_cake)
        bot.send_message(message.chat.id, 'Вы перешли в основное меню:', reply_markup=markup)

    if message.text == 'Создать торт' or message.text == 'Вернуться к созданию торта':

        meringue = types.KeyboardButton('Торт-бeзе')
        cake = types.KeyboardButton('Бисквитный торт')
        waffles = types.KeyboardButton('Вафельной торт')
        cream = types.KeyboardButton('Творожный торт')
        back = types.KeyboardButton('Вернуться в основное меню')

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(meringue, cake, waffles, cream, back)
        bot.send_message(message.chat.id, 'Выбираем основу торта:', reply_markup=markup)

    if message.text == 'Шоколадный крем':
        bot.send_message(message.chat.id, 'Отличный выбор!')

    if message.text == 'Бисквитный торт':

        choco_cream = types.KeyboardButton('Шоколадный крем')
        banana_cream = types.KeyboardButton('Банановый крем')
        berry_cream = types.KeyboardButton('Ягодный крем')
        pistachio_cream = types.KeyboardButton('Фисташковый крем')
        back = types.KeyboardButton('Вернуться к созданию торта')

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(choco_cream, banana_cream, berry_cream, pistachio_cream, back)
        bot.send_message(message.chat.id, 'Определимся с кремом:', reply_markup=markup)

    if message.text == 'Торт-бeзе':

        choco_cream = types.KeyboardButton('Шоколадный крем')
        banana_cream = types.KeyboardButton('Банановый крем')
        berry_cream = types.KeyboardButton('Ягодный крем')
        pistachio_cream = types.KeyboardButton('Фисташковый крем')
        back = types.KeyboardButton('Вернуться к созданию торта')

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(choco_cream, banana_cream, berry_cream, pistachio_cream, back)
        bot.send_message(message.chat.id, 'Определимся с кремом:', reply_markup=markup)


bot.polling(none_stop=True)
