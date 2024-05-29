from uuid import UUID
from fastapi import APIRouter, Depends
from auth.oauth2 import get_current_user, admin_check
from models.role import Role
from schemas.role import RoleUpdate
from schemas.user import UserPrivate
from models.user import User


router = APIRouter(
    prefix="/role",
    tags=["Role"]
)


@router.patch("/{uuid}", response_model=UserPrivate)
async def update(uuid: UUID, request: RoleUpdate, current_user: UserPrivate = Depends(get_current_user), is_admin: bool = Depends(admin_check)):
    update_data = await User.find_one(User.uuid == uuid, fetch_links=True)

    update_data.role = await Role.find_one(Role.name == request.name)

    await update_data.save()

    return update_data
