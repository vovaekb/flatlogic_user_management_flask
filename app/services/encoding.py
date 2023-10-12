import jwt

from app import app


def generate_token(payload):
    """Generates JWT toekn

    Args:
        payload (dict): payload for token

    Returns:
        str: generated token
    """
    token = jwt.encode(
        payload,
        app.config.get('SECRET_KEY'),
        algorithm='HS256'
    )
    print(f'{token}')
    return token
