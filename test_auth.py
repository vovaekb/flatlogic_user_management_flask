from flask import json, jsonify
from app import app


def test_signup():
    print('testing /auth/signup')

    # Create new user from sign in form
    '''
    with app.test_client() as c:
        rv = c.post('/auth/signup', json={
            'email': 'bill_xavier@host.com', 'password': 'dfgvd564rf'
        })
        json_data = rv.get_json()
        # print(json_data)
        print(rv.data)
        print('status: ', rv.status_code)
    '''

    # Create new user from admin panel
    #'''
    with app.test_client() as c:
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTczOTA5NjEsImlhdCI6MTYxNzM2OTM2MSwiaWQiOiJiNTM1MGQ1YS03ZmYyLTQwM2ItOTMzNC00Y2UzNjQ0M2YzYTYiLCJlbWFpbCI6ImJpbGxfeGF2aWVyQGhvc3QuY29tIn0.GHzmEbzhMj5z3Zesr4wR_sIr9Od0SZ6SxRzO9gb780o"
        authorization = 'Bearer ' + str(token)

        headers = {
            # 'Access-Control-Allow-Origin': '*',
            # 'Content-Type': 'application/json',
            'Authorization': authorization
        }
        password = 'sdvw3HGY' # '&hgvdsdf4xf'
        rv = c.post('/auth/signup', json={
            'email': 'uman_lesset@host.com', 'password': password
        }, headers=headers)
        # json_data = rv.get_json()
        # print(json_data)
        print(rv.data)
        print('status: ', rv.status_code)
    #'''

def test_verify_email():
    print('testing /verify-email')
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTczNjk1OTcsImlhdCI6MTYxNzM2OTIzNywic3ViIjoiYjUzNTBkNWEtN2ZmMi00MDNiLTkzMzQtNGNlMzY0NDNmM2E2In0.hIX8D--k-6s99wuYntarPyj35KJfpkP5ImOiT_t4fLo"
    with app.test_client() as c:
        rv = c.put('/auth/verify-email', json={
            'token': token
        })
        # json_data = rv.get_json()
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
        token = str(rv.data)
        print(token)
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
        # print(json_data)

if __name__ == '__main__':
    test_signup()
    #test_verify_email()
    #test_signin_local()
    # test_password_update()
