from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List
from sqlalchemy.orm.session import Session
from auth.oauth2 import get_current_user

from database.database import get_db
from database import db_dictionary
from routers.schemas import DictionaryBase, DictionaryDisplay, DictionaryUpdate, UserBase


router = APIRouter(
    prefix="/dictionary",
    tags=["Dictionary"]
)


@router.post("/")
def create(request: DictionaryBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_dictionary.create(db, request)


@router.put("/{dictionary_id}")
def update(dictionary_id: int, request: DictionaryUpdate, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_dictionary.update(db, request, dictionary_id)


@router.delete("/{dictionary_id}")
def delete(dictionary_id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_dictionary.delete(db, dictionary_id)


@router.get("/original/{original}", response_model=DictionaryDisplay)
def get_entry_by_original_name(original: str, db: Session = Depends(get_db)):
    return db_dictionary.get_entry_by_original_name(db, original)


@router.get("/all", response_model=List[DictionaryDisplay])
def get_all_entries(db: Session = Depends(get_db)):
    return db_dictionary.get_all_entries(db)
