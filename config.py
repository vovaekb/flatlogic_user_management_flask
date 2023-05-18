import os

DATABASE_URI = os.environ.get('DB_PROD')

providers = {
    'LOCAL': 'local',
    'GOOGLE': 'google'
}


class Config:
    UPLOAD_FOLDER = 'static/'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    SECRET_KEY = os.environ.get('SECRET_KEY')
    APP_TITLE = 'Application'
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_DEFAULT_SENDER = 'support@flatlogic.com'
    MAIL_USERNAME = 'support@flatlogic.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


class DevConfig(Config):
    EMAIL_ADDRESS = 'vladprivalov1990@gmail.com'
    REMOTE = 'http://localhost:5000'


class ProductionConfig(Config):
    REMOTE = 'https://sing-generator-node.herokuapp.com'
