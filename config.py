# Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
DATABASE_URI = "postgres+psycopg2://postgres:123@localhost/user_management"

class Config:
    UPLOAD_FOLDER = 'static/'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    SECRET_KEY = "\x88\xc7\x12I\xc1\x8b\xcf\xc5\x16\xc2\xefG\x92}\x8e\xe84Y\x19\x8d\xc7\xdd9\xbd"
    APP_TITLE = 'Application'
    MAIL_SERVER = "smtp.googlemail.com" # 'smtp.gmail.com' # os.environ.get('MAIL_SERVER')
    MAIL_PORT = 587 # 465 # 8025 # 
    MAIL_USE_TLS=1
    MAIL_DEFAULT_SENDER = "support@flatlogic.com"
    MAIL_USERNAME = "support@flatlogic.com"
    MAIL_PASSWORD="UBU2JGC2wEqc"

class DevConfig(Config):
    EMAIL_ADDRESS = 'vladprivalov1990@gmail.com'
