from flask import json, jsonify
from app import app

def test_create():
    print('testing /users POST')

    # Create new user from sign in form
    with app.test_client() as c:
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTc1NzI4ODksImlhdCI6MTYxNzU1MTI4OSwiaWQiOiJjOTlhYTYyZi1hNTUzLTRkMDktOGZiYS0yYTBhN2Q4MzRkZGQiLCJlbWFpbCI6ImJpbGx5X3hhdmllckBob3N0LmNvbSJ9.7noCzG3ILFYpaVTHy4iXtRZidGSJnlJNvW2FxnxANlE"
        authorization = 'Bearer ' + str(token)

        headers = {
            # 'Content-Type': 'application/json',
            'Authorization': authorization
        }
        rv = c.post('/users', json={
            "id": None,
            "email": "vovaprivalov@gmail.com", # "ralf_stone@host.com",
            "firstName": "Vladimir", # "Ralf",
            "lastName": "Privalov", # "Stone",
            "phoneNumber": "34645346", # "23241945",
            "role": "user",
            "authenticationUid": None,
            "avatar": []
        }, headers=headers)
        # json_data = rv.get_json()
        # print(json_data)
        print(rv.data)
        print('status: ', rv.status_code)

def test_get_all():
    print('testing /users GET')
    with app.test_client() as c:
        rv = c.get('/users', json={})
        print(rv.data)
        print('status: ', rv.status_code)

def test_get_user():
    print('testing /users/<user_id> GET')
    id = "c99aa62f-a553-4d09-8fba-2a0a7d834ddd"
    with app.test_client() as c:
        rv = c.get('/users/%s' % id, json={})
        print(rv.data)
        print('status: ', rv.status_code)

def test_put_user():
    print('testing /users/<user_id> PUT')
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTc1NjU3ODIsImlhdCI6MTYxNzU0NDE4MiwiaWQiOiJjOTlhYTYyZi1hNTUzLTRkMDktOGZiYS0yYTBhN2Q4MzRkZGQiLCJlbWFpbCI6ImJpbGxfeGF2aWVyQGhvc3QuY29tIn0.k7nOe0C3XgFq-FzEZKEJHm5NeckPpz2I3w6QxYHc93k"
    authorization = 'Bearer ' + str(token)
    headers = {
        # 'Content-Type': 'application/json',
        'Authorization': authorization
    }

    id = "c99aa62f-a553-4d09-8fba-2a0a7d834ddd"
    with app.test_client() as c:
        rv = c.put('/users/%s' % id, json={
            "id": id,
            "email": "billy_xavier@host.com",
            "firstName": "Billie",
            "lastName": "Xaviert",
            "phoneNumber": "2211945",
            "role": "admin", 
            "disabled": False,
            "avatar": []
        }, headers=headers)
        print(rv.data)
        print('status: ', rv.status_code)

if __name__ == '__main__':
    test_create()
    # test_get_all()
    # test_get_user()
    #test_put_user()
