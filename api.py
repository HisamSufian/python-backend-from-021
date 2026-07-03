from flask import Flask, jsonify, request
import sqlite3

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
    # 1. Catch the JSON data sent by the client
    new_item = request.get_json()
    
    # 2. Open the warehouse
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()


    # 1. Check for missing fields
    if 'name' not in new_item or 'price' not in new_item or 'quantity' not in new_item:
        return jsonify({"error": "Missing required fields: name, price, and quantity are mandatory"}), 400

    # 2. Check for invalid data types or negative numbers
    if type(new_item['price']) not in [int, float] or new_item['price'] < 0:
        return jsonify({"error": "Price must be a positive number"}), 400
        
    if type(new_item['quantity']) != int or new_item['quantity'] < 0:
        return jsonify({"error": "Quantity must be a positive integer"}), 400  



    # 3. Securely insert the new item
    cursor.execute(
        "INSERT INTO products (name, category, stock_quantity, price) VALUES (?, ?, ?, ?)", 
        (new_item['name'], new_item['category'], new_item['stock_quantity'], new_item['price'])
    )
    
    # 4. Save and lock up
    conn.commit()
    cursor.close()
    conn.close()
    
    # 5. Send a success receipt back to the client
    return jsonify({"status": "success", "message": f"{new_item['name']} added to inventory!"}), 201


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
