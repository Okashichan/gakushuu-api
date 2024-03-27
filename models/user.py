from typing import Annotated, Optional
from datetime import datetime
from uuid import UUID, uuid4

from beanie import Document, Indexed, Link
from pydantic import EmailStr, Field
from config import settings
from models.role import Role


class User(Document):
    uuid: UUID = Field(default_factory=uuid4)
    email: Annotated[EmailStr, Indexed(unique=True)] = None
    username: Annotated[str, Indexed(unique=True)] = None
    password: str = None
    role: Link[Role] = None

    avatar_url: Optional[str] = f'{settings.APP_URL}/static/images/blank_avatar.jpg'
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
