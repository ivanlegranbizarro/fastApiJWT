import time
import jwt
from decouple import config


JWT_SECRET = config('secret')
JWT_ALGORITHM = config('algorithm')


def token_response(token: str):
    return {
        'access_token': token
    }


def sign_jwt(user_id: str):
    payload = {
        'user_id': user_id,
        'expiry': int(time.time()) + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=[JWT_ALGORITHM])
    return token_response(token)


def decode_jwt(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decode_token if decode_token['expiry'] >= int(time.time()) else None
    except jwt.ExpiredSignatureError:
        return None
