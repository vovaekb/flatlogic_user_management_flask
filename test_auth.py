from flask import json, jsonify
from app import app


def test_signup():
    print('testing /auth/signup')

    # Create new user from sign in form
    #'''
    with app.test_client() as c:
        rv = c.post('/auth/signup', json={
            'email': 'bill_xavier@host.com',
            'password': 'dfgvd564rf'
        })
        json_data = rv.get_json()
        # print(json_data)
        print(rv.data)
        print('status: ', rv.status_code)
    #'''

    # Create new user from admin panel
    '''
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
    '''

def test_verify_email():
    print('testing /verify-email')
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTc2MTU2MDksImlhdCI6MTYxNzYxNTI1MCwic3ViIjoiMjI4ZjRiYmUtMjNlYy00YWZmLWE4NzQtMjU2ZTFjOGRlY2ZjIn0.NjFwQarP7avBANWum6R_Ffo1xqC_WAhwhRWoCDSQZhQ"
    with app.test_client() as c:
        rv = c.put('/auth/verify-email', json={
            'token': token
        })
        # json_data = rv.get_json()
        print(rv.data)
        print('status: ' , rv.status_code)
        #print(json_data)

def test_send_email_address_verification_email():
    with app.test_client() as c:
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTc0MjM5OTEsImlhdCI6MTYxNzQwMjM5MSwiaWQiOiIwZTA1MWYxMC04Zjc2LTRiMDktOWVkYy04MzhiZDcwM2EwZDgiLCJlbWFpbCI6ImJpbGxfeGF2aWVyQGhvc3QuY29tIn0.GMOjL8Y3mVHW0OF-MtKPlaircX5mU504V5rIZQw-EHE"
        authorization = 'Bearer ' + str(token)

        headers = {
            # 'Access-Control-Allow-Origin': '*',
            # 'Content-Type': 'application/json',
            #'Authorization': authorization
        }
        password = 'sdvw3HGY'  # '&hgvdsdf4xf'
        rv = c.post('/auth/send-email-address-verification-email', json={}, headers=headers)
        # json_data = rv.get_json()
        # print(json_data)
        print(rv.data)
        print('status: ', rv.status_code)

def test_signin_local():
    print('testing /signin/local')
    with app.test_client() as c:
        rv = c.post('/auth/signin/local', json={
            'email': 'bill_xavier@host.com', # 'billy_xavier@host.com',
            'password': 'dfgvd564rf'
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

def test_send_pasword_reset_email():
    with app.test_client() as c:
        rv = c.post('/auth/send-password-reset-email', json={
            'email': 'bill_xavier@host.com'
        })
        print(rv.data)
        print('status: ', rv.status_code)

def test_password_reset():
    print('testing /auth/password-reset')
    auth_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTc2MzcwNzQsImlhdCI6MTYxNzYxNTQ3NCwiaWQiOiIyMjhmNGJiZS0yM2VjLTRhZmYtYTg3NC0yNTZlMWM4ZGVjZmMiLCJlbWFpbCI6ImJpbGxfeGF2aWVyQGhvc3QuY29tIn0.B1FXZ-UfjKq-HILHZuoVTV6C3uzlYhq54HI9b5hKb4w"
    authorization = 'Bearer ' + str(auth_token)

    password_reset_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTc2MTY0ODcsImlhdCI6MTYxNzYxNjEyNywic3ViIjoiMjI4ZjRiYmUtMjNlYy00YWZmLWE4NzQtMjU2ZTFjOGRlY2ZjIn0.y-hPtyxpV21OJYiPtLw2qFZa_Bg6spgHV_q5ZTIZ_rA"

    headers = {
        # 'Access-Control-Allow-Origin': '*',
        # 'Content-Type': 'application/json',
        'Authorization': authorization
    }
    with app.test_client() as c:
        rv = c.put('/auth/password-reset', json={
            "password": "dfgvd564rf",
            "token": password_reset_token, # "2as25Ifzr"
        }, headers=headers)
        print(rv.data)
        print('status: ', rv.status_code)

def test_profile():
    print('testing /auth/profile')
    auth_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTczODUxNjEsImlhdCI6MTYxNzM2MzU2MSwiaWQiOiIyYTE2ZTRmYy0xNmNkLTRlYTktOTNhZS0wZTIwZjg0ZWUzMjAiLCJlbWFpbCI6ImJpbGxfeGF2aWVyQGhvc3QuY29tIn0.49G21qLF1QFeE3y77z8FTwId5R7suxuDaitovl4oMoo"
    authorization = 'Bearer ' + str(auth_token)

    password_reset_token = ""

    profile_data = {}

    headers = {
        # 'Access-Control-Allow-Origin': '*',
        # 'Content-Type': 'application/json',
        'Authorization': authorization
    }
    with app.test_client() as c:
        rv = c.put('/auth/profile', json={
            "profile": profile_data,  # "2as25Ifzr"
        }, headers=headers)
        print(rv.data)
        print('status: ', rv.status_code)

def test_me():
    print('testing /auth/me')
    auth_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTczODUxNjEsImlhdCI6MTYxNzM2MzU2MSwiaWQiOiIyYTE2ZTRmYy0xNmNkLTRlYTktOTNhZS0wZTIwZjg0ZWUzMjAiLCJlbWFpbCI6ImJpbGxfeGF2aWVyQGhvc3QuY29tIn0.49G21qLF1QFeE3y77z8FTwId5R7suxuDaitovl4oMoo"
    authorization = 'Bearer ' + str(auth_token)

    headers = {
        'Authorization': authorization
    }
    with app.test_client() as c:
        rv = c.get('/auth/me', json={}, headers=headers)
        print(rv.data)
        print('status: ', rv.status_code)

if __name__ == '__main__':
    #test_signup()
    # test_send_email_address_verification_email()
    #test_verify_email()
    #test_signin_local()
    # test_password_update()

    # Test password reset
    # test_signup()
    #test_verify_email()
    #test_signin_local()
    #test_send_pasword_reset_email()
    test_password_reset()

    # Test profile and me
    #test_signin_local()
    # test_me()

