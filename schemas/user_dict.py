from pydantic import BaseModel
from schemas.role import RoleUpdate


class UserOut(BaseModel):
    role: RoleUpdate
    username: str
