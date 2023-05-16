import os

# Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
DATABASE_URI = "postgres+psycopg2://postgres:123@localhost/user_management"

providers = {
    "LOCAL": "local",
    "GOOGLE": "google"
}


class Config:
    UPLOAD_FOLDER = 'static/'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    SECRET_KEY = "HUEyqESqgQ1yTwzVlO6wprC9Kf1J1xuA" # "\x88\xc7\x12I\xc1\x8b\xcf\xc5\x16\xc2\xefG\x92}\x8e\xe84Y\x19\x8d\xc7\xdd9\xbd"
    APP_TITLE = 'Application'
    MAIL_SERVER = "smtp.googlemail.com" # os.environ.get('MAIL_SERVER')
    MAIL_PORT = 587
    MAIL_USE_TLS=1
    MAIL_DEFAULT_SENDER = "support@flatlogic.com"
    MAIL_USERNAME = "support@flatlogic.com"
    MAIL_PASSWORD="UBU2JGC2wEqc"
    # Google Auth parameters


class DevConfig(Config):
    EMAIL_ADDRESS = 'vladprivalov1990@gmail.com'
    REMOTE = "http://localhost:5000" # http://localhost:8080


class ProductionConfig(Config):
    REMOTE = "https://sing-generator-node.herokuapp.com"
