from flask import render_template
from flask_mail import Message
from app import CustomError
from app import app, mail
from app.auth.notifications import EMAIL_CONFIG

class EmailSender:
    def __init__(self, email, email_type):
        self.email = email
        # self.email_type = email_type
        self.config = EMAIL_CONFIG[email_type]

    def send(self, data):
        if not EmailSender.isConfigured():
            raise CustomError({'message': 'Error when sending email: Email provider is not configured. Please configure it in config.py\n'})
        msg = Message(self.config['subject'], sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[self.email])
        msg.html = render_template(self.config['html_template'], **data)
        mail.send(msg)

    def isConfigured():
        return (app.config['MAIL_DEFAULT_SENDER'] and app.config['MAIL_SERVER'])
