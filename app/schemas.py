from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class UserCreat(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    creat: datetime


class PostOut(BaseModel):
    title: str
    content: str
    pub: bool = True 
    id: int
    creat: datetime
    owner_id: int
    owner: UserOut
    votes: int

class PostBase(BaseModel):
    title: str
    content: str
    pub: bool = True
    

class PostCreat(PostBase):
    pass

class Post(BaseModel):
    title: str
    content: str
    pub: bool = True 
    id: int
    creat: datetime
    owner_id: int





     
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserfromDB(BaseModel):
    email: EmailStr
    password: str
    id: int
    creat: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None



class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)