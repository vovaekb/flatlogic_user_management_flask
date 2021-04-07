import os

ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'
AUTHORIZATION_SCOPE = 'openid email profile'
AUTH_REDIRECT_URI = "http://127.0.0.1:5000/auth/signin/google/callback" # os.environ.get("FN_AUTH_REDIRECT_URI", default=False)
BASE_URI = "http://127.0.0.1:5000" # os.environ.get("FN_BASE_URI", default=False)
CLIENT_ID = os.environ.get("FN_CLIENT_ID", default=False)
CLIENT_SECRET = os.environ.get("FN_CLIENT_SECRET", default=False)
AUTH_TOKEN_KEY = 'auth_token'
AUTH_STATE_KEY = 'auth_state'
