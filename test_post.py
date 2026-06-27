import urllib.request
import json

"""
# The new stock we want to add
data = {
    "name": "Onions",
    "category": "Vegetable",
    "stock_quantity": 100,
    "price": 2.25
}

# Package it up and send it to your API
req = urllib.request.Request('http://127.0.0.1:5000/api/products', method='POST')
req.add_header('Content-Type', 'application/json')
jsondata = json.dumps(data).encode('utf-8')

# Receive the receipt
response = urllib.request.urlopen(req, jsondata)
print(response.read().decode('utf-8'))



# The newly adjusted stock level
data = {
    "stock_quantity": 60
}

req = urllib.request.Request('http://127.0.0.1:5000/api/products/4', method='PUT')
req.add_header('Content-Type', 'application/json')
jsondata = json.dumps(data).encode('utf-8')

response = urllib.request.urlopen(req, jsondata)
print(response.read().decode('utf-8'))
"""

req = urllib.request.Request('http://127.0.0.1:5000/api/products/4', method='DELETE')
req.add_header('Content-Type', 'application/json')
#jsondata = json.dumps().encode('utf-8')

response = urllib.request.urlopen(req, )
print(response.read().decode('utf-8'))