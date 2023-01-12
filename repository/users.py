from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth.hashing import Hash
from auth.token import create_access_token
from db import get_db
from schemas.user import UserCreate
from models.user import User


def create_user_in_db(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(email=user.email, username=user.username, password=Hash.bcrypt(password=user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id_from_db(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Пользователь с id {user_id} не найден!')
    return user


def get_user_by_email_from_db(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Пользователь с email {email} не найден!')
    return user


def get_user_and_check_password(request: OAuth2PasswordRequestForm, db: Session = Depends(get_db)):
    user = get_user_by_email_from_db(email=request.username, db=db)
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Incorrect password!')

    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}
