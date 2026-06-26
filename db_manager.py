import sqlite3

conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        stock_quantity INTEGER DEFAULT 0,
        price REAL
    )
"""
)

cursor.execute("INSERT INTO products(name, category, stock_quantity, price) VALUES(?,?,?,?)", ('Tomatoes', 'Vegetable', 50, 4.50))
cursor.execute("INSERT INTO products(name, category, stock_quantity, price) VALUES(?,?,?,?)", ('Apple', 'Fruit', 3, 24.50))
cursor.execute("INSERT INTO products(name, category, stock_quantity, price) VALUES(?,?,?,?)", ('Mangoes', 'Fruit', 40, 11))

cursor.execute("SELECT * FROM products WHERE stock_quantity > 5")

storage = cursor.fetchall()

print(storage)

conn.commit()
cursor.close()
conn.close()
