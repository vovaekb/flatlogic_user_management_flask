import os
from flask import render_template, Blueprint, request, jsonify, Response
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from app import app, APP_ROOT
from app.models import Products
from app.serializers import ProductsSchema
from app.products.services import ProductService

# CONFIG
products_blueprint = Blueprint('products', __name__) # , template_folder='templates')
product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)

# ROUTES
@products_blueprint.route('/products/images-list', methods=['GET'])
def images_list():
    payload = ProductService.get_images()
    return jsonify(payload)


@products_blueprint.route('/products', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        product = ProductService.create_product(data)
        return jsonify(product)
    else:
        payload = ProductService.get_products()
        return jsonify(payload)


@products_blueprint.route('/products/<product_id>', methods=['GET', 'PUT', 'DELETE'])
def product(product_id):
    if request.method == 'PUT':
        data = request.get_json()
        ProductService.update_product(product_id, data)
        text = 'OK'
        return Response(text, status=200)
    elif request.method == 'DELETE':
        ProductService.delete_product(product_id)
        text = 'OK'
        return Response(text, status=200)
    elif request.method == 'GET':
        product = ProductService.get_product(product_id)
        return jsonify(product)
