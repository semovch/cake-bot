import telebot
from telebot import types

from sql_functions import (
    SQL_register_new_user,
    SQL_get_user_data
    )


TOKEN = '5811022670:AAGnEXWfmIgbYxJQ0DHH8mJXTJjtqjhhddI'  # Semen_bot
# TOKEN = '5778281282:AAHAPOtzeP7_qofFxkkb0KxgSJzhMarWn-Y'  # Sergey_bot

bot = telebot.TeleBot(TOKEN)


form_buttons = ['Круглый', 'Квадратный', 'Прямоугольный' ]
layer_buttons = ['1 уровень', '2 уровня','3 уровня']   
topping_buttons = ['Без топинга', 'Белый соус','Карамельный сироп', 'Клиновый сироп', 'Клубничный сироп', 'Черничный сироп', 'Молочный шоколад']
berries_button = ['Ежевика', 'Малина', 'Голубика', 'Клубника']

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 2)

    catalog = types.KeyboardButton('Каталог')
    contacts = types.KeyboardButton('Контакты')
    basket = types.KeyboardButton('Корзина')
    make_cake = types.KeyboardButton('Создать торт')

    markup.add(catalog, contacts, basket, make_cake)
    
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
    
@bot.message_handler(content_types=['text'])
def subcategory(message):
    if message.chat.type == 'private':
        if message.text == 'Создать торт':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 1)
            
            meringue = types.KeyboardButton('Торт-бeзе')
            cake = types.KeyboardButton('Бисквитный торт')
            waffles = types.KeyboardButton('Вафельной торт')
            cream = types.KeyboardButton('Творожный торт')
            back = types.KeyboardButton('Вернуться в основное меню')
            
            markup.add(meringue, cake, waffles, cream, back)
            
            bot.send_message(message.chat.id,'На какой основе хотите торт?',reply_markup=markup) 
            
        elif message.text == 'Торт-безе': 
                
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 1)
            
            choco_cream = types.KeyboardButton('Шоколадный крем')
            banana_cream = types.KeyboardButton('Банановый крем')
            berry_cream = types.KeyboardButton('Ягодный крем')
            pistachio_cream = types.KeyboardButton('Фисташковый крем')
            back = types.KeyboardButton('Вернуться в основное меню')
            
            markup.add(choco_cream, banana_cream, berry_cream, pistachio_cream, back)
                
            bot.send_message(message.chat.id,'Отличный выбор! Определимся с кремом:',reply_markup=markup)
            
        elif message.text == 'Вернуться в основное меню': 
                
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 2)

            catalog = types.KeyboardButton('Каталог')
            contacts = types.KeyboardButton('Контакты')
            basket = types.KeyboardButton('Корзина')
            make_cake = types.KeyboardButton('Создать торт')

            markup.add(catalog, contacts, basket, make_cake)
                
            bot.send_message(message.chat.id,'Вы перешли в основное меню:',reply_markup=markup) 
            
'''            
@bot.message_handler(content_types=['text'])
def bisquit_cake(message):
    if message.chat.type == 'private':               
        if message.text == 'Бисквитный торт': 
                
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 1)

            banana_cake = types.KeyboardButton('Банановый бисквит')
            choco_cake = types.KeyboardButton('Шоколадный бисквит')
            berry_cake = types.KeyboardButton('Ягодный бисквит')
            cheese_cake = types.KeyboardButton('Сырный бисквит')
            back = types.KeyboardButton('Вернуться в основное меню')
            
            markup.add(banana_cake, choco_cake, raspberry_cake, cheese_cake, back)
                
            bot.send_message(message.chat.id,'Выберите вид бисквита:', reply_markup=markup)
        
        elif message.text == 'Торт-безе': 
                
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 1)
            
            choco_cream = types.KeyboardButton('Шоколадный крем')
            banana_cream = types.KeyboardButton('Банановый крем')
            berry_cream = types.KeyboardButton('Ягодный крем')
            pistachio_cream = types.KeyboardButton('Фисташковый крем')
            back = types.KeyboardButton('Вернуться в основное меню')
            
            markup.add(choco_cream, banana_cream, berry_cream, pistachio_cream, back)
                
            bot.send_message(message.chat.id,'Отличный выбор! Определимся с кремом:',reply_markup=markup)     
                

                    
        elif message.text == 'Вернуться в основное меню': 
                
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 2)

            catalog = types.KeyboardButton('Каталог')
            contacts = types.KeyboardButton('Контакты')
            basket = types.KeyboardButton('Корзина')
            make_cake = types.KeyboardButton('Создать торт')

            markup.add(catalog, contacts, basket, make_cake)
                
            bot.send_message(message.chat.id,'Вы перешли в основное меню:',reply_markup=markup) 
            
        else:
            bot.send_message(message.chat.id,'Я вас не понимаю')
'''            
bot.polling(none_stop=True)
