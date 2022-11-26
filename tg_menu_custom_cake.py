import pandas
import telebot
import pprint
from telebot import types
from pathlib import Path


PRICELIST_CUSTOM = Path.cwd().joinpath('data').joinpath('prices_custom.xlsx')

pp = pprint.PrettyPrinter(indent=3)


def read_excel_column(excelfile, col):
    column = pandas.read_excel(
        excelfile,
        index_col=None,
        usecols=col,
        na_filter=False
        )
    category = column.columns[0]
    column = column.to_dict('tight')['data']

    product_price = {}
    for item in column:
        if len(item[0]) < 1:
            continue
        product_price.update({item[0]: item[1]})
    return {category: product_price}


def read_pricelist_custom():

    file_loc = PRICELIST_CUSTOM

    price_list_custom = {}
    price_list_custom.update(read_excel_column(file_loc, "B:C"))  # Кол-во уров
    price_list_custom.update(read_excel_column(file_loc, "E:F"))  # Форма
    price_list_custom.update(read_excel_column(file_loc, "H:I"))  # Топпинг
    price_list_custom.update(read_excel_column(file_loc, "K:L"))  # Ягоды
    price_list_custom.update(read_excel_column(file_loc, "N:O"))  # Декор

    text_label = pandas.read_excel(
        file_loc,
        index_col=None,
        usecols='Q:Q',
        na_filter=False).to_dict('split')['data'][0][0]

    price_list_custom.update({'Надпись': text_label})  # Надпись

    return price_list_custom


# TOKEN = '5811022670:AAGnEXWfmIgbYxJQ0DHH8mJXTJjtqjhhddI'  # Semen_bot
TOKEN = '5778281282:AAHAPOtzeP7_qofFxkkb0KxgSJzhMarWn-Y'  # Sergey_bot

bot = telebot.TeleBot(TOKEN)


def change_receipe(old_text, group, choice):

    price_list = read_pricelist_custom()

    groups = ['Количество уровней', 'Форма', 'Топпинг',
              'Ягоды', 'Декор', 'Надпись']
    new_text = ""

    if group == 'Levels':
        group = groups[0]
    if group == 'Form':
        group = groups[1]
    if group == 'Topping':
        group = groups[2]
    if group == 'Berries':
        group = groups[3]
    if group == 'Decor':
        group = groups[4]

# ================== Add choice

    add_text = f'{group}: {choice}'
    group_finded = False
    for item in old_text.splitlines():
        if group in item:
            new_text = new_text + add_text + '\n'
            group_finded = True
        else:
            new_text = new_text + item + '\n'
    if not group_finded:
        new_text = new_text + add_text + '\n'

    # ================== Sort lines

    old_text = new_text
    new_text = ''
    price = 0
    lines = [None, None, None, None, None, None]

    for item in old_text.splitlines():
        if groups[0] in item:
            lines[0] = item
            for pItem in price_list['Количество уровней']:
                if pItem in item:
                    price += price_list['Количество уровней'][pItem]

        if groups[1] in item:
            lines[1] = item
            for pItem in price_list['Форма']:
                if pItem in item:
                    price += price_list['Форма'][pItem]

        if groups[2] in item:
            lines[2] = item
            for pItem in price_list['Топпинг']:
                if pItem in item:
                    price += price_list['Топпинг'][pItem]

        if groups[3] in item:
            lines[3] = item
            for pItem in price_list['Ягоды']:
                if pItem in item:
                    price += price_list['Ягоды'][pItem]

        if groups[4] in item:
            lines[4] = item
            for pItem in price_list['Декор']:
                if pItem in item:
                    price += price_list['Декор'][pItem]

        if groups[5] in item:
            lines[5] = item
            for pItem in price_list['Надпись']:
                if pItem in item:
                    price += price_list['Надпись'][pItem]

    new_text = [item for item in lines if item]
    new_text = "\n".join(new_text)
    new_text = new_text + '\n\n'
    new_text = new_text + f'Стоимость: {price} рублей'

    return new_text



@bot.message_handler(commands=['start'])
def start_message(message):
    message_reply(message)


@bot.message_handler(commands=['button'])
def button_message(message):

    make_сustom = types.KeyboardButton('Собрать свой торт')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(make_сustom)
    bot.send_message(message.chat.id, 'Главное меню:', reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):

    if message.text == '/start':
        display = types.InlineKeyboardMarkup(row_width=1)
        btn_create_cake = types.InlineKeyboardButton('Собрать свой торт', callback_data="Собрать свой торт")
        display.add(btn_create_cake)
        display_message = '=========== Текущий рецепт ===========\n\n(ещё ничего не выбрано)'
        bot.send_message(message.chat.id, display_message, reply_markup=display)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    price_list = read_pricelist_custom()

    main_display = types.InlineKeyboardMarkup(row_width=1)
    btn_levels = types.InlineKeyboardButton('Изменить количество уровней', callback_data="Количество уровней")
    btn_shape = types.InlineKeyboardButton('Изменить форму', callback_data="Форма")
    btn_topping = types.InlineKeyboardButton('Изменить топпинг', callback_data="Топпинг")
    btn_berries = types.InlineKeyboardButton('Изменить ягоды', callback_data="Ягоды")
    btn_decor = types.InlineKeyboardButton('Изменить декор', callback_data="Декор")
    btn_label = types.InlineKeyboardButton('Изменить надпись', callback_data="Надпись")
    main_display.add(btn_levels, btn_shape, btn_topping, btn_berries, btn_decor, btn_label)

    if call.message:

        if call.data.split('%')[0] == 'change':
            getting_data = call.data.split('%')
            getting_data.remove(getting_data[0])

            if call.message.text == '=========== Текущий рецепт ===========\n\n(ещё ничего не выбрано)':
                text_message = change_receipe('', getting_data[0], getting_data[1])
            else:
                text_message = change_receipe(call.message.text, getting_data[0], getting_data[1])

            text_message = '=========== Текущий рецепт ===========\n\n' + text_message

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text_message,
                reply_markup=main_display
                )

        if call.data == 'Собрать свой торт':
            text_message = call.message.text
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text_message,
                reply_markup=main_display
                )

        if call.data == "Количество уровней":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = [types.InlineKeyboardButton(f'{key} ({value} р.)', callback_data=f'change%Levels%{key}') for key, value in price_list['Количество уровней'].items()]
            buttons.append(types.InlineKeyboardButton('Вернуться Назад', callback_data="Собрать свой торт"))
            keyboard.add(*buttons)
            text_message = call.message.text
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text_message,
                reply_markup=keyboard
                )

        if call.data == "Форма":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = [types.InlineKeyboardButton(f'{key} ({value} р.)', callback_data=f'change%Form%{key}') for key, value in price_list['Форма'].items()]
            buttons.append(types.InlineKeyboardButton('Вернуться Назад', callback_data="Собрать свой торт"))
            keyboard.add(*buttons)
            text_message = call.message.text
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text_message,
                reply_markup=keyboard
                )

        if call.data == "Топпинг":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = [types.InlineKeyboardButton(f'{key} ({value} р.)', callback_data=f'change%Topping%{key}') for key, value in price_list['Топпинг'].items()]
            buttons.append(types.InlineKeyboardButton('Вернуться Назад', callback_data="Собрать свой торт"))
            keyboard.add(*buttons)
            text_message = call.message.text
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text_message,
                reply_markup=keyboard
                )

        if call.data == "Ягоды":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = [types.InlineKeyboardButton(f'{key} ({value} р.)', callback_data=f'change%Berries%{key}') for key, value in price_list['Ягоды'].items()]
            buttons.append(types.InlineKeyboardButton('Вернуться Назад', callback_data="Собрать свой торт"))
            keyboard.add(*buttons)
            text_message = call.message.text
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text_message,
                reply_markup=keyboard
                )

        if call.data == "Декор":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = [types.InlineKeyboardButton(f'{key} ({value} р.)', callback_data=f'change%Decor%{key}') for key, value in price_list['Декор'].items()]
            buttons.append(types.InlineKeyboardButton('Вернуться Назад', callback_data="Собрать свой торт"))
            keyboard.add(*buttons)
            text_message = call.message.text
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text_message,
                reply_markup=keyboard
                )

        if call.data == "Надпись":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = [types.InlineKeyboardButton('Задать Текст', callback_data="Собрать свой торт")]
            buttons.append(types.InlineKeyboardButton('Вернуться Назад', callback_data="Собрать свой торт"))
            keyboard.add(*buttons)
            text_message = call.message.text
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text_message,
                reply_markup=keyboard
                )


if __name__ == '__main__':
    bot.infinity_polling()
