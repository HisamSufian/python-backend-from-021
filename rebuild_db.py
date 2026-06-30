import sqlite3

def rebuild_database():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # 1. Drop existing tables if they exist to start fresh
    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("DROP TABLE IF EXISTS suppliers")

    # 2. Create the Suppliers table
    cursor.execute("""
        CREATE TABLE suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_number TEXT
        )
    """)

    # 3. Create the Products table with a Foreign Key
    cursor.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            supplier_id INTEGER,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
        )
    """)

    # 4. Seed initial data into Suppliers
    cursor.execute("INSERT INTO suppliers (name, contact_number) VALUES ('Al Madina Farms', '+971500000001')")
    cursor.execute("INSERT INTO suppliers (name, contact_number) VALUES ('Oasis Organics', '+971500000002')")
    
    # 5. Seed initial data into Products (linking them via supplier_id)
    # Tomatoes (supplier_id = 1 -> Al Madina Farms)
    cursor.execute("INSERT INTO products (name, price, quantity, supplier_id) VALUES ('Tomatoes', 4.50, 100, 1)")
    # Onions (supplier_id = 1 -> Al Madina Farms)
    cursor.execute("INSERT INTO products (name, price, quantity, supplier_id) VALUES ('Onions', 3.00, 250, 1)")
    # Cucumbers (supplier_id = 2 -> Oasis Organics)
    cursor.execute("INSERT INTO products (name, price, quantity, supplier_id) VALUES ('Cucumbers', 5.00, 80, 2)")
    # Avocados (supplier_id = NULL -> No supplier assigned yet)
    cursor.execute("INSERT INTO products (name, price, quantity, supplier_id) VALUES ('Avocados', 12.00, 40, NULL)")

    conn.commit()
    print("Database successfully rebuilt with relational schema!")
    
    # 6. Test Query: Let's see the JOIN in action
    print("\n--- Testing LEFT JOIN Output ---")
    cursor.execute("""
        SELECT products.name, products.price, suppliers.name 
        FROM products
        LEFT JOIN suppliers ON products.supplier_id = suppliers.id
    """)
    
    rows = cursor.fetchall()
    for row in rows:
        print(f"Product: {row[0]} | Price: {row[1]} AED | Supplier: {row[2]}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    rebuild_database()