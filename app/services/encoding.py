import jwt
from app import app

def generate_token(payload):
    print('generate_token')
    token = jwt.encode(
        payload,
        app.config.get('SECRET_KEY'),
        algorithm='HS256'
    )
    print(f'{token}')
    return token