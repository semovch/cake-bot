import sqlite3
import datetime
import json
import pprint
from pathlib import Path


BASE = Path.cwd().joinpath('data').joinpath('bot_database.db')
pp = pprint.PrettyPrinter(indent=3)


def SQL_register_new_user(name, login, tg_id):
    conn = sqlite3.connect(BASE)
    cur = conn.cursor()
    exec_text = f"""
        INSERT INTO 'users' (tg_id, login, name)
        VALUES ('{tg_id}', '{login}', '{name}')
        """
    cur.execute(exec_text)
    conn.commit()
    conn.close()


def SQL_get_user_data(tg_id):

    conn = sqlite3.connect(BASE)
    cur = conn.cursor()
    exec_text = f"SELECT * FROM 'users' WHERE tg_id is '{tg_id}'"
    cur.execute(exec_text)
    result = cur.fetchone()
    conn.close()

    if isinstance(result, type(None)):
        return False

    formated_result = {
        'id': result[0],
        'tg_id': result[1],
        'login': result[2],
        'name': result[3],
        'contact': result[4]
        }
    return formated_result


def SQL_register_new_order(user_id,
                           recipe,
                           price,
                           address,
                           delivery_date,
                           delivery_time,
                           comment=None
                           ):

    conn = sqlite3.connect(BASE)
    cur = conn.cursor()
    order_time = datetime.datetime.now()
    exec_text = f"""
        INSERT INTO 'orders'
            (user_id, recipe, price,
            address, delivery_date,
            delivery_time, comment, order_time, current_status)
        VALUES ('{user_id}', '{recipe}', '{price}',
                '{address}', '{delivery_date}', '{delivery_time}',
                '{comment}', '{order_time}', 'Added New')
        """
    cur.execute(exec_text)
    conn.commit()
    conn.close()


def SQL_get_order_by_id(order_id):

    conn = sqlite3.connect(BASE)
    cur = conn.cursor()
    exec_text = f"SELECT * FROM 'orders' WHERE id is '{order_id}'"
    cur.execute(exec_text)
    result = cur.fetchone()
    conn.close()

    if isinstance(result, type(None)):
        return False

    formated_result = {
        'id': result[0],
        'user_id': result[1],
        'recipe': json.loads(result[2]),
        'price': result[3],
        'address': result[4],
        'comment': result[5],
        'delivery_date': result[6],
        'delivery_time': result[7],
        'order_time': result[8],
        'current_status': result[9]
        }
    return formated_result


# =================================================
# =================  For Testing  =================
# =================================================

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

# SQL_register_new_order(user_id, recipe, price, address, delivery_date, delivery_time, comment)
# pp.pprint(SQL_get_order_by_id(3))
