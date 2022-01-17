from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt_handler import decode_jwt


class JWTBEARER(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBEARER, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBEARER, self).__call__(request)
        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(status_code=403, detail='Invalid scheme')
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail='Invalid scheme')


def verify_jwt_token(jwtoken: str):
    is_token_valid: bool = False
    payload = decode_jwt(jwtoken)
    if payload:
        is_token_valid = True
    return is_token_valid
