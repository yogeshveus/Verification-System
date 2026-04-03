from models.user_model import create_user, get_user
from database.db import get_connection
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash


def register_user(name, email, password, role):
    hashed_password = generate_password_hash(password)
    return create_user(name, email, hashed_password, role)

def login_user(email, password):
    user = get_user_by_email(email) 

    if user:
        if check_password_hash(user[3], password): 
            return {"status": True, "role": user[4]}

    return {"status": False}

def get_user_by_email(email):

    #conn = get_connection()
    conn = get_connection(current_app.config['DATABASE'])
    
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()

    conn.close()
    return user