from fastapi import HTTPException, status
from routers.schemas import RoleBase
from sqlalchemy.orm.session import Session
from database.models import DbRole


def create(db: Session, request: RoleBase):
    new_role = DbRole(name=request.name)

    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    return new_role


def update(db: Session, request: RoleBase, role_id: int):
    role = db.query(DbRole).filter(DbRole.id == role_id).first()

    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Role with id {role_id} not found")

    role.name = request.name

    db.commit()
    db.refresh(role)

    return {"message": f"Role with id {role_id} updated with value {request.name}"}


def delete(db: Session, role_id: int):
    role = db.query(DbRole).filter(DbRole.id == role_id).first()

    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Role with id {role_id} not found")

    db.delete(role)
    db.commit()

    return {"message": f"Role with id {role_id} deleted"}


def get_role(db: Session, role_id: int):
    role = db.query(DbRole).filter(DbRole.id == role_id).first()

    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Role with id {role_id} not found")

    return role
