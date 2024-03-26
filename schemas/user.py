from datetime import datetime
from typing import Optional
from beanie import PydanticObjectId
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from config import settings


class UserBase(BaseModel):
    """
    Shared User properties for registration.
    """
    email: str
    username: str
    password: str
    avatar_url: Optional[str] = f'{settings.APP_URL}/static/images/blank_avatar.jpg'


class UserPublic(BaseModel):
    """
    Shared User properties for public usage.
    """
    email: EmailStr
    username: str
    avatar_url: str
    created_at: datetime


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
    role: str
    email: EmailStr
    username: str
    avatar_url: str
    created_at: datetime
