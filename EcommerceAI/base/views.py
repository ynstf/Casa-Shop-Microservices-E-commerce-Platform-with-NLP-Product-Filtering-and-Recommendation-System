from django.shortcuts import render, redirect
import json
from .forms import RegisterForm, ProductForm
from django.contrib import messages
from .models import Product, Category
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate
import requests
import os
from EcommerceAI.settings import auth_endpoint, policy_endpoint, category_endpoint, search_endpoint, product_endpoint
import cloudinary
from cloudinary.uploader import upload

# Create your views here.


#home page
def home(request):
    title = "Casa - Home"    
    categories = Category.objects.all()
    
    page = request.GET.get('page', 1)  # Get the requested page number, default to 1
    search = request.GET.get("search") if request.GET.get("search") != None else ''
    category = request.GET.get("category") if request.GET.get("category") != None else ''
    if category != '':
        cate = Category.objects.get(category_name=category)
        url = f'http://{category_endpoint}/search?category={cate.id}&page={page}'
        myproducts = requests.get(url)
        products = json.loads(myproducts.content.decode('utf-8'))#.get('results', [])
        print(products)

    elif search != '':
        url = f'http://{search_endpoint}/shearch?search={search}&page={page}'
        myproducts = requests.get(url)
        products = json.loads(myproducts.content.decode('utf-8'))#.get('results', [])

    else :
        url = f'http://{product_endpoint}/showproducts?page={page}'
        myproducts = requests.get(url)
        products = json.loads(myproducts.content.decode('utf-8'))

    context = {
        "title": title,
        "products": products['results'],
        "num_pages": products['num_pages'],
        "current_page": products['current_page'],
        "next_page": products['next_page'],
        "previous_page": products['previous_page'],
        "categories": categories,
        "search":search,
        "category": category
    }
    return render(request, "base/home.html", context)

#product page
def product(request,pk):

    #extract all categories in database
    categories_url = f"http://{category_endpoint}/categorie"
    categories = json.loads(requests.get(categories_url).content.decode('utf-8'))

    #extract infos from product api
    product_url = f'http://{product_endpoint}/showproducts/{pk}'
    myproduct = requests.get(product_url)
    product = json.loads(myproduct.content.decode('utf-8'))

    #page name
    title = product['name']

    #semmilare
    # Define the URL and payload
    url = 'http://localhost/predict'
    payload = {'data': title}
    # Send the POST request
    response = requests.post(url, json=payload)
    simmilars = response.json()["precision"]
    simmilar = []
    from .models import Product
    for sm in simmilars:
        if title==sm:
            pass
        else:
            try:
                p = Product.objects.get(name=sm)
                simmilar.append(p)
            except:
                pass
        
            




    #extract the categories in product from category api
    categorie_url = f'http://{category_endpoint}/categorie/{pk}'
    categories_of_product = json.loads(requests.get(categorie_url).content.decode('utf-8'))

    context = {
        "title":title,
        "product":product,
        "categories_of_product":categories_of_product['results'],
        "categories":categories['results'],
        "simmilar":simmilar,
        }
    return render(request,"base/product.html",context)

#registration point
def register(request):
    title = "Create an Account"
    categories = Category.objects.all()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            url = f"http://{auth_endpoint}/api/register"
            myobj = {
                "username":username,
                "email":email,
                "password":password
                    }
            x = requests.post(url, json = myobj)

            if int(x.content) == 1 :
                messages.success(request, 'You are registered successfully, please login to your account')
                return redirect("home")
    else:
        form = RegisterForm()

    context = {
        "title":title,
        "form":form,
        "categories":categories,
    }
    return render(request, "base/register.html", context)

#login point
def Login(request):
    title = "Login"
    categories = Category.objects.all()
    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        url = f"http://{auth_endpoint}/api/login"
        myobj = {
            "username":username,
            "password":password
                }
        x = requests.post(url, json = myobj)
        #if user true
        if int(json.loads(x.content.decode('utf8'))['login']) == 1 :
            #return home page
            #messages.success(request, 'welcome')
            token = json.loads(x.content.decode('utf8'))['jwt']
            response = redirect("home")
            response.set_cookie(key='jwt', value=token, httponly=True)
            #set jwt cookie
            url = f"http://{auth_endpoint}/api/user"
            token = {'jwt':request.COOKIES.get('jwt')}
            x = requests.get(url,data=token)
            #login with user
            #user = User.objects.get(username=json.loads(x.content.decode('utf8'))['username'])
            user_to_log = authenticate(username=username,password=password)
            login(request,user_to_log)
            
            return response
        # if user false
        elif int(json.loads(x.content.decode('utf8'))['login']) == 0 :
            errors = json.loads(x.content.decode('utf8'))['error']
            return render(request,'base/login.html',{'errors':errors})

    context = {
        "title":title,
        "categories":categories,
    }

    return render(request,'base/login.html',context)

#singin in cloudinary
cloudinary.config(
                    cloud_name = 'dbhawzisa',
                    api_key = '874379634442717',
                    api_secret= os.environ.get('api_secret')
                )
#upload to cloud
def upload(img,name):
    # Define upload options
    filename, file_extension = os.path.splitext(name)
    upload_options = {
        "folder": "/media/products_images/",  # Specify the folder
        "public_id": filename, # Specify the public ID (file name)
        "format" : file_extension[1:] ,
        "version": "v1" ,
        #"width": width,  # Specify the width (for resizing)
        #"height": height,  # Specify the height (for resizing)
    }
    cloudinary.uploader.upload(img, **upload_options)
    cloudinary.CloudinaryImage(filename).build_url(version=1)

#add product
@login_required
def listing(request):
    title = 'add new product'
    categories = Category.objects.all()
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            #check if the images are exist
            if 'image' in request.FILES:
                image = request.FILES['image'].name
            else :
                image = ""
            if 'product_side' in request.FILES:
                product_side = request.FILES['product_side'].name
            else :
                product_side = ""
            if 'product_cross' in request.FILES:
                product_cross = request.FILES['product_cross'].name
            else :
                product_cross = ""
            if 'product_with_model' in request.FILES:
                product_with_model = request.FILES['product_with_model'].name
            else :
                product_with_model = ""
            if 'product_back' in request.FILES:
                product_back = request.FILES['product_back'].name
            else :
                product_back = ""

            images = {
                "image" : image,
                "product_side" : product_side,
                "product_cross" : product_cross,
                "product_with_model" : product_with_model,
                "product_back": product_back
            }
            
            url = f'http://{product_endpoint}/postproducts'
            data = {'request':dict(request.POST.lists()),'user':request.user.id,'images':images}
            x = requests.post(url,json=data)
            print(x)
            if int(x.content.decode('utf8')) == 1 :

                #save images
                if image !="":
                    upload(request.FILES['image'],request.FILES['image'].name)
                if product_side !="":
                    upload(request.FILES['product_side'],request.FILES['product_side'].name)
                if product_cross !="":
                    upload(request.FILES['product_cross'],request.FILES['product_cross'].name)
                if product_with_model !="":
                    upload(request.FILES['product_with_model'],request.FILES['product_with_model'].name)
                if product_back !="":
                    upload(request.FILES['product_back'],request.FILES['product_back'].name)
                #redidrect to home
                messages.success(request, 'The product has been created successfully')
                return redirect("home")
            else : #added
                msg = f"This product does not comply with our policy. <a style='color: brown;' href='http://localhost:8000/policy/'><u>Check the policy for details.</u></a> "
                #redidrect to home
                messages.warning(request, msg)
                form = ProductForm(request.POST)
                #return redirect("listing")
                return render(request, "base/listing.html", {'product_form':form,"title":title,"categories":categories})
    else:
        form = ProductForm()

    context = {
        "title":title,
        "product_form":form,
        "categories":categories,
    }
    return render(request, "base/listing.html", context)

#profile page
@login_required
def dashboard(request):
    title = 'Casa - dashboard'

    context = {
        "title":title,
    }
    return render(request, "base/dashboard.html", context)

#policy point
def policy(request):
    title = 'Casa - Policy'
    url = f"http://{policy_endpoint}"
    response = requests.get(url)
    response = (json.loads(response.content))['page']
    content = response.items()
    #print(content)
    context = {
        "title":title,
        "content":content
    }
    return render(request, "base/policy.html", context)

#end sessions
def Logout(request):

    response = redirect("home")
    response.delete_cookie('sessionid')
    response.delete_cookie('jwt')
    return response

#errors pages
def custom_page_not_found_view(request, exception):
    title = 'Page Not Found'
    message = "We couldn't find the page you were looking for. 404"
    context = {
        'title': title,
        'message': message
    }
    return render(request, "errors.html", context, status=404)
def custom_error_view(request, exception=None):
    title = 'Server Error'
    message = 'server error 500'
    context = {
        'title': title,
        'message': message
    }
    return render(request, "errors.html", context, status=500)
def custom_permission_denied_view(request, exception=None):
    title = 'Permission Denied'
    message = 'Permission denied 403'
    context = {
        'title': title,
        'message': message
    }
    return render(request, "errors.html", context, status=403)
def custom_bad_request_view(request, exception=None):
    title = 'Bad Request'
    message = 'bad request 400'
    context = {
        'title': title,
        'message': message
    }
    return render(request, "errors.html", context, status=400)
