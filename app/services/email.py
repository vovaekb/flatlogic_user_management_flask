from flask import render_template
from flask_mail import Message
from app import CustomError
from app import app, mail
from app.auth.notifications import EMAIL_CONFIG


class EmailSender:
    def __init__(self, email: str, email_type: str):
        self.email = email
        self.config = EMAIL_CONFIG[email_type]

    def send(self, data: dict) -> None:
        if not EmailSender.isConfigured():
            raise CustomError({'message': 'Error when sending email: Email provider is not configured. Please configure it in config.py\n'})
        msg = Message(
            self.config['subject'], 
            sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[self.email]
        )
        msg.html = render_template(self.config['html_template'], **data)
        mail.send(msg)

    def isConfigured() -> bool:
        return (not app.config['MAIL_DEFAULT_SENDER'] is None and not app.config['MAIL_SERVER'] is None)
