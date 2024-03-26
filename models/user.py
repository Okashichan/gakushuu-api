from typing import Annotated, Optional
from datetime import datetime
from uuid import UUID, uuid4

from beanie import Document, Indexed
from pydantic import EmailStr, Field


class User(Document):
    uuid: UUID = Field(default_factory=uuid4)
    email: Annotated[EmailStr, Indexed(unique=True)]
    username: str = None
    password: str = None
    role: str = "user"

    avatar_url: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
