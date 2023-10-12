from app import app

# Global dicts
EMAIL_CONFIG = {
    'email_address_verification': {
        'from': '',
        'subject': 'Verify your email for %s' % app.config['APP_TITLE'],
        'html_template': 'mail/email_verification.html'
    },
    'password_reset': {
        'from': '',
        'subject': 'Reset your password for %s' % app.config['APP_TITLE'],
        'html_template': 'mail/password_reset.html'
    },
    'invitation': {
        'from': '',
        'subject': 'You\'ve been invited to % s' % app.config['APP_TITLE'],
                                                                       'html_template': 'mail/invitation.html'
    }
}
