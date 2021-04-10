import os
from flask import json, jsonify
from app import app


def test_get_images():
    print('testing /products/images-list GET')
    with app.test_client() as c:
        rv = c.get('/products', json={})
        print(rv.data)
        print('status: ', rv.status_code)

def test_get_all():
    print('testing /products GET')
    with app.test_client() as c:
        rv = c.get('/products', json={})
        print(rv.data)
        print('status: ', rv.status_code)

def test_get_product():
    print('testing /products/<product_id> GET')
    id = "c99aa62f-a553-4d09-8fba-2a0a7d834ddd"
    with app.test_client() as c:
        rv = c.get('/products/%s' % id, json={})
        print(rv.data)
        print('status: ', rv.status_code)

def test_update_product():
    print('testing /products/<product_id> PUT')
    product_id = "4a652f44-0b07-49a2-a0d2-20dca2b93223"
    with app.test_client() as c:
        rv = c.put('/products/%s' % product_id, json={
            # "id": product_id,
            "title": "",
            "subtitle": "",
            "price": "",
            "rating": "",
            "code": "",
            "hashtag": "",
            "technology": "",
            "discount": "",
            "description_1": "",
            "description_2": "",
        })
        print(rv.data)
        print('status: ', rv.status_code)

def test_create_product():
    print('testing /products POST')

    # Create new user from sign in form
    with app.test_client() as c:
        rv = c.post('/products', json={
            "title": "",
            "subtitle": "",
            "price": "",
            "rating": "",
            "code": "",
            "hashtag": "",
            "technology": "",
            "discount": "",
            "description_1": "",
            "description_2": "",
        })
        print(rv.data)
        print('status: ', rv.status_code)

def test_delete_product():
    print('testing /products/<product_id> DELETE')

    product_id = "4a652f44-0b07-49a2-a0d2-20dca2b93223"
    with app.test_client() as c:
        rv = c.delete('/products/%s' % product_id, json={})
        print(rv.data)
        print('status: ', rv.status_code)

if __name__ == '__main__':
    # test_get_images()
    # test_get_all()
    # test_get_product()
    # test_update_product()
    # test_create_product()
    # test_delete_product()