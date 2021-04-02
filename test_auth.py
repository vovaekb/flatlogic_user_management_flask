from flask import json, jsonify
from app import app


def test_signup():
    print('testing /auth/signup')
    with app.test_client() as c:
        rv = c.post('/auth/signup', json={
            'email': 'bill_xavier@host.com', 'password': 'dfgvd564rf'
        })
        json_data = rv.get_json()
        print(json_data)

def test_verify_email():
    print('testing /verify-email')
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTczNTYyMTAsImlhdCI6MTYxNzM1NTg1MCwic3ViIjoiYWI4YzA0YWEtNWUzMy00NmZjLWIwNTYtOGMxMWQ2OWFiYjExIn0.BqEJSRLjcXScZgIUILYpeug2joZQxwYvq4udj0IL5yA"
    with app.test_client() as c:
        rv = c.put('/auth/verify-email', json={
            'token': token
        })
        json_data = rv.get_json()
        print(json_data)

def test_signin_local():
    print('testing /signin/local')
    with app.test_client() as c:
        rv = c.post('/auth/signin/local', json={
            'email': 'bill_xavier@host.com', 'password': 'dfgvd564rf'
        })
        json_data = rv.get_json()
        print(json_data)

def test_password_update():
    print('testing /signin/password-update')
    token = ""
    authorization = 'Bearer ' + token

    headers = {
        # 'Access-Control-Allow-Origin': '*',
        # 'Content-Type': 'application/json',
        'Authorization': authorization
    }
    with app.test_client() as c:
        rv = c.put('/auth/verify-email', json={
            "current_password": "2fgsdf5zr",
            "new_password": "2as25Ifzr"
        }, headers=headers)
        json_data = rv.get_json()
        print(json_data)

if __name__ == '__main__':
    # test_signup()
    test_verify_email()
    # test_signin_local()
    # test_password_update()