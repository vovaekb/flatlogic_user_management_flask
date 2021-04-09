import os
from flask import json, jsonify
from app import app

AUTH_TOKEN = ""

def test_signup():
    print('testing /auth/signup')

    # Create new user from sign in form
    #'''
    with app.test_client() as c:
        rv = c.post('/auth/signup', json={
           'email': "ralf_stone@host.com", #'bill_xavier@host.com',
            'password': 'jkht6fd4le,*', # 'nnjk4cb&%d3', # 'dfgvd564rf'
        })
        json_data = rv.get_json()
        # print(json_data)
        print(rv.data)
        token = rv.data
        os.environ["AUTH_TOKEN"] = token.decode("utf-8")
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
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTc5Njk3NzUsImlhdCI6MTYxNzk2OTQxNSwic3ViIjoiN2YxZTVhMTAtNTdkNC00MGJmLThlZDAtODAzYzgzMTBlZjc3In0.oIFpXNmD2Ao1CT9GC9I426NUkmAHilVbV0RbUtFjtoQ"
    # os.environ["EMAIL_VERIFY_TOKEN"] # AUTH_TOKEN"]
    print(token)
    with app.test_client() as c:
        rv = c.put('/auth/verify-email', json={
            'token': token
        })
        # json_data = rv.get_json()
        print(rv.data)
        print('status: ' , rv.status_code)
        #print(json_data)

def test_send_email_address_verification_email():
    print('test_send_email_address_verification_email')
    #print(os.environ["AUTH_TOKEN"])
    with app.test_client() as c:
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTc5OTA2MjAsImlhdCI6MTYxNzk2OTAyMCwiaWQiOiI3ZjFlNWExMC01N2Q0LTQwYmYtOGVkMC04MDNjODMxMGVmNzciLCJlbWFpbCI6InJhbGZfc3RvbmVAaG9zdC5jb20ifQ.Rzz27cK0SXsSA2Tgbg3V2lA5pnvL5BUzMHU0T4DL4s4" # os.environ["AUTH_TOKEN"]
        #token = os.environ["AUTH_TOKEN"]
        authorization = 'Bearer ' + str(token)

        headers = {
            # 'Content-Type': 'application/json',
            'Authorization': authorization
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
            'email': "ralf_stone@host.com", # 'billy_xavier@host.com', # 'billy_xavier@host.com',
            'password': "dfgvd564rf", # 'jkht6fd4le,*', # "dfgvd564rf", #  'nnjk4cb&%d3', # 'dfgvd564rf'
        })
        json_data = rv.get_json()
        #print(json_data)
        token = rv.data
        os.environ["AUTH_TOKEN"] = token.decode("utf-8")
        token_file = 'auth_token.txt'
        with open(token_file, 'w') as f:
            f.write(token.decode("utf-8"))
        print(token)
        print('status: ' , rv.status_code)

def test_password_update():
    print('testing /signin/password-update')
    #print(os.environ["AUTH_TOKEN"])
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTc5OTA2MjAsImlhdCI6MTYxNzk2OTAyMCwiaWQiOiI3ZjFlNWExMC01N2Q0LTQwYmYtOGVkMC04MDNjODMxMGVmNzciLCJlbWFpbCI6InJhbGZfc3RvbmVAaG9zdC5jb20ifQ.Rzz27cK0SXsSA2Tgbg3V2lA5pnvL5BUzMHU0T4DL4s4" # os.environ["AUTH_TOKEN"]
    #token = os.environ["AUTH_TOKEN"] #token # "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTczODUxNjEsImlhdCI6MTYxNzM2MzU2MSwiaWQiOiIyYTE2ZTRmYy0xNmNkLTRlYTktOTNhZS0wZTIwZjg0ZWUzMjAiLCJlbWFpbCI6ImJpbGxfeGF2aWVyQGhvc3QuY29tIn0.49G21qLF1QFeE3y77z8FTwId5R7suxuDaitovl4oMoo"
    authorization = 'Bearer ' + str(token)

    headers = {
        # 'Access-Control-Allow-Origin': '*',
        # 'Content-Type': 'application/json',
        'Authorization': authorization
    }
    with app.test_client() as c:
        rv = c.put('/auth/password-update', json={
            "current_password": 'jkht6fd4le,*', # "dfgvd564rf", # "dfgvd564rf",
            "new_password": "dfgvd564rf", # "2as25Ifzr"
        }, headers=headers)
        json_data = rv.get_json()
        print(rv.data)
        print('status: ' , rv.status_code)
        # print(json_data)

def test_send_pasword_reset_email():
    with app.test_client() as c:
        rv = c.post('/auth/send-password-reset-email', json={
            'email': "ralf_stone@host.com" # 'bill_xavier@host.com'
        })
        print(rv.data)
        print('status: ', rv.status_code)

def test_password_reset():
    print('testing /auth/password-reset')
    #print(os.environ["AUTH_TOKEN"])
    auth_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTc5OTA2MjAsImlhdCI6MTYxNzk2OTAyMCwiaWQiOiI3ZjFlNWExMC01N2Q0LTQwYmYtOGVkMC04MDNjODMxMGVmNzciLCJlbWFpbCI6InJhbGZfc3RvbmVAaG9zdC5jb20ifQ.Rzz27cK0SXsSA2Tgbg3V2lA5pnvL5BUzMHU0T4DL4s4" # os.environ["AUTH_TOKEN"]
    #auth_token = os.environ["AUTH_TOKEN"] # token # "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTc2MzcwNzQsImlhdCI6MTYxNzYxNTQ3NCwiaWQiOiIyMjhmNGJiZS0yM2VjLTRhZmYtYTg3NC0yNTZlMWM4ZGVjZmMiLCJlbWFpbCI6ImJpbGxfeGF2aWVyQGhvc3QuY29tIn0.B1FXZ-UfjKq-HILHZuoVTV6C3uzlYhq54HI9b5hKb4w"
    authorization = 'Bearer ' + str(auth_token)

    password_reset_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTc5NzE2MDYsImlhdCI6MTYxNzk3MTI0Niwic3ViIjoiN2YxZTVhMTAtNTdkNC00MGJmLThlZDAtODAzYzgzMTBlZjc3In0.PWsReE41SFZB4cye_DFY-fXAJCZJ1VAur-aCFC3QUJQ"

    headers = {
        # 'Access-Control-Allow-Origin': '*',
        # 'Content-Type': 'application/json',
        #'Authorization': authorization
    }
    with app.test_client() as c:
        rv = c.put('/auth/password-reset', json={
            "password": 'jkht6fd4le,*', # "dfgvd564rf",
            "token": password_reset_token, # "2as25Ifzr"
        }, headers=headers)
        print(rv.data)
        print('status: ', rv.status_code)

def test_profile():
    print('testing /auth/profile')
    print(os.environ["AUTH_TOKEN"])
    auth_token = os.environ["AUTH_TOKEN"]
    authorization = 'Bearer ' + str(auth_token)
    id = "188b7d6a-3bbd-44bd-8e07-6be6bc4b1e1f"

    profile_data = {
        #"id": id,
        "email": "ralf_stone@host.com", #"bill_xavier@host.com",
        "firstName": "Tailor", # "Billy",
        "lastName": None, # "Xavier1",
        "phoneNumber": "250051342", # "2211945",
        "role": "admin",
        "disabled": False,
        "avatar": [
            {
                "id": '79c2b036-2efb-4f82-bd8b-6158fe0f36de',
                "name": "tynvnmm.jpeg", # "test1.png",
                "new": True,
                "sizeInBytes": 321800,
                "privateUrl": "users/avatar/79c2b036-2efb-4f82-bd8b-6158fe0f36de.jpeg", # "users/avatar/eb4b4851-a5e4-483a-a1d0-3f3feedae3a6.png",
                "publicUrl": "http://127.0.0.1:5000/files/download?privateUrl=users/avatar/avatar/79c2b036-2efb-4f82-bd8b-6158fe0f36de.jpeg" # "http://127.0.0.1:5000/files/download?privateUrl=users/avatar/avatar/eb4b4851-a5e4-483a-a1d0-3f3feedae3a6.png"
            },
            {
                "id": '27e264dd-aa46-4c98-8c04-aecace218d9e',
                "name": "heyhere.png",
                "new": True,
                "sizeInBytes": 213500,
                "privateUrl": "users/avatar/27e264dd-aa46-4c98-8c04-aecace218d9e.png",
                "publicUrl": "http://127.0.0.1:5000/files/download?privateUrl=users/avatar/avatar/27e264dd-aa46-4c98-8c04-aecace218d9e.png"
            },
        ]
        # "avatar": []
    }

    headers = {
        # 'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',
        'Authorization': authorization
    }
    with app.test_client() as c:
        rv = c.put('/auth/profile', json={
            "profile": profile_data
        }, headers=headers)
        print(rv.data)
        print('status: ', rv.status_code)

def test_me():
    print('testing /auth/me')
    #print(os.environ["AUTH_TOKEN"])
    auth_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTc5OTA2MjAsImlhdCI6MTYxNzk2OTAyMCwiaWQiOiI3ZjFlNWExMC01N2Q0LTQwYmYtOGVkMC04MDNjODMxMGVmNzciLCJlbWFpbCI6InJhbGZfc3RvbmVAaG9zdC5jb20ifQ.Rzz27cK0SXsSA2Tgbg3V2lA5pnvL5BUzMHU0T4DL4s4" # os.environ["AUTH_TOKEN"]
    #auth_token = os.environ["AUTH_TOKEN"]
    authorization = 'Bearer ' + str(auth_token)

    headers = {
        'Authorization': authorization
    }
    with app.test_client() as c:
        rv = c.get('/auth/me', json={}, headers=headers)
        print(rv.data)
        print('status: ', rv.status_code)

def test_email_configured():
    print('testing /auth/email-configured')
    with app.test_client() as c:
        rv = c.get('/auth/email-configured', json={})
        print(rv.data)
        print('status: ', rv.status_code)

if __name__ == '__main__':
    #test_signup()
    #test_signin_local()
    #test_send_email_address_verification_email()
    #test_verify_email()
    #token = test_signin_local()
    # test_password_update(token)

    # Test password reset and update
    #test_signup()
    #test_verify_email()
    #test_signin_local()
    #test_send_pasword_reset_email()
    # test_password_reset()
    #test_password_update()

    # Test sending email verification email
    #test_send_email_address_verification_email()
    #test_verify_email()

    # Test profile and me
    test_signin_local()
    #test_me()
    test_profile()
    #test_email_configured()

