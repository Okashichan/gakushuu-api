from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm.session import Session
from auth.oauth2 import get_current_user

from database.database import get_db
from database import db_user
from routers.schemas import UserBase, UserDisplay

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
