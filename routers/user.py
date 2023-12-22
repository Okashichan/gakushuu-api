import shutil
import string
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from sqlalchemy.orm.session import Session
from auth.oauth2 import get_current_user
from config import get_settings

from database.database import get_db
from database import db_user
from routers.schemas import UserBase, UserDisplay
import uuid

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/")
def create(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create(db, request)


@router.put("/{user_id}")
def update(user_id: int, request: UserBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_user.update(db, request, user_id)


@router.delete("/{user_id}")
def delete(user_id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_user.delete(db, user_id)


@router.get("/{user_id}", response_model=UserDisplay)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_user.get_user(db, user_id)


@router.post("/upload_avatar")
def upload_avatar(image: UploadFile = File(...), db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    new_avatar = f'{uuid.uuid4()}.'
    filename = new_avatar.join(image.filename.rsplit('.', 1))
    path = f'static/images/{filename}'

    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(image.file, buffer)

    url = f'{get_settings().APP_URL}/{path}'

    db_user.update_avatar_by_id(db, url, current_user.id)

    return {"avatar_url": url}
