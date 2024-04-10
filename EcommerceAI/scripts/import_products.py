import csv
from base.models import Product
from random import randint

def handle():
    try:
        file_path = 'data.txt'
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row['Name of Product']
                description = 'lorem epsum'
                price = randint(10,200) # Set the price as needed

                # Create Product object
                product = Product.objects.create(
                    name=name,
                    short_description=name,  # You can set this to the same as the name for now
                    description=description,
                    price=price,
                    # Fill in other fields as needed
                )

                # Save the Product object
                product.save()

    except:
        print("error")


import pandas as pd
from base.models import Product

def fill_product_table():
    df = pd.read_csv('data.txt')
    for index, row in df.iterrows():
        prix = randint(10,200) # Set the price as needed

        product = Product.objects.create(
            name=row['Name of Product'],
            short_description='lorem epsum',
            description='lorem epsum',
            price=prix,

        )
        product.save()

# Call the function to fill the Product table
fill_product_table()
