import os
from flask import json, jsonify
from app import app


def test_get_images():
    print('testing /products/images-list GET')
    with app.test_client() as c:
        rv = c.get('/products/images-list', json={})
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
    id = "1d75b293-46dc-4687-8497-dc0b6146faed"
    with app.test_client() as c:
        rv = c.get('/products/%s' % id, json={})
        print(rv.data)
        print('status: ', rv.status_code)

def test_update_product():
    print('testing /products/<product_id> PUT')
    id = "fa95b6ff-617b-4cb9-a658-d10e396b0ee6"
    with app.test_client() as c:
        data = {
            "discount": None
        }
        '''
        data = {
            # "id": product_id,
            "title": "Curaprox 5460 Ultra Soft",
            "subtitle": "Toothpaste",
            "img": "http://localhost:5000/assets/products/feature_correlation.png",
            "price": 110.0,
            "rating": 0.6,
            "code": 280,
            "hashtag": "curaprox_brush",
            "technology": ["Some technology 2"],
            "discount": 42.5,
            "description_1": "Description 1",
            "description_2": "Description 2",
        }
        '''
        rv = c.put('/products/%s' % id, json=data)
        print(rv.data)
        print('status: ', rv.status_code)

def test_create_product():
    print('testing /products POST')

    # Create new user from sign in form
    with app.test_client() as c:
        data = {
            "discount": None
        }
        '''
        data = {
            "title": "Curaprox Perio Plus+ Support zubní pasta (CHX 0,09%), 75 ml",
            "subtitle": "Toothpaste",
            "img": "http://localhost:5000/assets/products/hxrvDnPTmSU.jpg",
            "price": 130.0,
            "rating": 0.4,
            "code": 240,
            "hashtag": "curaprox_paste",
            "technology": ["Some technology 1"],
            "discount": 25.4,
            "description_1": "Description 1",
            "description_2": "Description 2",
        }
        '''
        rv = c.post('/products', json=data)
        print(rv.data)
        print('status: ', rv.status_code)

def test_delete_product():
    print('testing /products/<product_id> DELETE')

    product_id = "1d75b293-46dc-4687-8497-dc0b6146faed"
    with app.test_client() as c:
        rv = c.delete('/products/%s' % product_id, json={})
        print(rv.data)
        print('status: ', rv.status_code)

if __name__ == '__main__':
    #test_get_images()
    #test_get_all()
    # test_update_product()
    #test_get_product()
    test_create_product()
    #test_delete_product()
    #test_get_product()
