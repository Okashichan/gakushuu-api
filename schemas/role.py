from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID


class RolesEnum(Enum):
    ADMIN = 'admin'
    LINGUIST = 'linguist'
    USER = 'user'


class RoleBase(BaseModel):
    """
    Shared Role properties.
    """
    uuid: UUID
    name: str


class RoleUpdate(BaseModel):
    """
    Shared Role properties for updating.
    """
    model_config = ConfigDict(use_enum_values=True)

    name: RolesEnum = Field(default=RolesEnum.USER, validate_default=True)
