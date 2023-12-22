from fastapi import HTTPException, status
from database.hash import Hash
from routers.schemas import UserBase
from sqlalchemy.orm.session import Session
from database.models import DbUser


def create(db: Session, request: UserBase):
    new_user = DbUser(username=request.username,
                      password_hash=Hash.bcrypt(request.password_hash),
                      avatar=request.avatar,
                      email=request.email,
                      created_at=request.created_at,
                      role_id=request.role_id)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def update(db: Session, request: UserBase, user_id: int):
    user = db.query(DbUser).filter(DbUser.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {user_id} not found")

    user.username = request.username
    user.password_hash = Hash.bcrypt(request.password_hash)
    user.avatar = request.avatar
    user.email = request.email
    user.created_at = request.created_at
    user.role_id = request.role_id

    db.commit()
    db.refresh(user)

    return {"message": f"User with id {user_id} updated"}


def delete(db: Session, user_id: int):
    user = db.query(DbUser).filter(DbUser.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {user_id} not found")
    db.delete(user)
    db.commit()

    return {"message": f"User with id {user_id} deleted"}


def get_user(db: Session, user_id: int):
    user = db.query(DbUser).filter(DbUser.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {user_id} not found")
    return user


def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with username {username} not found")
    return user


def update_avatar_by_id(db: Session, avatar: str, user_id: int):
    user = db.query(DbUser).filter(DbUser.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {user_id} not found")

    user.avatar = avatar

    db.commit()
    db.refresh(user)

    return {"message": f"User with id {user_id} updated"}
