import os

ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'
AUTHORIZATION_SCOPE = 'openid email profile'
AUTH_REDIRECT_URI = 'http://localhost:8080/api/auth/signin/google/callback' # os.environ.get('FN_AUTH_REDIRECT_URI', default=False)
BASE_URI = 'http://localhost:3000' # 8080' # os.environ.get('FN_BASE_URI', default=False)
CLIENT_ID = '671001533244-kf1k1gmp6mnl0r030qmvdu6v36ghmim6.apps.googleusercontent.com' 
CLIENT_SECRET = 'Yo4qbKZniqvojzUQ60iKlxqR' 
AUTH_TOKEN_KEY = 'auth_token'
AUTH_STATE_KEY = 'auth_state'



