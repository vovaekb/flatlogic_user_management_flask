from flask import render_template, Blueprint, request, Response, jsonify
import jwt
# from app import database
from app import app
from app.auth.services import generate_salt, generate_hash, Auth
from app.models import Users
from app.serializers import UsersSchema, FilesSchema
from app import CustomError, token_required

# CONFIG
auth_blueprint = Blueprint('auth', __name__, template_folder='templates')


@auth_blueprint.errorhandler(CustomError)
def handle_error(e):
    details = e.args[0]
    return Response(details['message'], status=200, mimetype='text/plain')


# ROUTES
@auth_blueprint.route('/auth/password-reset', methods=['PUT'])
def password_reset():
    return Response('password reset', status=200)

@auth_blueprint.route('/auth/password-update', methods=['PUT'])
@token_required
def password_update(current_user):
    options = {}
    print(current_user)
    payload = Auth.password_update(request.json['current_password'], request.json['new_password'], current_user)
    #return Response(payload, status=200)
    return jsonify(payload)

@auth_blueprint.route('/auth/send-email-address-verification-email', methods=['POST'])
def send_email_address_verification_email():
    return Response('send_email_address_verification_email', status=200)

@auth_blueprint.route('/auth/send-password-reset-email', methods=['POST'])
def send_password_reset_email():
    return Response('send-password-reset-email', status=200)

@auth_blueprint.route('/auth/signin/local', methods=['POST'])
def signin_local():
    options = {}
    payload = Auth.signin(request.json['email'], request.json['password'], options)
    return Response(payload, status=200)

@auth_blueprint.route('/auth/signup', methods=['POST'])
def signup():
    options = {}
    host = f'http://{request.host}'
    payload = Auth.signup(request.json['email'], request.json['password'], host, options)

    '''
    if user_password == user_confirm_password and validate_user_input(
        "authentication", email=user_email, password=user_password
    ):
        password_salt = generate_salt()
        password_hash = generate_hash(user_password, password_salt)
        # Save user to DB
        # If failed to save user to DB
        # return status 409
    else:
        # Registration Failed
        # return status 400
        pass
    '''

    return Response(payload, status=200)

@auth_blueprint.route('/auth/profile', methods=['PUT'])
def profile():
    return Response('profile', status=200)

@auth_blueprint.route('/auth/verify-email', methods=['PUT'])
def verify_email():
    print('Accept PUT to verify-email')
    options = {}
    # host = f'http://{request.host}'
    payload = Auth.verify_email(request.json['token'], options)
    #return Response('verify_email', status=200)
    return Response(str(payload), status=200)

@auth_blueprint.route('/auth/me', methods=['GET'])
def me():
    return Response('me', status=200)

@auth_blueprint.route('/auth/email-configured', methods=['GET'])
def email_configured():
    return Response('email_configured', status=200)

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

