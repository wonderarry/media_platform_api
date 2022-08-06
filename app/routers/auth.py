
import string
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
from sqlalchemy import desc
from .. import models
from ..database import engine, get_db
from sqlalchemy.exc import IntegrityError
from ..utils import hash, verify
from .. import oauth2
from .. import schemas
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['authentication'])


@router.post('/login', response_model=schemas.Token)
async def user_login(creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    userlookup = db.query(models.User).filter(models.User.email == creds.username).first()
         #creds act like a dict of username and password
    if userlookup is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'wrong credentials')
    if not verify(creds.password, userlookup.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'wrong credentials')
    access_token = await oauth2.change_access_token({'user_id': userlookup.id})
    return {'token': access_token, 'token_type': 'bearer'}
    return {'token': 'example_token'}
    