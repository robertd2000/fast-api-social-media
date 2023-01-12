from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from auth.oauth2 import get_current_user

from db import get_db
from schemas.post import PostShow, PostCreate, Likes, Dislikes, Post
from repository.posts import create_post_in_db, get_all_posts_from_db, get_post_by_id_from_db, like_post_db, \
    dislike_post_db, delete_post_from_db, update_post_in_db

router = APIRouter(prefix='/posts', tags=['posts'])


@router.post('/', response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, author: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_post_in_db(post=post, author=author, db=db)


@router.get('/', response_model=list[PostShow], status_code=status.HTTP_200_OK)
def get_all_posts(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_posts_from_db(offset=offset, limit=limit, db=db)


@router.get('/{post_id}', response_model=PostShow, status_code=status.HTTP_200_OK)
def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    return get_post_by_id_from_db(post_id=post_id, db=db)


@router.post('/{post_id}/like')
def like_post(like: Likes, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return like_post_db(like=like, author_id=user_id, db=db)


@router.post('/{post_id}/dislike')
def dislike_post(dislike: Dislikes, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return dislike_post_db(dislike=dislike, author_id=user_id, db=db)


@router.delete('/{post_id}')
def delete_post(post_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return delete_post_from_db(post_id=post_id, user_id=user_id, db=db)


@router.put('/{post_id}/update', response_model=Post)
def update_post(post_id: int, request: PostCreate, user_id: int = Depends(get_current_user),
                db: Session = Depends(get_db)):
    return update_post_in_db(post_id=post_id, request=request, user_id=user_id, db=db)
