from datetime import datetime
from typing import Optional, List
from beanie import Link, PydanticObjectId
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from config import settings
from schemas.role import RoleBase, RoleUpdate
from schemas.collection import CollectionBase
from schemas.stats import Stats


class UserBase(BaseModel):
    """
    Shared User properties for registration.
    """
    email: str
    username: str
    password: str
    avatar_url: Optional[str] = Field(
        default=f'{settings.APP_URL}/static/images/blank_avatar.jpg')


class UserPublic(BaseModel):
    """
    Shared User properties for public usage.
    """
    email: EmailStr
    username: str
    avatar_url: str
    role: RoleUpdate
    created_at: datetime
    collections: List[CollectionBase]


class UserUpdate(BaseModel):
    """
    Shared User properties for updating.
    """
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    avatar_url: Optional[str] = None


class UserPrivate(BaseModel):
    """
    Shared User properties for private usage.
    """
    id: PydanticObjectId
    uuid: UUID
    role: RoleBase
    email: str
    username: str
    collections: List[CollectionBase]
    avatar_url: str
    created_at: datetime


class UserStats(BaseModel):
    """
    Shared User properties for stats.
    """
    stats: Stats
