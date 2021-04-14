import os
import flask
from flask import render_template, Blueprint, request, Response, jsonify, redirect
from flask_cors import cross_origin
from authlib.client import OAuth2Session
from app import app
from app.serializers import UsersSchema
from app import CustomError, get_current_user, no_cache
from app.auth.services import Auth, EmailSender, is_logged_in
from app.auth import AUTHORIZATION_URL, ACCESS_TOKEN_URI, AUTHORIZATION_SCOPE, AUTH_REDIRECT_URI, AUTH_STATE_KEY, BASE_URI, CLIENT_ID, CLIENT_SECRET, AUTH_TOKEN_KEY

# CONFIG


auth_blueprint = Blueprint('auth', __name__, template_folder='templates')
user_schema = UsersSchema()


@auth_blueprint.errorhandler(CustomError)
def handle_error(e):
    details = e.args[0]
    return Response(details['message'], status=200, mimetype='text/plain')


# ROUTES
@auth_blueprint.route('/auth/password-reset', methods=['PUT'])
@cross_origin(supports_credentials=True)
@get_current_user
def password_reset(current_user):
    print(current_user)
    user = Auth.password_reset(request.json['token'], request.json['password'], current_user)
    payload = user_schema.dump(user)
    return jsonify(payload)

@auth_blueprint.route('/auth/password-update', methods=['PUT'])
@cross_origin(supports_credentials=True)
@get_current_user
def password_update(current_user):
    print(current_user)
    user = Auth.password_update(request.json['current_password'], request.json['new_password'], current_user)
    data = user_schema.dump(user)
    return jsonify(data)

@auth_blueprint.route('/auth/send-email-address-verification-email', methods=['POST'])
@cross_origin(supports_credentials=True)
@get_current_user
def send_email_address_verification_email(current_user):
    print('POST query to /auth/send-email-address-verification-email accepted')
    print(current_user)
    if not current_user:
        raise CustomError({'message': 'Error when sending email address verification email: Forbidden\n'})
    # not presenting and not passed to send_email_address_verification_email() in NodeJS implementation
    host = f'http://{request.host}'
    Auth.send_email_address_verification_email(current_user.email, host)
    payload = True
    return Response(str(payload), status=200)

@auth_blueprint.route('/auth/send-password-reset-email', methods=['POST'])
@cross_origin(supports_credentials=True)
def send_password_reset_email():
    print('POST query to /auth/send-email-address-verification-email accepted')
    host = f'http://{request.host}'
    Auth.send_password_reset_email(request.json['email'], host, 'register')
    payload = True
    return Response(str(payload), status=200)

@auth_blueprint.route('/auth/signin/local', methods=['POST'])
@cross_origin(supports_credentials=True)
def signin_local():
    payload = Auth.signin(request.json['email'], request.json['password'])
    return Response(payload, status=200)

@auth_blueprint.route('/auth/signup', methods=['POST'])
@cross_origin(supports_credentials=True)
@get_current_user
def signup(current_user):
    host = f'http://{request.host}'
    payload = Auth.signup(request.json['email'], request.json['password'], host, current_user)

    return Response(payload, status=200)

@auth_blueprint.route('/auth/profile', methods=['PUT'])
@cross_origin(supports_credentials=True)
@get_current_user
def profile(current_user):
    if not current_user:
        raise CustomError({'message': 'Error when loading profile: Forbidden\n'})

    Auth.update_profile(request.json['profile'], current_user)
    payload = True
    return Response(str(payload), status=200)

@auth_blueprint.route('/auth/verify-email', methods=['PUT'])
@cross_origin(supports_credentials=True)
@get_current_user
def verify_email(current_user):
    print('Accept PUT to verify-email')
    payload = Auth.verify_email(request.json['token'], current_user)
    return Response(str(payload), status=200)

@auth_blueprint.route('/auth/me', methods=['GET'])
@cross_origin(supports_credentials=True)
@get_current_user
def me(current_user):
    if not current_user:
        raise CustomError({'message': 'Error when loading profile: Forbidden\n'})
    print(current_user)
    data = user_schema.dump(current_user)
    print(data)
    return jsonify(data)

@auth_blueprint.route('/auth/email-configured', methods=['GET'])
@cross_origin(supports_credentials=True)
def email_configured():
    payload = EmailSender.isConfigured()
    print(payload)
    return Response(str(payload), status=200)

@auth_blueprint.route('/auth/signin/google', methods=['GET'])
@cross_origin(supports_credentials=True)
@no_cache
def signin_google():
    # state = request.args.get('app')
    session = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                            scope=AUTHORIZATION_SCOPE,
                            redirect_uri=AUTH_REDIRECT_URI)

    uri, state = session.authorization_url(AUTHORIZATION_URL)

    flask.session[AUTH_STATE_KEY] = state
    flask.session.permanent = True

    return redirect(uri, code=302)

@auth_blueprint.route('/auth/signin/google/callback', methods=['GET'])
@cross_origin(supports_credentials=True)
@no_cache
def signin_google_callback():
    req_state = request.args.get('state', default=None, type=None)
    app_url = request.args.get('app') if 'app' in request.args else BASE_URI

    if req_state != flask.session[AUTH_STATE_KEY]:
        # response = flask.make_response('Invalid state parameter', 401)
        # return response
        raise CustomError({'message': 'Error when signing in with Google: Invalid state parameter\n'})

    '''
    session = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                            scope=AUTHORIZATION_SCOPE,
                            state=flask.session[AUTH_STATE_KEY],
                            redirect_uri=AUTH_REDIRECT_URI)

    oauth2_tokens = session.fetch_access_token(
        ACCESS_TOKEN_URI,
        authorization_response=request.url)

    flask.session[AUTH_TOKEN_KEY] = oauth2_tokens
    '''

    # Generate token
    token = Auth.signin_google_callback(request.url)

    redirect_url = '%s/login?token=%s' % (app_url, token)

    # TODO: redirect to /login endpoint
    return redirect(redirect_url, code=302)

@auth_blueprint.route('/auth/signin/microsoft', methods=['GET'])
def signin_microsoft():
    return Response('signin/microsoft', status=200)

@auth_blueprint.route('/auth/signin/microsoft/callback', methods=['GET'])
def signin_microsoft_callback():
    return Response('signin_microsoft_callback', status=200)

