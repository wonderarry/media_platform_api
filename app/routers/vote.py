from typing import Coroutine, List
from fastapi import APIRouter, HTTPException, status

from sqlalchemy.orm import Session
from fastapi import Depends
from ..database import get_db
from .. import schemas
from .. import models
from ..oauth2 import get_current_user
from sqlalchemy.exc import IntegrityError


router = APIRouter(tags= ['voting system'], prefix = '/votes')

@router.get('/{id}', response_model=schemas.ResponseVote)
async def get_vote_count(id, db : Session = Depends(get_db), user_id_future : Coroutine = Depends(get_current_user)):
    await user_id_future
    post_lookup = db.query(models.Post).filter(models.Post.id == id).first()
    if post_lookup is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no post with such id found')
    result = db.query(models.Vote).filter(models.Vote.post_id == id).count()
    return {'post_id' : id,'vote_count' : result}


@router.post('/{id}', response_model=schemas.ResponseVote)
async def vote_on_post(id: int, db : Session = Depends(get_db), user_id_future : Coroutine = Depends(get_current_user)):
    authed_user_id = await user_id_future
    post_lookup = db.query(models.Post).filter(models.Post.id == id).first()
    if post_lookup is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no post with such id found')

    #if you have not voted on this post, you will be upvoting it
    vote_direction: int
    existing_vote_query = db.query(models.Vote).filter(models.Vote.post_id == id).filter(models.Vote.user_id == authed_user_id.id)
    if existing_vote_query.first() is None:
        vote_direction = 1
        appended_vote = models.Vote(post_id = id, user_id = authed_user_id.id)
        db.add(appended_vote)
        
    else:
        vote_direction = -1
        existing_vote_query.delete(synchronize_session = False)

    try:
        db.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='there was an error trying to upvote the post')

    #return {'post_id': id, 'user_id': authed_user_id.id}
    votes_after_voting = db.query(models.Vote).filter(models.Vote.post_id == id).count()
    return {'post_id' : id, 'vote_count' : votes_after_voting, 'vote_direction' : int}


