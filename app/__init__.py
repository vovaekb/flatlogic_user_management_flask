import os
from flask import Flask, _app_ctx_stack, render_template, request, jsonify, Response
from flask_mail import Mail
from sqlalchemy.orm import scoped_session
from app.database import SessionLocal, engine, Base
from app import models
from config import Config

# Create database structure
#Base.metadata.create_all(bind=engine)

FILE_FOLDER = 'static/'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
print(APP_ROOT)

app = Flask(__name__)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)
app.config.from_object(Config)
print(app.config['UPLOAD_FOLDER'])
print(app.config['MAIL_SERVER'])
#app.config['UPLOAD_FOLDER'] = FILE_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

mail = Mail(app)

# BLUEPRINTS
from app.auth.views import auth_blueprint
from app.files.views import files_blueprint
from app.users.views import users_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(files_blueprint)
app.register_blueprint(users_blueprint)

# from app import views
