import os
import io
from flask import json, jsonify
from app import app

AUTH_TOKEN = ""

def get_token():
    print('get_token')
    token_file = 'auth_token.txt'
    with open(token_file, 'r') as f:
        os.environ["AUTH_TOKEN"] = f.readline()
    print(os.environ["AUTH_TOKEN"])
    print('')


def upload_file():
    print('testing /files/upload/users/avatar POST')
    print(os.environ["AUTH_TOKEN"])
    with app.test_client() as c:
        token = os.environ["AUTH_TOKEN"]
        data = {
                'filename': 'eb4b4851-a5e4-483a-a1d0-3f3feedae3a6.png',
                'file': (io.BytesIO(b"abcdef"), 'test1.png')
                }
        rv = c.post('/files/upload/users/avatar',
                content_type='multipart/form-data',
                data = data)
        print(rv.data)
        print('status: ', rv.status_code)

def test_create():
    print('testing /users POST')
    print(os.environ["AUTH_TOKEN"])

    # Create new user from sign in form
    with app.test_client() as c:
        token = os.environ["AUTH_TOKEN"]
        print(token)
        authorization = 'Bearer ' + str(token)
        headers = {
            # 'Content-Type': 'application/json',
            'Authorization': authorization
        }
        rv = c.post('/users', json={
            "id": None,
            "email": "marcel_flann@host.com", # "vovaprivalov@gmail.com", # "ralf_stone@host.com",
            "firstName": None, # "Vladimir", # "Ralf",
            "lastName": None, # "Privalov", # "Stone",
            "phoneNumber": "6733292", # "34645346", # "23241945",
            "role": "user",
            "authenticationUid": None,
            "disabled": True,
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
    token = os.environ["AUTH_TOKEN"]
    print(token)
    authorization = 'Bearer ' + str(token)
    headers = {
        # 'Content-Type': 'application/json',
        'Authorization': authorization
    }

    user_id = "d17014dd-7ce3-4520-9faf-3d66612d2d8c" # "4a58a55d-866b-4dba-9ea5-0f00670b5882"
    with app.test_client() as c:
        rv = c.put('/users/%s' % user_id, json={
            "id": user_id,
            "email": "marcel_flann18@host.com", # "billy_xavier@host.com",
            "firstName": "Kenny", # "Simon",
            "lastName": None, # "Xaviert",
            "phoneNumber": "233235894", # "2211945",
            "role": "user", # "admin",
            "disabled": False,
            "avatar": [{"id": 'eb4b4851-a5e4-483a-a1d0-3f3feedae3a6', "name": "test1.png", "new": True, "sizeInBytes": 342800,  "privateUrl": "users/avatar/eb4b4851-a5e4-483a-a1d0-3f3feedae3a6.png", "publicUrl": "http://127.0.0.1:5000/files/download?privateUrl=users/avatar/avatar/eb4b4851-a5e4-483a-a1d0-3f3feedae3a6.png" }]
        }, headers=headers)
        print(rv.data)
        print('status: ', rv.status_code)

def test_delete_user():
    print('testing /users/<user_id> PUT')
    token = os.environ["AUTH_TOKEN"]
    authorization = 'Bearer ' + str(token)
    headers = {
        # 'Content-Type': 'application/json',
        'Authorization': authorization
    }

    id = "c99aa62f-a553-4d09-8fba-2a0a7d834ddd"
    with app.test_client() as c:
        rv = c.delete('/users/%s' % id, json={}, headers=headers)
        print(rv.data)
        print('status: ', rv.status_code)

if __name__ == '__main__':
    get_token()
    #upload_file()
    #test_create()
    #test_get_all()
    # test_get_user()
    test_put_user()
    # test_delete_user()
