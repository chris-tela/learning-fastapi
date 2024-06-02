from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

# uses pydantic BaseModel so that it can tell fastAPI what the schema of a post should look like
# in this case the title and content should both be strings

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str
    priv: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):

    id: int
    created_at: datetime
    user_id: int 
    owner: UserOut

    # pydantic converting it to a pydantic model
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    #ensures email is valid
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass 



class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
