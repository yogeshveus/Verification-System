from models.user_model import create_user, get_user
from database.db import get_connection

def register_user(name, email, password, role):
    return create_user(name, email, password, role)


def login_user(email, password):
    user = get_user(email, password)

    if user:
        return {"status": True, "role": user[4]}
    else:
        return {"status": False}
    

def get_user_by_email(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()

    conn.close()
    return user