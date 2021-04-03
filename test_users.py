from flask import json, jsonify
from app import app

def test_create():
    print('testing /users POST')

    # Create new user from sign in form
    with app.test_client() as c:
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTczOTA5NjEsImlhdCI6MTYxNzM2OTM2MSwiaWQiOiJiNTM1MGQ1YS03ZmYyLTQwM2ItOTMzNC00Y2UzNjQ0M2YzYTYiLCJlbWFpbCI6ImJpbGxfeGF2aWVyQGhvc3QuY29tIn0.GHzmEbzhMj5z3Zesr4wR_sIr9Od0SZ6SxRzO9gb780o"
        authorization = 'Bearer ' + str(token)

        headers = {
            # 'Access-Control-Allow-Origin': '*',
            # 'Content-Type': 'application/json',
            'Authorization': authorization
        }
        rv = c.post('/users', json={
            "id": None,
            "email": "ralf_stone@host.com",
            "firstName": "Ralf",
            "lastName": "Stone", "phoneNumber": "23241945", "role": "user", "authenticationUid": None, "avatar": []
        }, headers=headers)
        # json_data = rv.get_json()
        # print(json_data)
        print(rv.data)
        print('status: ', rv.status_code)

def test_get_all():
    print('testing /users POST')
    with app.test_client() as c:
        rv = c.get('/users', json={})
        print(rv.data)
        print('status: ', rv.status_code)

def test_get_user():
    print('testing /users POST')
    id = "c99aa62f-a553-4d09-8fba-2a0a7d834ddd"
    with app.test_client() as c:
        rv = c.get('/users/%s' % id, json={})
        print(rv.data)
        print('status: ', rv.status_code)

if __name__ == '__main__':
    test_create()
    # test_get_all()
