from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import get_db
from schemas.post import PostCreate, Likes, Dislikes
from models.post import Post, Like, Dislike
from auth.oauth2 import get_current_user
from utils.posts import get_posts_from_db, check_post_author, check_like_in_db, check_dislike_in_db, get_post_from_db


def create_post_in_db(post: PostCreate, author: int = Depends(get_current_user), db: Session = Depends(get_db)) -> Post:
    post_db = Post(**dict(post), author_id=author)
    db.add(post_db)
    db.commit()
    db.refresh(post_db)
    return post_db


def get_all_posts_from_db(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = get_posts_from_db(db=db).group_by(Post.id).limit(limit=limit).offset(offset=offset).all()
    return posts


def get_post_by_id_from_db(post_id: int, db: Session = Depends(get_db)):
    post = get_posts_from_db(db=db).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Пост с id {post_id} не найден!')
    return post


def like_post_db(like: Likes, author_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    is_author = check_post_author(post_id=like.post_id, user_id=author_id, db=db)
    if is_author:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Вы не можете лайкать собственный пост!')
    check_like = check_like_in_db(post_id=like.post_id, author_id=author_id, db=db)
    check_dislike_in_db(post_id=like.post_id, author_id=author_id, db=db)
    if check_like:
        return {
            "message": f"Лайк успешно убран!"
        }
    like = Like(**dict(like), user_id=author_id)
    db.add(like)
    db.commit()
    return {
        "message": f"Лайк успешно поставлен!"
    }


def dislike_post_db(dislike: Dislikes, author_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    is_author = check_post_author(post_id=dislike.post_id, user_id=author_id, db=db)
    if is_author:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Вы не можете дислайкать собственный пост!')
    check_dislike = check_dislike_in_db(post_id=dislike.post_id, author_id=author_id, db=db)
    check_like_in_db(post_id=dislike.post_id, author_id=author_id, db=db)
    if check_dislike:
        return {
            "message": f"Дислайк успешно убран!"
        }
    dislike = Dislike(**dict(dislike), user_id=author_id)
    db.add(dislike)
    db.commit()
    return {
        "message": f"Дислайк успешно поставлен!"
    }


def delete_post_from_db(post_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    post = get_post_from_db(post_id=post_id, user_id=user_id, db=db)
    post.delete()
    db.commit()
    return {
        "message": f"Пост с id {post_id} успешно удален!"
    }


def update_post_in_db(post_id: int, request: PostCreate, user_id: int = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    post = get_post_from_db(post_id=post_id, user_id=user_id, db=db)
    post.update(request.dict())
    db.commit()
    return post.first()
