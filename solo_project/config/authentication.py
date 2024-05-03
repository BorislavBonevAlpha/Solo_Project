from time import time
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError
from base_models.token_model import TokenData
from db_models import sqlalchemy_script
from config.db_engine import db_dependency, read_query
from services.authorization_service import is_authenticated

oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(db: db_dependency, token: str = Depends(oauth_2_scheme)):
    credential_exception = HTTPException(status_code=401,
                                         detail='Could not validate credentials',
                                         headers={'WWW-AUTHENTICATE': 'Bearer'})

    try:
        payload = is_authenticated(token)
        username = payload.get("username")
        if username is None:
            raise credential_exception

        token_data = TokenData(username=username)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401,
                            detail='Expired token.')
    current_property = 'username'
    user_info = read_query(sqlalchemy_script.User,db,token_data.username, current_property)

    if user_info is None:
        raise credential_exception
    
    return user_info