import os
from flask import render_template, Blueprint, request, jsonify, Response
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from app import app, APP_ROOT
from app.models import Products
from app.serializers import ProductsSchema

# CONFIG
products_blueprint = Blueprint('products', __name__) # , template_folder='templates')
product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)

# ROUTES
@products_blueprint.route('/products', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        text = 'OK'
        return Response(text, status=200)
    else:
        products = app.session.query(Products)
        products = products.order_by(Products.createdAt.desc()).all()
        print(products)
        ...
        # data = {
        #     'rows': products_list,
        #     'count': len(products_list)
        # }
        # return jsonify(data)
        text = 'OK'
        return Response(text, status=200)

@products_blueprint.route('/products/<product_id>', methods=['GET', 'PUT', 'DELETE'])
def product(product_id):
    if request.method == 'PUT':
        text = 'OK'
        return Response(text, status=200)
    elif request.method == 'DELETE':
        text = 'OK'
        return Response(text, status=200)
    elif request.method == 'GET':
        text = 'OK'
        return Response(text, status=200)