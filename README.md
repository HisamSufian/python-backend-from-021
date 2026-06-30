# Inventory Management REST API

A fully functional CRUD API built to manage wholesale physical inventory. This project serves as the foundational architecture for tracking stock levels, categorizing produce, and managing pricing dynamically.

## 🚀 Tech Stack
* **Language:** Python
* **Framework:** Flask
* **Database:** SQLite

## 🏗️ Features
* **RESTful Architecture:** Clean endpoint design for seamless frontend integration.
* **Full CRUD Operations:** * `GET /api/products` - Retrieve all current stock
  * `POST /api/products` - Add new inventory deliveries
  * `PUT /api/products/<id>` - Adjust specific stock quantities dynamically
  * `DELETE /api/products/<id>` - Remove spoiled or discontinued items
* **Persistent Storage:** Data is securely written to a local `.db` file using native SQL queries.

## 🛠️ How to Run Locally
1. Clone this repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment and install Flask: `pip install flask`
4. Run the server: `python api.py`