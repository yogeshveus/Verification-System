import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM products")
rows = cursor.fetchall()

print("Products in DB:")
for row in rows:
    print(row)

conn.close()