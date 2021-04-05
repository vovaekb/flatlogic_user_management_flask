import os
import datetime
from hashlib import pbkdf2_hmac
import jwt
from flask import render_template
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from app.models import Users
from app import app
from app import CustomError
from app.services.email import EmailSender
from app.users.services import UserDBApi


def validate_user_input(input_type, **kwargs):
    if input_type == "authentication":
        if len(kwargs["email"]) <= 255 and len(kwargs["password"]) <= 255:
            return True
        else:
            return False

'''
def generate_salt():
    salt = os.urandom(16)
    return salt.hex()
'''

def generate_token(payload):
    print('generate_token')
    token = jwt.encode(
        payload,
        app.config.get('SECRET_KEY'),
        algorithm='HS256'
    )
    print(f'{token}')
    return token


'''
def generate_hash(plain_password, password_salt):
    password_hash = pbkdf2_hmac(
        "sha256",
        b"%b" % bytes(plain_password, "utf-8"),
        b"%b" % bytes(password_salt, "utf-8"),
        10000
    )
    return password_hash.hex()
'''

# Auth service class
class Auth:
    def signup(email, password, host, current_user=None):
        print('Auth.sign()')
        user_email = email
        print('user_email: ', user_email)
        user = app.session.query(Users).filter_by(email=user_email).first()
        print(user)
        user_password = password
        print('user_password: ', user_password)
        # password_salt = generate_salt()
        # print(password_salt)
        # password_hash = generate_hash(user_password, password_salt)
        password_hash = generate_password_hash(user_password, method='sha256')
        print(password_hash)

        if user:
            print(user.authenticationUid)
            if user.authenticationUid:
                raise CustomError({'message': 'Error when registering user in database: Email already in use\n' })

            if user.disabled:
                raise CustomError({'message': 'Error when registering user in database: User disabled \n' })

            # update password
            user = UserDBApi.update_password(user.id, password_hash, current_user)

            print('host: ', host)

            # if email sender is configured
            # send email address verification email
            if EmailSender.isConfigured():
                Auth.send_email_address_verification_email(user_email, host)

            token_expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=6)
            data = {
                "exp": token_expires_at,
                "iat": datetime.datetime.utcnow(),
                "id": str(user.id),
                "email": str(user.email)
            }
            # return JWT sign with data
            token = generate_token(data)
            print(token)
            return token
        
        print('Creating new user')
        # Create user
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
        if not EmailSender.isConfigured():
            user.emailVerified = True
            app.session.add(user)
            app.session.commit()

        if not user.emailVerified:
            raise CustomError({'message': 'Error when signing in: User not verified\n'})

        # check if entered password match the user password saved in BD
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


    def send_email_address_verification_email(email, host):
        print('Auth.send_email_address_verification_email')
        if not EmailSender.isConfigured():
            raise CustomError({'message': 'Error when sending email: Email provider is not configured. Please configure it in config.py\n'})
        # Generate email verification token
        try:
            token = UserDBApi.generate_email_verification_token(email)
            link = f'{host}/auth/verify-email?token={token}'
            print(link)
        except Exception as e:
            print(str(e))
            # Validation Error
            raise CustomError({'message': 'Error during generating email address verification token occurred %s\n' % str(e)})

        # send email
        # TODO: Remove it. Use it for debug
        if os.environ['FLASK_DEV']:
            email = 'vladprivalov1990@gmail.com'
        print(email)
        email_sender = EmailSender(email, 'email_address_verification')
        data = {
            'link': link,
            'title': app.config['APP_TITLE']
        }
        email_sender.send(data)

    def send_password_reset_email(email, host, type='register'):
        print('Auth.send_password_reset_email')
        if not EmailSender.isConfigured():
            raise CustomError({
                'message': 'Error when sending email: Email provider is not configured. Please configure it in config.py\n'
            })
        try:
            token = UserDBApi.generate_password_reset_token(email)
            link = f'{host}/auth/password-reset?token={token}'
            print(link)
        except Exception as e:
            print(str(e))
            # Validation Error
            raise CustomError({'message': 'Error during generating password reset token occurred %s\n' % str(e)})

        # send email
        # TODO: Remove it. Use it for debug
        if os.environ['FLASK_DEV']:
            email = 'vladprivalov1990@gmail.com'
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

    def password_update(current_password, new_password, current_user=None):
        print('Auth.password_update')
        # currentUser = options.currentUser
        if not current_user:
            raise CustomError({'message': 'Error when updating password: Forbidden\n'})

        if not check_password_hash(current_user.password, current_password):
            raise CustomError({'message': 'Error when updating password: Wrong password\n'})

        if check_password_hash(current_user.password, new_password):
            raise CustomError({'message': 'Error when updating password: The same password\n'})

        password_hash = generate_password_hash(new_password, method='sha256')
        print(password_hash)

        user = UserDBApi.update_password(current_user.id, password_hash, current_user)
        return user

    def password_reset(token, password, current_user=None):
        # find user by password reset token
        user = app.session.query(Users) \
            .filter(Users.passwordResetToken == token) \
            .filter(Users.passwordResetTokenExpiresAt > datetime.datetime.utcnow()) \
            .first()
        print(user)
        if not user:
            raise CustomError({'message': 'Error when reset password: invalid token\n'})

        password_hash = generate_password_hash(password, method='sha256')
        print(password_hash)

        user = UserDBApi.update_password(user.id, password_hash, current_user)
        print(user)
        return user


    def verify_email(token, current_user=None):
        user = app.session.query(Users)\
            .filter(Users.emailVerificationToken==token)\
            .filter(Users.emailVerificationTokenExpiresAt > datetime.datetime.utcnow())\
            .first()
        print(user)
        if not user:
            raise CustomError({'message': 'Error when verifying email: Invalid token\n' })

        # mark email verified
        UserDBApi.mark_email_verified(user.id, current_user)
        return True

    def update_profile(data, current_user):
        user = app.session.query(Users).filter_by(id=current_user.id).first()
        print(user)
        UserDBApi.update(current_user.id, data, current_user)

