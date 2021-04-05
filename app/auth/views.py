from flask import render_template, Blueprint, request, Response, jsonify
import jwt
# from app import database
from app import app
from app.models import Users
from app.serializers import UsersSchema, FilesSchema
from app import CustomError, get_current_user
from app.auth.services import Auth, EmailSender

# CONFIG
auth_blueprint = Blueprint('auth', __name__, template_folder='templates')

user_schema = UsersSchema()


@auth_blueprint.errorhandler(CustomError)
def handle_error(e):
    details = e.args[0]
    return Response(details['message'], status=200, mimetype='text/plain')


# ROUTES
@auth_blueprint.route('/auth/password-reset', methods=['PUT'])
@get_current_user
def password_reset(current_user):
    print(current_user)
    user = Auth.password_reset(request.json['token'], request.json['password'], current_user)
    payload = user_schema.dump(user)
    return jsonify(payload)

@auth_blueprint.route('/auth/password-update', methods=['PUT'])
@get_current_user
def password_update(current_user):
    print(current_user)
    user = Auth.password_update(request.json['current_password'], request.json['new_password'], current_user)
    data = user_schema.dump(user)
    #return Response(payload, status=200)
    return jsonify(data)

@auth_blueprint.route('/auth/send-email-address-verification-email', methods=['POST'])
@get_current_user
def send_email_address_verification_email(current_user):
    print('POST query to /auth/send-email-address-verification-email accepted')
    if not current_user:
        raise CustomError({'message': 'Error when sending email address verification email: Forbidden\n'})
    # not presenting and not passed to send_email_address_verification_email() in NodeJS implementation
    host = f'http://{request.host}'
    Auth.send_email_address_verification_email(current_user.email, host)
    payload = True
    return Response(str(payload), status=200)

@auth_blueprint.route('/auth/send-password-reset-email', methods=['POST'])
def send_password_reset_email():
    print('POST query to /auth/send-email-address-verification-email accepted')
    host = f'http://{request.host}'
    Auth.send_password_reset_email(request.json['email'], host, 'register')
    payload = True
    return Response(str(payload), status=200)

@auth_blueprint.route('/auth/signin/local', methods=['POST'])
def signin_local():
    options = {}
    payload = Auth.signin(request.json['email'], request.json['password'], options)
    return Response(payload, status=200)

@auth_blueprint.route('/auth/signup', methods=['POST'])
@get_current_user
def signup(current_user):
    host = f'http://{request.host}'
    payload = Auth.signup(request.json['email'], request.json['password'], host, current_user)

    return Response(payload, status=200)

@auth_blueprint.route('/auth/profile', methods=['PUT'])
@get_current_user
def profile(current_user):
    if not current_user:
        raise CustomError({'message': 'Error when loading profile: Forbidden\n'})

    Auth.update_profile(request.json['profile'], current_user)
    payload = True
    return Response(str(payload), status=200)

@auth_blueprint.route('/auth/verify-email', methods=['PUT'])
@get_current_user
def verify_email(current_user):
    print('Accept PUT to verify-email')
    # host = f'http://{request.host}'
    payload = Auth.verify_email(request.json['token'], current_user)
    #return Response('verify_email', status=200)
    return Response(str(payload), status=200)

@auth_blueprint.route('/auth/me', methods=['GET'])
@get_current_user
def me(current_user):
    if not current_user:
        raise CustomError({'message': 'Error when loading profile: Forbidden\n'})
    print(current_user)
    data = user_schema.dump(current_user)
    print(data)
    return jsonify(data)
    # return Response(payload, status=200)

@auth_blueprint.route('/auth/email-configured', methods=['GET'])
def email_configured():
    payload = EmailSender.isConfigured()
    return Response(str(payload), status=200)

@auth_blueprint.route('/auth/signin/google', methods=['GET'])
def signin_google():
    return Response('signin google', status=200)

@auth_blueprint.route('/auth/signin/google/callback', methods=['GET'])
def signin_google_callback():
    return Response('signin google callback', status=200)

@auth_blueprint.route('/auth/signin/microsoft', methods=['GET'])
def signin_microsoft():
    return Response('signin/microsoft', status=200)

@auth_blueprint.route('/auth/signin/microsoft/callback', methods=['GET'])
def signin_microsoft_callback():
    return Response('signin_microsoft_callback', status=200)

