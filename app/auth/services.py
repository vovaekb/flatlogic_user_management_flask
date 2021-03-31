import os
import datetime
from hashlib import pbkdf2_hmac
import jwt
from flask import render_template
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from app.models import Users
from app import app, mail
#from app.auth.views import CustomError
from app.auth import CustomError


def validate_user_input(input_type, **kwargs):
    if input_type == "authentication":
        if len(kwargs["email"]) <= 255 and len(kwargs["password"]) <= 255:
            return True
        else:
            return False

def generate_salt():
    salt = os.urandom(16)
    return salt.hex()

def generate_token(payload):
    print('generate_token')
    token = jwt.encode(
        payload,
        app.config.get('SECRET_KEY'),
        algorithm='HS256'
    )
    print(f'{token}')
    return token

def generate_hash(plain_password, password_salt):
    password_hash = pbkdf2_hmac(
        "sha256",
        b"%b" % bytes(plain_password, "utf-8"),
        b"%b" % bytes(password_salt, "utf-8"),
        10000
    )
    return password_hash.hex()

class UserDBApi:
    def generate_email_verification_token(email, options):
        # get current user
        # current_user = options.currentUser
        user = app.session.query(Users).filter_by(email=email).first()
        token_expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=360)
        payload = {
            'exp': token_expires_at,
            'iat': datetime.datetime.utcnow(),
            'sub': str(user.id)
        }
        token = generate_token(payload)
        
        user.emailVerificationToken = token
        user.emailVerificationTokenExpiresAt = token_expires_at
        #user.updatedById  = current_user.id
        app.session.add(user)
        app.session.commit()
        return token


# Auth service class
class Auth:
    def signup(email, password, host, options={}):
        print('Auth.sign()')
        user_email = email
        print(user_email)
        user = app.session.query(Users).filter_by(email=user_email).first()
        print(user)
        user_password = password
        print(user_password)
        #user_confirm_password = request.json['confirm_password']
        #print(user_confirm_password)
        password_salt = generate_salt()
        print(password_salt)
        # password_hash = generate_hash(user_password, password_salt)
        password_hash = generate_password_hash(user_password, method='sha256')

        print(password_hash)
        if user:
            print(user.authenticationUid)
            if user.authenticationUid:
                raise CustomError({'message': 'Error when registering user in database: Email already in use\n' })

            if user.disabled:
                raise CustomError({'message': 'Error when registering user in database: User disabled \n' })

            # get current user

            # update password
            user.password = password_hash
            user.authenticationUid = user.id
            # user.updatedById = currentUser.id
            app.session.add(user)
            app.session.commit()

            print('host: ', host)

            # if email sender is configured
            # send email address verification email
            Auth.sendEmailAddressVerificationEmail(user_email, host)
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
        
        print('Creating new user')
        # Create user
        user = Users(
            firstName = user_email.split('@')[0], # data['firstName']
            password = password_hash,
            email = user_email,
            updatedAt = func.now()
        )
        app.session.add(user)
        app.session.flush()
        user.authenticationUid = user.id
        app.session.add(user)
        app.session.commit()
        
        # if email sender is configured
        # send email address verification email
        Auth.sendEmailAddressVerificationEmail(user_email, host)
        
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
    
    def signin(email, password, options):
        user = app.session.query(Users).filter_by(email=email).first()
        print(user)

        if not user:
            raise CustomError({'message': 'Error when signing in: User not found\n' })

        if user.disabled:
            raise CustomError({'message': 'Error when signing in: User disabled\n'})

        if not user.password:
            raise CustomError({'message': 'Error when signing in: Wrong password\n'})

        # not email sender configured
        # user.emailVerified = True

        if not user.emailVerified:
            raise CustomError({'message': 'Error when signing in: User not verified\n'})

        # TODO: Implement it!!
        # check if entered password match the user password saved in BD
        # password_match =
        if not check_password_hash(user.password, password):
            raise CustomError({'message': 'Error when signing in: Wrong password\n'})

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


    def sendEmailAddressVerificationEmail(email, host):
        print('sendEmailAddressVerificationEmail')
        # GENERATE EMAIL VERIFICATIOB TOKEN
        options = {}
        token = UserDBApi.generate_email_verification_token(email, options)
        link = f'{host}/auth/verify-email?token={token}'
        print(link)

        # send email
        subject = 'Verify your email for %s' % app.config['APP_TITLE']
        print(subject)
        # TODO: Remove it. Use it for debug
        if os.environ['FLASK_DEV']:
            email = 'vladprivalov1990@gmail.com'
        print(email)
        msg = Message(subject,  sender=app.config['MAIL_DEFAULT_SENDER'], recipients = [email])
        msg.html = render_template('mail/email_verification.html',
                                   link=link, app_title=app.config['APP_TITLE'])
        mail.send(msg)
    
    def sendPasswordResetEmail(email, host, type='register'):
        pass
    
    def verify_email(token, options):
        user = app.session.query(Users)\
            .filter(Users.emailVerificationToken==token)\
            .filter(Users.emailVerificationTokenExpiresAt > datetime.datetime.utcnow())\
            .first()
        print(user)
        if not user:
            raise CustomError({'message': 'Error when verifying email: Invalid token\n' })

        # mark email verified
        # current_user = options.user
        user = app.session.query(Users)\
            .filter_by(id=user.id)\
            .first()
        print(user)
        user.emailVerified = True
        #user.updatedById  = current_user.id
        app.session.add(user)
        app.session.commit()
        return True

