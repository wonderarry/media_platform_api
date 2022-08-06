
import string
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from .. import models
from ..database import engine, get_db
from sqlalchemy.exc import IntegrityError
from ..utils import hash

from .. import schemas
from app import utils

router = APIRouter(prefix='/users', tags = ['users'])

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseUser)
async def create_user(userdata: schemas.CreateUser, db: Session = Depends(get_db)):
    userdata.password = utils.hash(userdata.password)
    new_user = models.User(**userdata.dict())
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                         detail=f'a user with such email already exists')
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schemas.ResponseUser)
async def get_user(id: int, db: Session = Depends(get_db)):
    searchquery = db.query(models.User).filter(models.User.id == id)
    if searchquery.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'no user with id = {id} in system')
    return searchquery.first()
  