from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False
    
    


class CreatePost(PostBase):
    pass
class UpdatePost(PostBase):
    pass




class UserBase(BaseModel):
    email: EmailStr
    

class CreateUser(UserBase):
    password: str

class ResponseUser(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    token: str
    token_type: str
    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id: Optional[int] = None  


class ResponsePost(PostBase):
    id: int
    created_at: datetime
    user_id: Optional[int] = None
    user: ResponseUser

    class Config:
        orm_mode = True
