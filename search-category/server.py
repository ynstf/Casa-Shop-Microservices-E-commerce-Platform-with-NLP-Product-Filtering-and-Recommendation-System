from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)
product_host = os.environ.get('PRODUCT_SVC_ADDRESS') or '127.0.0.1'

#to test the server run
@app.route('/', methods=['GET'])
def home():
    return 'Welcome'

#all categories
@app.route('/categorie', methods=['GET'])
def show_category():
    #get all categories from product api
    cat_response = requests.get(f"http://{product_host}:5555/all_cate")
    cat_data = cat_response.json()
    #return the categories
    result = {
        "results": cat_data
    }
    return jsonify(result)

#get the category of one product
@app.route('/categorie/<id>', methods=['GET'])
def product_category(id):
    #get the category of product (id) from product api
    cat_response = requests.get(f"http://{product_host}:5555/productcategories/{id}/")
    # Check if the request was successful (status code 200)
    if cat_response.status_code == 200:
        # Extract JSON content from the response
        cat_data = cat_response.json()
        result = {
            "results": cat_data
        }
        return jsonify(result)
    else:
        # If the request was not successful, return an error response
        return jsonify({"error": f"Failed to fetch data. Status code: {cat_response.status_code}"}), cat_response.status_code

#search by category
@app.route('/search', methods=['GET'])
def search_category():
    # get all categories from product api
    products = json.loads(requests.get(f"http://{product_host}:5555/showproducts").content.decode('utf-8'))
    # get the category arg (category id)
    try :
        # convert to int
        category = int(request.args.get('category', ''))
    except:
        return jsonify({"error": f"Failed to fetch data. Status code: {500}"})
    # Access the 'results' key in the products dictionary
    products_list = products.get('results', [])
    #get the list of all product with the category id
    filtered_products = [product for product in products_list \
                                if (category in product['category'])
                        ]

    # make paginator
    page = int(request.args.get('page', 1))
    items_per_page = 10  # Adjust this based on your preference
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    paginated_products = filtered_products[start_index:end_index]
    #construct the respons
    result = {
        "results": paginated_products,
        "num_pages": len(filtered_products) // items_per_page ,
        "current_page": page,
        "next_page": page + 1 if end_index < len(filtered_products) else None,
        "previous_page": page - 1 if start_index > 0 else None,
    }
    #send the result
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)
