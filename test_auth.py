import os
import os
from dotenv import load_dotenv
from flask import json, jsonify

from app import app

AUTH_TOKEN = ''


def test_signup():
    """Create new user from sign in form
    """
    print('testing /auth/signup')
    with app.test_client() as c:
        rv = c.post(
            '/auth/signup',
            json={
                'email': 'ralf_stone@host.com',
                'password': 'jkht6fd4le,*',
            }
        )
        print(rv.data)
        token = rv.data
        os.environ['AUTH_TOKEN'] = token.decode('utf-8')
        print('status: %s' % rv.status_code)

    # Create new user from admin panel
    '''
    with app.test_client() as c:
        token = os.environ['AUTH_TOKEN']
        authorization = 'Bearer ' + str(token)

        headers = {
            # 'Access-Control-Allow-Origin': '*',
            # 'Content-Type': 'application/json',
            'Authorization': authorization
        }
        password = 'sdvw3HGY'
        rv = c.post(
            '/auth/signup', 
            json={
                'email': 'uman_lesset@host.com', 
                'password': password
            }, 
            headers=headers
        )
        print(rv.data)
        print('status: %s' % rv.status_code)
    '''


def test_verify_email():
    """Test email verification endpoint
    """
    print('testing /verify-email')
    token = os.environ['EMAIL_VERIFY_TOKEN']
    print(token)
    with app.test_client() as c:
        rv = c.put(
            '/auth/verify-email',
            json={
                'token': token
            }
        )
        # json_data = rv.get_json()
        print(rv.data)
        print('status: %s' % rv.status_code)
        # print(json_data)


def test_send_email_address_verification_email():
    """Test sending email verification endpoint
    """
    print('test_send_email_address_verification_email')
    with app.test_client() as c:
        token = os.environ['AUTH_TOKEN']
        authorization = 'Bearer ' + str(token)

        headers = {
            # 'Content-Type': 'application/json',
            'Authorization': authorization
        }
        rv = c.post(
            '/auth/send-email-address-verification-email',
            json={},
            headers=headers
        )
        print(rv.data)
        print('status: %s' % rv.status_code)


def test_signin_local():
    """Test local signing in endpoint
    """
    print('testing /signin/local')
    with app.test_client() as c:
        rv = c.post(
            '/auth/signin/local', json={
                'email': 'ralf_stone@host.com',
                'password': 'dfgvd564rf',
            }
        )
        token = rv.data
        os.environ['AUTH_TOKEN'] = token.decode('utf-8')
        token_file = 'auth_token.txt'
        with open(token_file, 'w') as f:
            f.write(token.decode('utf-8'))
        print(token)
        print('status: %s' % rv.status_code)


def test_password_update():
    """Test updating password endpoint
    """
    print('testing /signin/password-update')
    token = os.environ['AUTH_TOKEN']
    authorization = 'Bearer ' + str(token)

    headers = {
        # 'Access-Control-Allow-Origin': '*',
        # 'Content-Type': 'application/json',
        'Authorization': authorization
    }
    with app.test_client() as c:
        rv = c.put(
            '/auth/password-update',
            json={
                'current_password': 'jkht6fd4le,*',
                'new_password': 'dfgvd564rf',
            },
            headers=headers
        )
        print(rv.data)
        print('status: %s' % rv.status_code)


def test_send_pasword_reset_email():
    """Test sending password reset email endpoint
    """
    with app.test_client() as c:
        rv = c.post(
            '/auth/send-password-reset-email',
            json={
                'email': 'ralf_stone@host.com'
            }
        )
        print(rv.data)
        print('status: %s' % rv.status_code)


def test_password_reset():
    """Test password reset endpoint endpoint
    """
    print('testing /auth/password-reset')
    auth_token = os.environ['AUTH_TOKEN']
    authorization = 'Bearer ' + str(auth_token)

    password_reset_token = os.environ['PASSWORD_RESET_TOKEN']

    headers = {
        # 'Access-Control-Allow-Origin': '*',
        # 'Content-Type': 'application/json',
        # 'Authorization': authorization
    }
    with app.test_client() as c:
        rv = c.put('/auth/password-reset', json={
            'password': 'jkht6fd4le,*',
            'token': password_reset_token,
        }, headers=headers)
        print(rv.data)
        print('status: %s' % rv.status_code)


def test_profile():
    """Test user profile endpoint
    """
    print('testing /auth/profile')
    auth_token = os.environ['AUTH_TOKEN']
    authorization = 'Bearer ' + str(auth_token)
    id = '188b7d6a-3bbd-44bd-8e07-6be6bc4b1e1f'

    image_paths = [
        '79c2b036-2efb-4f82-bd8b-6158fe0f36de.jpeg',
        '27e264dd-aa46-4c98-8c04-aecace218d9e.png'
    ]

    profile_data = {
        'email': 'ralf_stone@host.com',
        'firstName': 'Tailor',
        'lastName': None,
        'phoneNumber': '250051342',
        'role': 'admin',
        'disabled': False,
        'avatar': [
            {
                'id': '79c2b036-2efb-4f82-bd8b-6158fe0f36de',
                'name': 'tynvnmm.jpeg',
                'new': True,
                'sizeInBytes': 321800,
                'privateUrl': 'users/avatar/%s' % (image_paths[0]),
                'publicUrl':
                    '%s/files/download?privateUrl=users/avatar/avatar/%s' %
                    (app.config['REMOTE'], image_paths[0])
            },
            {
                'id': '27e264dd-aa46-4c98-8c04-aecace218d9e',
                'name': 'heyhere.png',
                'new': True,
                'sizeInBytes': 213500,
                'privateUrl': 'users/avatar/%s' % (image_paths[1]),
                'publicUrl':
                    '%s/files/download?privateUrl=users/avatar/avatar/%s' %
                    (app.config['REMOTE'], image_paths[1])
            },
        ]
    }

    headers = {
        # 'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',
        'Authorization': authorization
    }
    with app.test_client() as c:
        rv = c.put(
            '/auth/profile',
            json={
                'profile': profile_data
            },
            headers=headers
        )
        print(rv.data)
        print('status: %s' % rv.status_code)


def test_me():
    '''Test updating password endpoint
    '''
    print('testing /auth/me')
    auth_token = os.environ['AUTH_TOKEN']
    authorization = 'Bearer ' + str(auth_token)

    headers = {
        'Authorization': authorization
    }
    with app.test_client() as c:
        rv = c.get(
            '/auth/me',
            json={},
            headers=headers
        )
        print(rv.data)
        print('status: %s' % rv.status_code)


def test_email_configured():
    """Test if email is configured endpoint
    """
    print('testing /auth/email-configured')
    with app.test_client() as c:
        rv = c.get(
            '/auth/email-configured',
            json={}
        )
        print(rv.data)
        print('status: %s' % rv.status_code)


if __name__ == '__main__':
    test_signup()
    # test_signin_local()
    # test_send_email_address_verification_email()
    # test_verify_email()
    # token = test_signin_local()
    # test_password_update(token)

    # Test password reset and update
    # test_signup()
    # test_verify_email()
    # test_signin_local()
    # test_send_pasword_reset_email()
    # test_password_reset()
    # test_password_update()

    # Test sending email verification email
    # test_send_email_address_verification_email()
    # test_verify_email()

    # Test profile and me
    test_signin_local()
    # test_me()
    test_profile()
    # test_email_configured()
