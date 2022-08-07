
from enum import auto
from http import server
from os import stat
from sqlite3 import IntegrityError
import string
from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
from sqlalchemy import desc
from . import models
from .database import engine, get_db
from sqlalchemy.exc import IntegrityError
from .utils import hash
from .routers import post, user, auth, vote
from . import schemas
from app import utils
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

#no need, we have alembic
#models.Base.metadata.create_all(bind=engine)





# from passlib.context import CryptContext
# pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

import time
import psycopg2
from psycopg2.extras import RealDictCursor
# SELECT name, price, id FROM products where ;
# select name, price, id from products where name like '%tv%' order by id desc, price desc limit 2 offset 1;

# insert into products (price, name, inventory) values ('werid thing', 222123, 3322);


# select * from products;




# update betterposts set user_id = 13;
# select * from betterusers;



# select * from betterposts;

# select name, id from products where name like '%handmade%' order by id asc limit 1;

# insert into products (name, price, inventory) values ('thingy', 23222, 43) returning *;
# update products set name = 'simple staff', price=444 where name like '%awesome%' returning *;


app = FastAPI()

#from any website. to be removed.
origins = ['*']
app.add_middleware(CORSMiddleware,
allow_origins = origins,
allow_credentials = True,
allow_methods = ['*'],
allow_headers = ['*'])
    

@app.get('/sqlalch')
async def testing_alchemy(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    


@app.get('/')
async def root():
    return {'message': 'Hello world'}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)