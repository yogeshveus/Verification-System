import sqlite3
from config import DATABASE

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS product_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        created_by TEXT NOT NULL,
        is_active INTEGER DEFAULT 1,
        UNIQUE(name, created_by)
    )
''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            itemId INTEGER,
            product_type_id TEXT,
            metadataHash TEXT,
            manufacturer_email TEXT
        )
    ''')

    conn.commit()
    conn.close()

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  
    return conn
