import pandas
import pprint
from pathlib import Path

from sql_functions import (
    SQL_register_new_order
)


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


def add_order_to_busket(busket, recipe, price):
    busket.update({
        len(busket) + 1: {
            'recipe': recipe,
            'price': price
            }
        })
    return busket


def delete_from_busket(busket, id):
    busket.pop(id)
    new_busket = {}
    num = 1
    for item in busket:
        new_busket.update({num: busket[item]})
        num += 1

    return new_busket


def formatting_recipe2txt(recipe: dict):

    text = f"Количество уровней: {recipe['Количество уровней']} \n"
    text += f"Форма: {recipe['Форма']} \n"
    if recipe['Топпинг'] != 'Без топпинга':
        text += f"Топпинг: {recipe['Топпинг']} \n"
    text += f"Ягоды: {recipe['Ягоды']} \n"
    if recipe['Декор']:
        text += f"Декор: {recipe['Декор']} \n"

    return text


def confirm_busket2order(user_id, busket, all_addreses):

    num = 0
    total_price = 0
    order_info_txt = '===== ЗАКАЗ =====' + '\n'
    order_info_txt += '=================' + '\n'
    order_info_txt += '' + '\n'
    for item in busket:
        num += 1
        order_info_txt += 'Торт #{num}:' + '\n'
        order_info_txt += '' + '\n'
        order_info_txt += formatting_recipe2txt(busket[item]['recipe'])
        order_info_txt += f"Cтоимость: {busket[item]['price']}" + '\n'
        order_info_txt += '' + '\n'
        total_price += busket[item]['price']
    order_info_txt += '=================' + '\n'
    order_info_txt += f"ИТОГО: {total_price}" + '\n'
    order_info_txt += '' + '\n'
    order_info_txt += 'Адрес доставки:' + '\n'
    if not all_addreses:
        order_info_txt += 'не указан' + '\n'
    else:
        order_info_txt += all_addreses[0] + '\n'
    order_info_txt += '' + '\n'

    # print(order_info_txt)

    if not all_addreses:
        pass
        # Код для отображения кнопки и функционала "указать адрес"
    else:
        pass
        # Код для отображения кнопки и функционала "изменить адрес"
        #  - Указать новый
        #  - Выбрать из истории

    order_address = ""

    # --- Код для добавления/изменения коментария
    order_comment = ""

    # --- Код для указания даты и времени заказа.
    order_date = ""
    order_time = ""

    # --- Кнопка. Отправить заказ в обработку
    SQL_register_new_order(user_id,  # TG_id
                           recipe=order_info_txt,
                           price=total_price,
                           address=order_address,
                           delivery_date=order_date,
                           delivery_time=order_time,
                           comment=order_comment
                           )


# pp.pprint(read_pricelist_custom())
