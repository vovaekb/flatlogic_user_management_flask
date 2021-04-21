import os
import datetime
import json
from json import JSONEncoder
import flask
from flask import render_template
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
import google.oauth2.credentials
import googleapiclient.discovery
from authlib.client import OAuth2Session
from app.models import Users
from app import app
from config import providers
from app import CustomError
from app.services.email import EmailSender
from app.services.encoding import generate_token
from app.users.db import UserDBApi
from app.auth import ACCESS_TOKEN_URI, AUTHORIZATION_SCOPE, AUTH_REDIRECT_URI, AUTH_STATE_KEY, CLIENT_ID, CLIENT_SECRET, AUTH_TOKEN_KEY
from app.auth import ValidationError, ForbiddenError



def is_logged_in():
    return True if AUTH_TOKEN_KEY in flask.session else False

def build_credentials():
    if not is_logged_in():
        raise Exception('User must be logged in')

    oauth2_tokens = flask.session[AUTH_TOKEN_KEY]
    return google.oauth2.credentials.Credentials(
        oauth2_tokens['access_token'],
        refresh_token=oauth2_tokens['refresh_token'],
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        token_uri=ACCESS_TOKEN_URI)

def get_user_info():
    credentials = build_credentials()

    oauth2_client = googleapiclient.discovery.build(
        'oauth2', 'v2',
        credentials=credentials)

    return oauth2_client.userinfo().get().execute()



# Auth service class
class Auth:
    def signup(email: str, password: str, host: str, current_user: Users = None):
        print('Auth.sign()')
        user_email = email
        print('user_email: ', user_email)
        user = app.session.query(Users).filter_by(email=user_email).first()
        print(user)
        user_password = password
        print('user_password: ', user_password)
        password_hash = generate_password_hash(user_password, method='sha256')
        print(password_hash)

        if user:
            print(user.authenticationUid)
            if user.authenticationUid:
                raise ValidationError({'message': 'Error when registering user in database: Email already in use\n' })

            if user.disabled:
                raise ValidationError({'message': 'Error when registering user in database: User disabled \n' })

            # update password
            user = UserDBApi.update_password(user.id, password_hash, current_user)

            print('host: ', host)

            # if email sender is configured
            # send email address verification email
            if EmailSender.isConfigured():
                Auth.send_email_address_verification_email(user_email, host)

            token_expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=6)
            user_dict = {
                "id": str(user.id),
                "email": str(user.email)
            }
            data = {
                "exp": token_expires_at,
                "iat": datetime.datetime.utcnow(),
                "user": user_dict
            }
            # return JWT sign with data
            token = generate_token(data)
            print(token)
            return token
        
        print('Creating new user')
        # Create user
        data = {
            'first_name': user_email.split('@')[0],
            'password': password_hash,
            'email': user_email
        }
        user = UserDBApi.create_from_auth(data)
        '''
        user = Users(
            firstName = user_email.split('@')[0],
            password = password_hash,
            email = user_email,
            # authenticationUid = data.authenticationUid,
            updatedAt = func.now()
        )
        app.session.add(user)
        app.session.flush()
        user.authenticationUid = user.id
        app.session.add(user)
        app.session.commit()
        '''
        
        # if email sender is configured
        # send email address verification email
        if EmailSender.isConfigured():
            Auth.send_email_address_verification_email(user_email, host)
        
        #del user.password
        
        token_expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=6)
        data = {
            "exp": token_expires_at,
            "iat": datetime.datetime.utcnow(),
            "id": str(user.id),
            "email": str(user.email)
        }
        # return JWT sign with data
        token = generate_token(data)
        return token
    
    def signin(email: str, password: str):
        print('\nAuth.signin')
        user = app.session.query(Users).filter_by(email=email).first()
        print(user)

        if not user:
            raise ValidationError({'message': 'Error when signing in: User not found\n' })

        if user.disabled:
            raise ValidationError({'message': 'Error when signing in: User disabled\n'})

        if not user.password:
            raise ValidationError({'message': 'Error when signing in: Wrong password\n'})

        # not email sender configured
        if not EmailSender.isConfigured():
            user.emailVerified = True
            app.session.add(user)
            app.session.commit()

        if not user.emailVerified:
            raise ValidationError({'message': 'Error when signing in: User not verified\n'})

        # check if entered password match the user password saved in BD
        if not check_password_hash(user.password, password):
            raise ValidationError({'message': 'Error when signing in: Wrong password\n'})

        token_expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=6)
        user_dict = {
                    "id": str(user.id),
                    "email": str(user.email)
                }
        data = {
            "iat": datetime.datetime.utcnow(),
            "exp": token_expires_at,
            "user": user_dict 
        }
        print(data)
        # return JWT sign with data
        token = generate_token(data)
        return token

    def send_email_address_verification_email(email: str, host: str):
        print('Auth.send_email_address_verification_email')
        if not EmailSender.isConfigured():
            raise CustomError({'message': 'Email provider is not configured. Please configure it in config.py\n'})
        # Generate email verification token
        try:
            token = UserDBApi.generate_email_verification_token(email)
            print('')
            link = f'{host}/#/verify-email?token={token}'
            #print(link)
        except Exception as e:
            print(str(e))
            raise ValidationError({'message': 'Email address verification email error: %s\n' % str(e)})

        # send email
        print(email)
        email_sender = EmailSender(email, 'email_address_verification')
        data = {
            'link': link,
            'title': app.config['APP_TITLE']
        }
        email_sender.send(data)

    def send_password_reset_email(email: str, host: str, type: str = 'register'):
        print('Auth.send_password_reset_email')
        if not EmailSender.isConfigured():
            raise CustomError({
                'message': 'Email provider is not configured. Please configure it in config.py\n'
            })
        try:
            token = UserDBApi.generate_password_reset_token(email)
            link = f'{host}/password-reset?token={token}#/login'
            print(link)
        except Exception as e:
            print(str(e))
            raise ValidationError({'message': 'Password reset error: %s\n' % str(e)})

        # send email
        print(email)
        email_type = None
        if type == 'register':
            email_type = 'password_reset'
        elif type == 'invitation':
            email_type = 'invitation'
        email_sender = EmailSender(email, email_type)
        data = {
            'link': link,
            'title': app.config['APP_TITLE'],
            'email': email
        }
        email_sender.send(data)

    def password_update(current_password: str, new_password: str, current_user: Users = None):
        print('Auth.password_update')
        if not current_user: 
            raise ForbiddenError({'message': 'Password update error: Forbidden\n'})

        if not check_password_hash(current_user.password, current_password): 
            raise ValidationError({'message': 'Password update error: Wrong password\n'})

        if check_password_hash(current_user.password, new_password):
            raise ValidationError({'message': 'Password update error: The same password\n'})

        password_hash = generate_password_hash(new_password, method='sha256')
        print(password_hash)

        user = UserDBApi.update_password(current_user.id, password_hash, current_user)
        return user

    def password_reset(token: str, password: str, current_user: Users = None):
        # find user by password reset token
        user = app.session.query(Users) \
            .filter(Users.passwordResetToken == token) \
            .filter(Users.passwordResetTokenExpiresAt > datetime.datetime.utcnow()) \
            .first()
        print(user)
        if not user:
            raise ValidationError({'message': 'Password reset error: Invalid token\n'})

        password_hash = generate_password_hash(password, method='sha256')
        print(password_hash)

        user = UserDBApi.update_password(user.id, password_hash, current_user)
        print(user)
        return user


    def verify_email(token: str, current_user: Users = None):
        user = app.session.query(Users)\
            .filter(Users.emailVerificationToken==token)\
            .filter(Users.emailVerificationTokenExpiresAt > datetime.datetime.utcnow())\
            .first()
        print(user)
        if not user:
            raise ValidationError({'message': 'Verify email error: Invalid token\n' })

        # mark email verified
        UserDBApi.mark_email_verified(user.id, current_user)
        return True

    def update_profile(data: dict, current_user: Users):
        print('Auth.update_profile')
        user = app.session.query(Users).filter_by(id=current_user.id).first()
        print(user)
        UserDBApi.update(current_user.id, data, current_user)

    def signin_google_callback(request_url: str):

        session = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                                scope=AUTHORIZATION_SCOPE,
                                state=flask.session[AUTH_STATE_KEY],
                                redirect_uri=AUTH_REDIRECT_URI)

        oauth2_tokens = session.fetch_access_token(
            ACCESS_TOKEN_URI,
            authorization_response=request_url)
        flask.session[AUTH_TOKEN_KEY] = oauth2_tokens

        user_info = get_user_info()
        print(user_info)

        provider = providers["GOOGLE"]  # "google"
        user = app.session.query(Users) \
            .filter(Users.email == user_info['email']) \
            .filter(Users.provider == provider) \
            .first()
        print(user)
        if not user:
            # Create new user
            print('Creating new user')
            user = Users(
                email=user_info['email'],
                provider=provider,
                updatedAt=func.now()
            )
            app.session.add(user)
            app.session.flush()
            app.session.add(user)
            app.session.commit()
        print(user.id)

        token_expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=6)
        user_dict = {
            "id": str(user.id),
            "email": str(user.email),
            "name": user_info['name']
        }
        data = {
            "exp": token_expires_at,
            "iat": datetime.datetime.utcnow(),
            "user": user_dict
        }
        # return JWT sign with data
        token = generate_token(data)
        print(token)
        return token
