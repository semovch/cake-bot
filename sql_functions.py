import sqlite3


BASE = 'data/bot_database.db'


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
        'contact': result[3]
        }
    return formated_result


'''
user = SQL_get_user_data(898397711)
if user:
    print(f"Welcome back {user['login']}")
else:
    print(f"Привет, user_login! Самые вкусные торты тут! 🍰")
'''
