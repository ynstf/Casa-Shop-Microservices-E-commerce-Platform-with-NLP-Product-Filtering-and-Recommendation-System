from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)
product_host = 'product'
product_host = '127.0.0.1'
product_host = os.environ.get('PRODUCT_SVC_ADDRESS') or '127.0.0.1'

#to test the server run
@app.route('/', methods=['GET'])
def home():
    return 'Welcome'

#search by product name and describtion
@app.route('/shearch', methods=['GET'])
def show_products():
    # get all products
    products = json.loads(requests.get(f"http://{product_host}:5555/showproducts").content.decode('utf-8'))
    # Access the 'results' key in the products dictionary
    search = request.args.get('search', '')
    products_list = products.get('results', [])
    print(products)
    # Filter products based on the search query
    filtered_products = [product for product in products_list \
                            if (search.lower() in product['name'].lower()) or\
                                (search.lower() in product['description'].lower()) #or\
                                #(search.lower() in product['category'].lower())
                                ]
    #make paginator
    page = int(request.args.get('page', 1))
    items_per_page = 10  # Adjust this based on your preference
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    paginated_products = filtered_products[start_index:end_index]
    # construct result
    result = {
        "results": paginated_products,
        "num_pages": len(filtered_products) // items_per_page ,
        "current_page": page,
        "next_page": page + 1 if end_index < len(filtered_products) else None,
        "previous_page": page - 1 if start_index > 0 else None,
    }
    # sen the result
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5550)
