


import string
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
from sqlalchemy import desc
from .. import models, schemas, oauth2
from ..database import engine, get_db
from sqlalchemy.exc import IntegrityError
from ..utils import hash

from .. import schemas





router = APIRouter(prefix='/posts', tags=['posts'])


    







@router.get('/', response_model=List[schemas.ResponsePost])
async def get_posts(db: Session = Depends(get_db), limit : int = 5, page : int = 0, search : Optional[str] = ""):
    # cursor.execute(""" select * from posts;""")
    # posts = cursor.fetchall()

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(limit * page).all()
    return posts
    # return {'data' : my_posts}

    # return {'data': 'this is your post'}


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost)
async def create_post(payload: schemas.CreatePost, db: Session = Depends(get_db),user_id: int =  Depends(oauth2.get_current_user)):
    # cursor.execute(""" insert into posts (title, content, published) values (%s, %s, %s) returning *;""",
    #                (payload.title, payload.content, payload.published))
    # conn.commit()
    #return {'data' : cursor.fetchone()}
    obtained_id = await user_id
    posts = models.Post(**payload.dict(), user_id = obtained_id.id)
    db.add(posts)
    db.commit()
    db.refresh(posts)
    return posts
    # post_dict = payload.dict()
    # post_dict['id'] = randrange(1, 2048)
    # my_posts.append(post_dict)
    # return {'data': post_dict}


# async def find_post(id):
#     for post in my_posts:
#         if post['id'] == id:
#             return post
#     return None


@router.get('/latest', response_model=schemas.ResponsePost)
async def get_latest_post(db: Session = Depends(get_db)):
    # result = my_posts[-1]
    # return {'post_detail': result}

    # cursor.execute("""select * from posts order by id desc limit 1;""")
    # searchedpost = cursor.fetchone()
    # if searchedpost is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='there are no posts in the db')
    # return {'data': searchedpost}

    lastpost = db.query(models.Post).order_by(desc(models.Post.id)).limit(1).all()
    if lastpost is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='there are no posts in the db')
    return lastpost


@router.get('/{id}', response_model=schemas.ResponsePost)
async def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute("""select * from posts where id = %s""", (str(id),))
    # searchedpost = cursor.fetchone()
    # if searchedpost is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                     detail=f'post with id: {id} was not found')

    # return {'data': searchedpost}

    lookedup = db.query(models.Post).filter(models.Post.id == id).first()
    if lookedup is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'post with id: {id} was not found')
    return lookedup


    # result = await find_post(id)
    # if result is not None:
    #     return {'post_detail': result}
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                     detail=f'post with id: {id} was not found')
    #response.status_code = status.HTTP_404_NOT_FOUND
    # return {'post_detail': 'no post found'}

    # print(payload.dict())
    # return {'data': payload.dict()}
    # return {'new_post': f"title {payload['title']} content {payload['content']}"}


# async def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#            return i


@router.delete('/{id}')
async def delete_post(id: int, db: Session = Depends(get_db),user_id: int =  Depends(oauth2.get_current_user)):

    # cursor.execute("""delete from posts where id = %s returning *;""", (str(id),))
    # res = cursor.fetchone()
    # if res is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                     detail=f'post with id: {id} was not found')
    # conn.commit()
    # return Response(status_code=status.HTTP_204_NO_CONTENT)


    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'post with id: {id} was not found')
    obtained_id = await user_id
    if obtained_id.id  != post.first().user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f'you are not the owner of the post')
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



    # searched_index = await find_index_post(id)
    # if searched_index is not None:
    #     my_posts.pop(searched_index)
    #     return Response(status_code=status.HTTP_204_NO_CONTENT)
    # # return Response(status_code=status.HTTP_404_NOT_FOUND)
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                     detail=f'an item with id: {id} could not be found')


@router.put('/{id}', response_model=schemas.ResponsePost)
async def update_post(id: int, post: schemas.UpdatePost, response: Response, db: Session = Depends(get_db),user_id: int =  Depends(oauth2.get_current_user)):
    # cursor.execute("""update posts set title = %s, content = %s, published = %s where id = %s returning *;""", (post.title, post.content, str(post.published), str(id)))
    # res = cursor.fetchone()
    # if res is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'no post with id = {id} found')
    # conn.commit()
    # return {'data': res}

    itemquery = db.query(models.Post).filter(models.Post.id == id)
    if itemquery.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'no post with id = {id} found')
    itemquery.update(post.dict(), synchronize_session=False)
    db.commit()
    #db.refresh(itemquery.first())
    return itemquery.first()
    

    # searched_index = await find_index_post(id)
    # if searched_index is not None:
    #     my_posts[searched_index] = post
    #     response.status_code = status.HTTP_202_ACCEPTED
    #     return {'message': post.dict()}
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                     detail=f'an item with id: {id} could not be found')
    # return {'message': 'upd_post'}
