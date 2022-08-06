from jose import JWTError, jwt
from datetime import datetime, timedelta
from .schemas import TokenData
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from .config import settings


# it is /login without the slash, means it is route on the website
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


async def change_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({'exp': expire})
    jwtres = jwt.encode(to_encode, settings.secretkey, algorithm=settings.algorithm)
    return jwtres


async def verify_access_token(token: str, creds_exc: Exception):
    try:
        payload = jwt.decode(token, settings.secretkey, algorithms=[settings.algorithm])
        id: str = payload.get('user_id')
        if id is None:
            raise creds_exc
        token_data = TokenData(id=id)
    except JWTError:
        raise creds_exc
    return token_data


async def get_current_user(token: str = Depends(oauth2_scheme)):
    creds_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail='could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})
    return verify_access_token(token, creds_exc)
