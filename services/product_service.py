import sqlite3

def save_product(itemId, product_type_id, metadataHash, manufacturer_email):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO products (itemId, product_type_id, metadataHash, manufacturer_email)
        VALUES (?, ?, ?, ?)
    """, (itemId, product_type_id, metadataHash, manufacturer_email))

    conn.commit()
    conn.close()

def get_product_types(user_email):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM product_types WHERE created_by = ?", (user_email,))
    products = cursor.fetchall()
    conn.close()
    return [p[1] for p in products]

def add_product_type(name, user_email):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO product_types (name, created_by) VALUES (?, ?)",
        (name, user_email)
    )

    conn.commit()
    conn.close()

def get_all_products(email):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    cur.execute("""
        SELECT p.itemId, p.product_type_id, p.metadataHash, p.manufacturer_email
        FROM products p
        WHERE p.manufacturer_email = ?
    """, (email,))

    products = cur.fetchall()

    conn.close()
    return products