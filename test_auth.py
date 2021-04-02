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
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTczNjM3MTEsImlhdCI6MTYxNzM2MzM1MSwic3ViIjoiMmExNmU0ZmMtMTZjZC00ZWE5LTkzYWUtMGUyMGY4NGVlMzIwIn0.7U8jlilZpKjvdZF3YNFhkPaiPhIxRfBe3UdwkTpP5ns"
    with app.test_client() as c:
        rv = c.put('/auth/verify-email', json={
            'token': token
        })
        json_data = rv.get_json()
        print(rv.data)
        print('status: ' , rv.status_code)
        #print(json_data)

def test_signin_local():
    print('testing /signin/local')
    with app.test_client() as c:
        rv = c.post('/auth/signin/local', json={
            'email': 'bill_xavier@host.com', 'password': 'dfgvd564rf'
        })
        json_data = rv.get_json()
        #print(json_data)
        print(rv.data)
        token = str(rv.data)
        print('status: ' , rv.status_code)

def test_password_update():
    print('testing /signin/password-update')
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTczODUxNjEsImlhdCI6MTYxNzM2MzU2MSwiaWQiOiIyYTE2ZTRmYy0xNmNkLTRlYTktOTNhZS0wZTIwZjg0ZWUzMjAiLCJlbWFpbCI6ImJpbGxfeGF2aWVyQGhvc3QuY29tIn0.49G21qLF1QFeE3y77z8FTwId5R7suxuDaitovl4oMoo"
    authorization = 'Bearer ' + str(token)

    headers = {
        # 'Access-Control-Allow-Origin': '*',
        # 'Content-Type': 'application/json',
        'Authorization': authorization
    }
    with app.test_client() as c:
        rv = c.put('/auth/password-update', json={
            "current_password": "dfgvd564rf",
            "new_password": "dfgvd564rf", # "2as25Ifzr"
        }, headers=headers)
        json_data = rv.get_json()
        print(rv.data)
        print('status: ' , rv.status_code)
        print(json_data)

if __name__ == '__main__':
    #test_signup()
    #test_verify_email()
    #test_signin_local()
    test_password_update()
