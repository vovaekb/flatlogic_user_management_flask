from flask import json, jsonify
from app import app


def test_signup():
    print('testing /auth/signup')

    # Create new user from sign in form
    #'''
    with app.test_client() as c:
        rv = c.post('/auth/signup', json={
            'email': 'bill_xavier@host.com', 'password': 'dfgvd564rf'
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
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTc0MDI1NjQsImlhdCI6MTYxNzQwMjIwNCwic3ViIjoiMGUwNTFmMTAtOGY3Ni00YjA5LTllZGMtODM4YmQ3MDNhMGQ4In0.vRcSxkoLIXSLcGezHZDgVJjWN4Ihtt7fKhc_Rgq_cXc"
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

def test_send_pasword_reset_email():
    with app.test_client() as c:
        rv = c.post('/auth/send-password-reset-email', json={
            'email': 'bill_xavier@host.com'
        })
        print(rv.data)
        print('status: ', rv.status_code)

if __name__ == '__main__':
    #test_signup()
    test_send_email_address_verification_email()
    #test_verify_email()
    #test_signin_local()
    # test_password_update()
