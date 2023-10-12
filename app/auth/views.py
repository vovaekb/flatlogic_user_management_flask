import flask
from authlib.client import OAuth2Session
from flask import render_template, Blueprint, request, Response, jsonify, redirect, abort

from app import CustomError, ValidationError, ForbiddenError, get_current_user, no_cache
from app import app
from app.auth import (
    AUTHORIZATION_URL,
    ACCESS_TOKEN_URI,
    AUTHORIZATION_SCOPE,
    AUTH_REDIRECT_URI,
    AUTH_STATE_KEY,
    BASE_URI,
    CLIENT_ID,
    CLIENT_SECRET,
    AUTH_TOKEN_KEY
)
from app.auth.services import Auth, EmailSender
from app.serializers import UsersSchema

auth_blueprint = Blueprint('auth', __name__, template_folder='templates')
user_schema = UsersSchema()


@auth_blueprint.errorhandler(CustomError)
def handle_error(e):
    details = e.args[0]
    return Response(details['message'], status=500, mimetype='text/plain')


@auth_blueprint.errorhandler(ValidationError)
def handle_validation_error(e):
    details = e.args[0]
    return Response(details['message'], status=400, mimetype='text/plain')


@auth_blueprint.errorhandler(ForbiddenError)
def handle_forbidden_error(e):
    details = e.args[0]
    return Response(details['message'], status=403, mimetype='text/plain')


@app.errorhandler(401)
def resource_not_found(e):
    return jsonify(error=str(e)), 401


# ROUTES
@auth_blueprint.route('/auth/password-reset', methods=['PUT'])
@get_current_user
def password_reset(current_user):
    user = Auth.password_reset(request.json['token'], request.json['password'], current_user)
    payload = user_schema.dump(user)
    return jsonify(payload)


@auth_blueprint.route('/auth/password-update', methods=['PUT'])
@get_current_user
def password_update(current_user):
    user = Auth.password_update(request.json['currentPassword'], request.json['newPassword'], current_user)
    data = user_schema.dump(user)
    return jsonify(data)


@auth_blueprint.route('/auth/send-email-address-verification-email', methods=['POST'])
@get_current_user
def send_email_address_verification_email(current_user):
    if not current_user:
        raise ForbiddenError({'message': 'Email address verification error: Forbidden\n'})
    # not presenting and not passed to send_email_address_verification_email() in NodeJS implementation
    referrer = request.headers.get("Referer")
    Auth.send_email_address_verification_email(current_user.email, referrer)
    payload = True
    return Response(str(payload), status=200)


@auth_blueprint.route('/auth/send-password-reset-email', methods=['POST'])
def send_password_reset_email():
    referrer = request.headers.get("Referer")
    Auth.send_password_reset_email(request.json['email'], referrer, 'register')
    payload = True
    return Response(str(payload), status=200)


@auth_blueprint.route('/auth/signin/local', methods=['POST'])
def signin_local():
    payload = Auth.signin(request.json['email'], request.json['password'])
    resp = Response(payload, status=200)
    return resp


@auth_blueprint.route('/auth/signup', methods=['POST'])
@get_current_user
def signup(current_user):
    referrer = request.headers.get("Referer")
    payload = Auth.signup(request.json['email'], request.json['password'], referrer, current_user)
    return Response(payload, status=200)


@auth_blueprint.route('/auth/profile', methods=['PUT'])
@get_current_user
def profile(current_user):
    if not current_user:
        raise ForbiddenError({'message': 'Loading profile error: Forbidden\n'})

    Auth.update_profile(request.json['profile'], current_user)
    payload = True
    return Response(str(payload), status=200)


@auth_blueprint.route('/auth/verify-email', methods=['PUT'])
@get_current_user
def verify_email(current_user):
    payload = Auth.verify_email(request.json['token'], current_user)
    return Response(str(payload), status=200)


@auth_blueprint.route('/auth/me', methods=['GET'])
@get_current_user
def me(current_user):
    if not current_user:
        raise ForbiddenError({'message': 'Loading profile error: Forbidden\n'})
    data = user_schema.dump(current_user)
    print(data)
    return jsonify(data)


@auth_blueprint.route('/auth/email-configured', methods=['GET'])
def email_configured():
    payload = EmailSender.isConfigured()
    print(payload)
    return Response(str(payload), status=200)


@auth_blueprint.route('/auth/signin/google', methods=['GET'])
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
@no_cache
def signin_google_callback():
    req_state = request.args.get('state', default=None, type=None)
    app_url = request.args.get('app') if 'app' in request.args else BASE_URI

    if req_state != flask.session[AUTH_STATE_KEY]:
        # return response
        abort(401, description='Invalid state parameter')

    # Generate token
    token = Auth.signin_google_callback(request.url)

    redirect_url = '%s/#/login?token=%s' % (app_url, token)

    # redirect to /login endpoint
    return redirect(redirect_url, code=302)


@auth_blueprint.route('/auth/signin/microsoft', methods=['GET'])
def signin_microsoft():
    return Response('signin/microsoft', status=200)


@auth_blueprint.route('/auth/signin/microsoft/callback', methods=['GET'])
def signin_microsoft_callback():
    return Response('signin_microsoft_callback', status=200)
