import os
from sqlalchemy.sql import func
from app import app, APP_ROOT
from app.models import Products
from app.serializers import ProductsSchema

product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)

class ProductService:
    def get_images():
        # print('ProductService.get_images()')
        images_dir = 'public/assets/products/'
        image_files = [f for f in os.listdir(os.path.join(APP_ROOT, images_dir)) if not f.startswith('.')]
        image_files = list(map(lambda f: "%s/assets/products/%s" % (app.config['REMOTE'], f), image_files))
        return image_files

    def get_products():
        # print('ProductService.get_products()')
        products = app.session.query(Products)
        products = products.order_by(Products.id.asc()).all()
        products_dict = products_schema.dump(products)
        print(products_dict)
        return products_dict

    def get_product(product_id):
        print('ProductService.get_product()')
        print(product_id)
        product = app.session.query(Products).filter_by(id=product_id).first()
        print(product.title)
        data = product_schema.dump(product)
        print(data)
        return data

    def update_product(product_id, data):
        # print('ProductService.update_product')
        product = app.session.query(Products).filter_by(id=product_id).first()
        # print(product)
        product.title = data.get('title', None) # data['title'] if 'title' in data else None
        product.subtitle = data.get('subtitle', None) # data['subtitle'] if 'subtitle' in data else None
        product.img = data.get('img', None) # data['img'] if 'img' in data else None
        product.price = data.get('price', None) # data['price'] if 'price' in data else None
        product.rating = data.get('rating', None) # data['rating'] if 'rating' in data else None
        product.code = data.get('code', None) #  data['code'] if 'code' in data else None
        product.hashtag = data.get('hashtag', None) # data['hashtag'] if 'hashtag' in data else None
        product.technology = data.get('technology', None) # data['technology'] if 'technology' in data else None
        product.discount = data.get('discount', None) # data['discount'] if 'discount' in data else None
        product.description_1 = data.get('description_1', None) # data['description_1'] if 'description_1' in data else None
        product.description_2 = data.get('description_2', None) # data['description_2'] if 'description_2' in data else None
        product.updatedAt = func.now()
        app.session.add(product)
        app.session.commit()


    def create_product(data):
        # print('ProductService.create_product')
        product = Products(
            title=data['title'] if 'title' in data else None,
            subtitle = data['subtitle'] if 'subtitle' in data else None,
            img = data['img'] if 'img' in data else None,
            price=data['price'] if 'price' in data else None,
            rating = data['rating'] if 'rating' in data else None,
            code = data['code'] if 'code' in data else None,
            hashtag = data['hashtag'] if 'hashtag' in data else None,
            technology = data['technology'] if 'technology' in data else None,
            discount=data['discount'] if 'discount' in data else None,
            description_1=data['description_1'] if 'description_1' in data else None,
            description_2=data['description_2'] if 'description_2' in data else None,
            updatedAt=func.now()
        )
        app.session.add(product)
        app.session.commit()
        product = product_schema.dump(product)
        return product

    def delete_product(product_id):
        # print('ProductService.delete_product')
        product = app.session.query(Products).filter_by(id=product_id).first()
        print(product)
        app.session.delete(product)
        app.session.commit()
