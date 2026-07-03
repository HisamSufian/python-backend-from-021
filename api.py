import os
from flask import Flask, jsonify, request
import sqlite3
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Access the secret key
SECRET_KEY = os.getenv("WAREHOUSE_SECRET_KEY")

# Temporary print statement to verify it's working (we'll remove this later)
print(f"\n[SECURITY] Loaded Secret Key: {SECRET_KEY}\n")


app = Flask(__name__)

# get method
@app.route('/api/products', methods=['GET'])
def get_products():
    # 1. Open the warehouse
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # 2. Execute the LEFT JOIN query
    cursor.execute("""
        SELECT products.id, products.name, products.price, products.quantity, suppliers.name 
        FROM products
        LEFT JOIN suppliers ON products.supplier_id = suppliers.id
    """)
    items = cursor.fetchall()

    # 3. Lock the doors
    cursor.close()
    conn.close()

    # 3. Format the data into clean JSON
    inventory_list = []
    for row in items:
        inventory_list.append({
            "id": row[0],
            "name": row[1],
            "price": row[2],
            "quantity": row[3],
            "supplier": row[4] # This will beautifully output 'null' in JSON for the Avocados!
        })

    # 4. Hand the data out the drive-thru window
    return jsonify(inventory_list), 200


# post method 
@app.route('/api/products', methods=['POST'])
def add_product():
    # --- 1. The Digital Bouncer ---
    provided_key = request.headers.get('X-API-Key')
    if provided_key != SECRET_KEY:
        return jsonify({"error": "Unauthorized: Invalid or missing API Key"}), 401

    data = request.get_json()

    # --- 2. Input Validation ---
    if 'name' not in data or 'price' not in data or 'quantity' not in data:
        return jsonify({"error": "Missing required fields: name, price, and quantity are mandatory"}), 400

    if type(data['price']) not in [int, float] or data['price'] < 0:
        return jsonify({"error": "Price must be a positive number"}), 400
        
    if type(data['quantity']) != int or data['quantity'] < 0:
        return jsonify({"error": "Quantity must be a positive integer"}), 400

    # --- 3. Database Insertion (New Relational Schema) ---
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO products (name, price, quantity, supplier_id) 
        VALUES (?, ?, ?, ?)
    """, (data['name'], data['price'], data['quantity'], data.get('supplier_id')))
    
    conn.commit()
    new_id = cursor.lastrowid
    
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Product added successfully", "id": new_id}), 201

    

# update method
@app.route('/api/products/<int:item_id>', methods=['PUT'])
def update_stock(item_id):
    # 1. Catch the incoming data (how much stock to add/subtract)
    update_data = request.get_json()
    new_stock_value = update_data['stock_quantity']
    
    # 2. Open the warehouse
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # 3. Update only the specific item using its ID
    cursor.execute(
        "UPDATE products SET stock_quantity = ? WHERE id = ?", 
        (new_stock_value, item_id)
    )
    
    # 4. Save and lock up
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"status": "success", "message": f"Item ID {item_id} stock updated to {new_stock_value}!"}), 200



# delete method
@app.route('/api/products/<int:item_id>', methods=['DELETE'])
def delete_stock(item_id):
    
    # 2. Open the warehouse
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # 3. Update only the specific item using its ID
    cursor.execute(
        "DELETE FROM products WHERE id = ?", 
        (item_id,)
    )
    
    # 4. Save and lock up
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"status": "success", "message": f"Item ID {item_id} stock deleted!"}), 200




if __name__ == '__main__':
    app.run(debug=True)
