import sqlite3
import uuid



def add_user(id, username):
    try:
        conn = sqlite3.connect("database_uf.db")
        cursor = conn.cursor()


        row = cursor.execute(f'SELECT * FROM users WHERE id = "{id}"').fetchone()
        if row == None:
            cursor.execute(f"INSERT INTO users VALUES ('{id}', '{username}')")
            conn.commit()
        conn.close()

        return row
    except Exception as e:
        return None
    

def all_user():
    try:
        conn = sqlite3.connect("database_uf.db")
        cursor = conn.cursor()


        # row = cursor.execute(f'SELECT * FROM users WHERE id = "{id}"').fetchone()

        rows = cursor.execute("SELECT id FROM users").fetchall()

        # вывод данных в консоль
        return rows

        # return row
    except Exception as e:
        return None