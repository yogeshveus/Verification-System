from database.db import get_connection
from flask import current_app

def create_user(name, email, password, role):
    #conn = get_connection()
    conn = get_connection(current_app.config['DATABASE'])
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
            (name, email, password, role)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def get_user(email, password):
    #conn = get_connection()
    conn = get_connection(current_app.config['DATABASE'])
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )
    user = cur.fetchone()
    conn.close()

    return user