from .models import Product, Category
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from .serializers import ProductSerializer, CategorySerializer
import json
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import requests
from product.settings import policy_model_endpoint

# Create your views here.
@api_view(['GET'])
def product_list(request):

    page = request.GET.get('page', 1)  # Get the requested page number, default to 1
    items_per_page = 10  # Set the number of items per page

    products = Product.objects.all()
    paginator = Paginator(products, items_per_page)

    search = request.GET.get("search") if request.GET.get("search") != None else ''

    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)

    serializer = ProductSerializer(paginated_products, many=True)

    # Include pagination details in the response
    response_data = {
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'current_page': paginated_products.number,
        'next_page': paginated_products.next_page_number() if paginated_products.has_next() else None,
        'previous_page': paginated_products.previous_page_number() if paginated_products.has_previous() else None,
        'results': serializer.data,
    }
    return Response(response_data)

@api_view(['GET'])
def product_show(request,pk):
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['GET'])
def product_categories(request,pk):
    product = Product.objects.get(id=pk)
    categories_of_product = product.category.all()
    serializer = CategorySerializer(categories_of_product, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def all_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def product_create(request):
    received_data = json.loads(request.body.decode('utf-8'))
    # Accessing data
    request_data = received_data.get('request', {})
    user_id = received_data.get('user', None)
    images = received_data.get('images', {})
    #extract the path of images
    image = f"products_images/{images['image']}" if images['image'] != "" else "../static/default_product.png"
    product_side = f"/products_images/{images['product_side']}" if images['product_side'] != "" else "../static/default_product.png"
    product_cross = f"/products_images/{images['product_cross']}" if images['product_cross'] != "" else "../static/default_product.png"
    product_with_model = f"/products_images/{images['product_with_model']}" if images['product_with_model'] != "" else "../static/default_product.png"
    product_back = f"/products_images/{images['product_back']}" if images['product_back'] != "" else "../static/default_product.png"

    # Extract products data
    data = {
        "name": request_data['name'][0],
        "short_description": request_data['short_description'][0],
        "description": request_data['description'][0],
        "price": float(request_data['price'][0]),
        "information": request_data['information'][0],
        "shipping_roles": request_data['shipping_roles'][0],
        "image": image,
        "product_side": product_side,
        "product_cross": product_cross,
        "product_with_model": product_with_model,
        "product_back": product_back,
        "user": user_id,
        # Extract category IDs
        'category_ids' : [int(i) for i in request_data['category']]
    }
    
    # the model classifaier endpoint
    api = f"http://{policy_model_endpoint}/predict"
    send_data={"data":str(data["name"])}
    print(send_data)
    # extract data of prediction
    pridection = json.loads(requests.post(url=api,data=json.dumps(send_data)).content.decode('utf8'))

    if pridection['prediction']=='Yes' and pridection['precision']>0.5 :
        # Get the User instance
        user_instance = User.objects.get(pk=user_id)
        # create the product
        product = Product.objects.create(
                user = user_instance,
                name = data['name'],
                short_description = data['short_description'],
                description = data['description'],
                price = data['price'],
                information = data['information'],
                shipping_roles = data['shipping_roles'],
                image = data['image'],
                product_side = data['product_side'],
                product_cross = data['product_cross'],
                product_with_model = data['product_with_model'],
                product_back = data['product_back'],
        )
        # Add categories to the product using set()
        product.category.set(data['category_ids'])
        # return 1 as a flag for passing policy
        return Response(1)
    else :
        # return 0 as a flag for not passing policy
        return Response(0)
