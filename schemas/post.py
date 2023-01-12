from pydantic import BaseModel

from .user import User


class PostBase(BaseModel):
    title: str
    body: str


class PostCreate(PostBase):
    pass


class Likes(BaseModel):
    post_id: int


class Dislikes(BaseModel):
    post_id: int


class Post(PostBase):
    id: int
    author: User
    author_id: int

    class Config:
        orm_mode = True


class PostShow(BaseModel):
    Post: Post
    likes: int = 0
    dislikes: int = 0

    class Config:
        orm_mode = True
