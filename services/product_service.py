import sqlite3
from config import DATABASE
from flask import current_app

def save_product(itemId, product_type_id, metadataHash, manufacturer_email):
    #conn = sqlite3.connect(DATABASE)
    conn = sqlite3.connect(current_app.config['DATABASE'])
    
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO products (itemId, product_type_id, metadataHash, manufacturer_email)
        VALUES (?, ?, ?, ?)
    """, (itemId, product_type_id, metadataHash, manufacturer_email))

    conn.commit()
    conn.close()

def get_product_types(user_email):
    #conn = sqlite3.connect(DATABASE)
    conn = sqlite3.connect(current_app.config['DATABASE'])
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM product_types WHERE created_by = ? AND is_active = 1", (user_email,))
    products = cursor.fetchall()
    conn.close()
    return [p[1] for p in products]

def add_product_type(name, user_email):
    #conn = sqlite3.connect(DATABASE)
    conn = sqlite3.connect(current_app.config['DATABASE'])
    cursor = conn.cursor()
    cursor.execute(
        "SELECT is_active FROM product_types WHERE name = ? AND created_by = ?",
        (name, user_email)
    )
    result = cursor.fetchone()

    if result:
        cursor.execute(
            "UPDATE product_types SET is_active = 1 WHERE name = ? AND created_by = ?",
            (name, user_email)
        )
    else:
        cursor.execute(
            "INSERT INTO product_types (name, created_by, is_active) VALUES (?, ?, 1)",
            (name, user_email)
        )

    conn.commit()
    conn.close()

def get_all_products(email):
    #conn = sqlite3.connect(DATABASE)
    conn = sqlite3.connect(current_app.config['DATABASE'])
    cur = conn.cursor()

    cur.execute("""
        SELECT p.itemId, p.product_type_id, p.metadataHash, p.manufacturer_email, p.sent
        FROM products p
        WHERE p.manufacturer_email = ?
    """, (email,))

    products = cur.fetchall()

    conn.close()
    return products