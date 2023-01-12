from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db import get_db
from repository.users import get_user_by_id_from_db, get_user_by_email_from_db
from schemas.user import UserShow

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/{user_id}', response_model=UserShow, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return get_user_by_id_from_db(user_id=user_id, db=db)


@router.get('/find/{email}', response_model=UserShow, status_code=status.HTTP_200_OK)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    return get_user_by_email_from_db(email=email, db=db)
