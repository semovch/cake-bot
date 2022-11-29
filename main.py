import telebot
from telebot import types

from sql_functions import (
    SQL_register_new_user,
    SQL_get_user_data,
    SQL_put_user_phone
    )


TOKEN = '5811022670:AAGnEXWfmIgbYxJQ0DHH8mJXTJjtqjhhddI'

bot = telebot.TeleBot(TOKEN)


form_buttons = ['Круглый', 'Квадратный', 'Прямоугольный']
layer_buttons = ['1 уровень', '2 уровня', '3 уровня']
topping_buttons = ['Без топинга', 'Белый соус', 'Карамельный сироп', 'Клиновый сироп', 'Клубничный сироп', 'Черничный сироп', 'Молочный шоколад']
berries_button = ['Ежевика', 'Малина', 'Голубика', 'Клубника']


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    catalog = types.KeyboardButton('Каталог')
    contacts = types.KeyboardButton('Контакты')
    basket = types.KeyboardButton('Корзина')
    make_cake = types.KeyboardButton('Создать торт')
    button_phone = types.KeyboardButton(text='Отправить свой номер телефона', request_contact=True)

    markup.add(catalog, contacts, basket, make_cake, button_phone)

    user_name = message.from_user.full_name
    user_login = message.from_user.username
    user_tg_id = message.from_user.id

    user = SQL_get_user_data(user_tg_id)
    if user:    # Если не новый пользователь
        bot.send_message(
            message.chat.id,
            f"Welcome back {user['login']}!",
            reply_markup=markup
            )
    else:       # Если пользователь новый
        bot.send_message(
            message.chat.id,
            f"Привет, {user_login}! Самые вкусные торты тут! 🍰",
            reply_markup=markup
            )
        SQL_register_new_user(user_name, user_login, user_tg_id)


@bot.message_handler(content_types=['contact'])
def read_contact_phone(message):
    SQL_put_user_phone(message.from_user.id, message.contact.phone_number)


@bot.message_handler(content_types=['text'])
def subcategory(message):
    if message.chat.type == 'private':
        if message.text == 'Создать торт':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

            layer = types.KeyboardButton('1 уровень')
            two_layers = types.KeyboardButton('2 уровня')
            three_layers = types.KeyboardButton('3 уровня')
            back = types.KeyboardButton('Вернуться в основное меню')

            markup.add(layer, two_layers, three_layers, back)

            bot.send_message(message.chat.id, 'Создайте свой торт! Укажите количество уровней торта:', reply_markup=markup)
        elif message.text in layer_buttons:

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

            square = types.KeyboardButton('Квадратный')
            circle = types.KeyboardButton('Круглый')
            rectangle = types.KeyboardButton('Прямоугольный')
            back = types.KeyboardButton('Вернуться в основное меню')

            markup.add(square, circle, rectangle, back)

            bot.send_message(message.chat.id,'Отлично! Теперь определимся с формой торта:', reply_markup=markup)

        elif message.text in form_buttons:

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

            without_topping = types.KeyboardButton('Без топинга')
            white_sauce = types.KeyboardButton('Белый соус')
            caramel = types.KeyboardButton('Карамельный сироп')
            maple = types.KeyboardButton('Клиновый сироп')
            strawberry = types.KeyboardButton('Клубничный сироп')
            bilberry = types.KeyboardButton('Черничный сироп')
            milk_choco = types.KeyboardButton('Молочный шоколад')
            back = types.KeyboardButton('Вернуться в основное меню')
            markup.add(without_topping, white_sauce, caramel, maple, strawberry, bilberry, milk_choco, back)

            bot.send_message(message.chat.id,'Хороший выбор) Как на счет топинга?', reply_markup=markup)

        elif message.text in topping_buttons:

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

            additionally = types.KeyboardButton('Дополнительно')
            ordering = types.KeyboardButton('Оформить заказ')
            back = types.KeyboardButton('Вернуться в основное меню')

            markup.add(additionally, ordering, back)

            bot.send_message(message.chat.id,
                             'Торт собран:) Чтобы добавить еще компонентов в свой торт нажмите "Дополнительно", для заказа - "Оформить заказ"',
                             reply_markup=markup)

        elif message.text == 'Дополнительно':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

            barries = types.KeyboardButton('Ягоды')
            decor = types.KeyboardButton('Декор')
            lettering = types.KeyboardButton('Надпись')
            back = types.KeyboardButton('Назад')

            markup.add(barries, decor, lettering, back)

            bot.send_message(message.chat.id,'Укажите дополнения:', reply_markup=markup)

        elif message.text == 'Ягоды':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

            blackberries = types.KeyboardButton('Ежевика')
            raspberries = types.KeyboardButton('Малина')
            blueberries = types.KeyboardButton('Голубика')
            strawberries = types.KeyboardButton('Клубника')
            back = types.KeyboardButton('Назад')

            markup.add(blackberries, raspberries, blueberries, strawberries, back)

            bot.send_message(message.chat.id,'Добавь ягод:', reply_markup=markup)

        elif message.text == 'Назад':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

            additionally = types.KeyboardButton('Дополнительно')
            ordering = types.KeyboardButton('Оформить заказ')
            back = types.KeyboardButton('Вернуться в основное меню')

            markup.add(additionally, ordering, back)

            bot.send_message(message.chat.id, 'Основа торта готова:) Чтобы добавить еще компонентов в свой торт нажмите "Дополнительно" ', reply_markup=markup)

        if message.text == 'Вернуться в основное меню': 

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 2)

            catalog = types.KeyboardButton('Каталог')
            contacts = types.KeyboardButton('Контакты')
            basket = types.KeyboardButton('Корзина')
            make_cake = types.KeyboardButton('Создать торт')

            markup.add(catalog, contacts, basket, make_cake)

            bot.send_message(message.chat.id,'Вы перешли в основное меню:', reply_markup=markup)


'''
elif message.text == 'Оформить заказ':

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 2)


    markup.add( )

    bot.send_message(message.chat.id,'Укажите ваши данные:',reply_markup=markup)
'''

bot.polling(none_stop=True)
