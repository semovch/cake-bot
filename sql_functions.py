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


def SQL_put_user_phone(tg_id, phone):
    conn = sqlite3.connect(BASE)
    cur = conn.cursor()
    exec_text = f"UPDATE 'users' SET contact={phone} WHERE tg_id={tg_id} "
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


def SQL_register_new_order(user_id,  # TG_id
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


def SQL_get_orders_by_user(tg_id):     # Получение истории заказов покупателя
    conn = sqlite3.connect(BASE)
    cur = conn.cursor()
    exec_text = f"SELECT * FROM 'orders' WHERE user_id is '{tg_id}'"
    cur.execute(exec_text)
    result = cur.fetchall()
    conn.close()

    if len(result) < 1:
        return False

    formated_result = {}
    for item in result:

        formated_result.update({
            item[0]: {
                'id': item[0],
                'user_id': item[1],
                'recipe': json.loads(item[2]),
                'price': item[3],
                'address': item[4],
                'comment': item[5],
                'delivery_date': item[6],
                'delivery_time': item[7],
                'order_time': item[8],
                'current_status': item[9]
                }
            })
    return formated_result


def SQL_get_addreses(tg_id):
    '''
    Сбор информации о предыдущих заказах пользователя
    Формирование списка всех прошлых адресов доставки
    all_addreses[0] - последний адрес
    Если заказов небыло, то: all_addreses= False
    '''
    all_addreses = []
    old_orders = SQL_get_orders_by_user(tg_id)
    if old_orders:
        old_addreses = [old_orders[item]['address'] for item in reversed(old_orders)]
        for item in old_addreses:
            if item not in all_addreses:
                all_addreses.append(item)
    else:
        all_addreses = False
    return all_addreses
