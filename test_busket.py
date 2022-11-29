import datetime
import pprint
import json

from sql_functions import (
    # SQL_register_new_user,
    # SQL_get_user_data,
    # SQL_get_orders_by_user,
    SQL_get_addreses
)

from base_functions import (
    # formatting_recipe2txt,
    # confirm_busket2order,
    read_pricelist_custom,
    add_order_to_busket
)


pp = pprint.PrettyPrinter(indent=3)


# ==================  For Busket  ==================
# ==================================================

user_id = 898397711
price_list = read_pricelist_custom()
all_addreses = SQL_get_addreses(user_id)
recipe1 = {
    'Декор': ['Марципан', 'Маршмеллоу'],
    'Количество уровней': '2 уровня',
    'Надпись': False,
    'Топпинг': ['Белый соус', 'Молочный шоколад'],
    'Форма': 'Круг',
    'Ягоды': ['Клубника']}
price1 = 2530

recipe2 = {
    'Декор': ['Марципан'],
    'Количество уровней': '1 уровня',
    'Надпись': False,
    'Топпинг': ['Белый соус', 'Молочный шоколад'],
    'Форма': 'Квадрат',
    'Ягоды': ['Клубника']}
price2 = 1700


busket = {}
busket = add_order_to_busket(busket, recipe1, price1)
busket = add_order_to_busket(busket, recipe2, price2)
# busket = delete_from_busket(busket, 2)

all_addreses = SQL_get_addreses(user_id)

pp.pprint(busket)


# =================  For New Order  =================
# ===================================================

user_id = 898397711
recipe_dict = {
    'Количество уровней': '2 уровня',
    'Форма': 'Круг',
    'Топпинг': ['Белый соус', 'Молочный шоколад'],
    'Ягоды': ['Клубника'],
    'Декор': ['Марципан', 'Маршмеллоу'],
    'Надпись': False
    }
recipe = json.dumps(recipe_dict)
price = 2530
address = 'Nizhniy Novgorod, Lubyanskaya str, 3-11'
delivery_date = datetime.datetime(2022, 12, 31)
delivery_time = datetime.time(18, 00)
comment = 'Код в подъезде 312'
