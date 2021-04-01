import os
from flask import Flask, _app_ctx_stack, render_template, request, jsonify, Response
from flask_mail import Mail
import jwt
from functools import wraps
from sqlalchemy.orm import scoped_session
from app.database import SessionLocal, engine, Base
from app.models import Users
from config import Config, DevConfig

# Create database structure
#Base.metadata.create_all(bind=engine)

FILE_FOLDER = 'static/'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
print(APP_ROOT)

app = Flask(__name__)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

if os.environ['FLASK_DEV']:
    app.config.from_object(DevConfig)
else:
    app.config.from_object(Config)

print(app.config['UPLOAD_FOLDER'])
print(app.config['MAIL_SERVER'])
#app.config['UPLOAD_FOLDER'] = FILE_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

mail = Mail(app)

# Global methods and classes

# Error handlers
class CustomError(Exception):
    pass


def get_current_user(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        print('get_current_user')

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
            print('token: ', token)

            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
                print(data)
                current_user = app.session.query(Users) \
                    .filter(Users.id == data['id']) \
                    .filter(Users.email==data['email']).first()
                print(current_user)
            except Exception as e:
                print('Error when decoding token: ', str(e))
                raise CustomError({'message': 'Error when verifying token: token is invalid\n'})
        else:
            current_user = None

        return f(current_user, *args, **kwargs)
    return decorator

'''
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        print('token_required')
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
            print('token: ', token)

        if not token:
            raise CustomError({'message': 'Error when verifying token: a valid token is missing\n'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
            print(data)
            current_user = app.session.query(Users) \
                .filter(Users.id == data['id']) \
                .filter(Users.email==data['email']).first()
            print(current_user)
        except Exception as e:
            print('Error when decoding token: ', str(e))
            raise CustomError({'message': 'Error when verifying token: token is invalid\n'})

        return f(current_user, *args, **kwargs)
    return decorator
'''

def token_included(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        print('token_included')
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
            print('token: ', token)

        if not token:
            current_user = None

# BLUEPRINTS
from app.auth.views import auth_blueprint
from app.files.views import files_blueprint
from app.users.views import users_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(files_blueprint)
app.register_blueprint(users_blueprint)

# from app import views
