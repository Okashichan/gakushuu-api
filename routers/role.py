from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm.session import Session
from auth.oauth2 import get_current_user

from database.database import get_db
from database import db_role
from routers.schemas import RoleBase, UserBase

router = APIRouter(
    prefix="/role",
    tags=["Role"]
)


@router.post("/")
def create(request: RoleBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_role.create(db, request)


@router.put("/{role_id}")
def update(role_id: int, request: RoleBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_role.update(db, request, role_id)


@router.delete("/{role_id}")
def delete(role_id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_role.delete(db, role_id)
