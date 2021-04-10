import os
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from app import app
from app.models import Users, Files, Products
from app import CustomError
from app.serializers import ProductsSchema

product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)

class ProductService:
    def get_images():
        print('ProductService.get_images()')
        pass

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
            product.title = data['title']
            product.subtitle = data['subtitle']
            product.price = data['price']
            product.rating = data['rating']
            product.code = data['code']
            product.hashtag = data['hashtag']
            product.technology = data['technology']
            product.discount = data['discount']
            product.description_1 = data['description_1']
            product.description_2 = data['description_2']
        except SQLAlchemyError as e:
            print("Unable to update product to database.")
            error = e.__dict__['orig']
            # raise custom error
            raise CustomError({'message': 'Error when saving rate to database: %s' % error})

    def create_product(data):
        print('ProductService.create_product')
        try:
            product = Products(
                title=data['title'],
                subtitle = data['subtitle'],
                price=data['price'],
                rating = data['rating'],
                code = data['code'],
                hashtag = data['hashtag'],
                technology = data['technology'],
                discount=data['discount'],
                description_1=data['description_1'],
                description_2=data['description_2']
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