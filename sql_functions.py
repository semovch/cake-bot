import sqlite3


BASE = 'data/bot_database.db'


def register_new_user(name):
    conn = sqlite3.connect(BASE)
    cur = conn.cursor()
    exec_text = f"""
        INSERT INTO 'users' (name)
        VALUES ('{name}')
        """
    cur.execute(exec_text)
    conn.commit()
    conn.close()
