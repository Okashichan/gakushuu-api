from datetime import datetime
from typing import Any, List, Optional
from beanie import Link, PydanticObjectId
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

from models.collection import Collection
from schemas.dictionary import DictionaryCreate


class CollectionBase(BaseModel):
    uuid: UUID
    name: str
    description: Optional[str]
    is_public: bool
    words: Optional[List[DictionaryCreate]]


class CollectionCreate(BaseModel):
    name: str
    description: Optional[str]
    is_public: bool = False
