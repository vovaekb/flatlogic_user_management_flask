import os
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from app import app, APP_ROOT
from app.models import Users, Files, Products
from app import CustomError
from app.serializers import ProductsSchema

product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)

class ProductService:
    def get_images():
        print('ProductService.get_images()')
        images_dir = 'public/assets/products/'
        image_files = [f for f in os.listdir(os.path.join(APP_ROOT, images_dir)) if not f.startswith('.')]
        image_files = list(map(lambda f: "%s/assets/products/%s" % (app.config['REMOTE'], f), image_files))
        return image_files

    def get_products():
        print('ProductService.get_products()')
        products = app.session.query(Products)
        products = products.all() # .order_by(Products.createdAt.desc()).all()
        products_dict = products_schema.dump(products)
        print(products_dict)
        return products_dict

    def get_product(product_id):
        print('ProductService.get_products()')
        try:
            product = app.session.query(Products).filter_by(id=product_id).first()
            print(product.title)
            data = product_schema.dump(product)
            print(data)
        except SQLAlchemyError as e:
            print("Unable to get product in database.")
            error = e.__dict__['orig']
            # raise custom error
            raise CustomError({'message': 'Error when reading user in database: %s\n' % error})
        return data

    def update_product(product_id, data):
        print('ProductService.update_product')
        try:
            product = app.session.query(Products).filter_by(id=product_id).first()
            print(product)
            product.title = data['title'] if 'title' in data else None
            product.subtitle = data['subtitle'] if 'subtitle' in data else None
            product.img = data['img'] if 'img' in data else None
            product.price = data['price'] if 'price' in data else None
            product.rating = data['rating'] if 'rating' in data else None
            product.code = data['code'] if 'code' in data else None
            product.hashtag = data['hashtag'] if 'hashtag' in data else None
            product.technology = data['technology'] if 'technology' in data else None
            product.discount = data['discount'] if 'discount' in data else None
            product.description_1 = data['description_1'] if 'description_1' in data else None
            product.description_2 = data['description_2'] if 'description_2' in data else None
            product.updatedAt = func.now()
            app.session.add(product)
            app.session.commit()
        except SQLAlchemyError as e:
            print("Unable to update product to database.")
            error = e.__dict__['orig']
            # raise custom error
            raise CustomError({'message': 'Error when saving rate to database: %s' % error})

    def create_product(data):
        print('ProductService.create_product')
        try:
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
        except SQLAlchemyError as e:
            print("Unable to add order to database.")
            error = e.__dict__['orig']
            # raise custom error
            raise CustomError({'message': 'Error when saving rate to database: %s' % error})
        product = product_schema.dump(product)
        return product

    def delete_product(product_id):
        print('ProductService.delete_product')
        product = app.session.query(Products).filter_by(id=product_id).first()
        print(product)
        app.session.delete(product)
        app.session.commit()
