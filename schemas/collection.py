from datetime import datetime
from typing import Any, List, Optional
from beanie import Link, PydanticObjectId
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

from models.collection import Collection
from schemas.dictionary import DictionaryCreate, DictionaryCollection


class CollectionBase(BaseModel):
    uuid: UUID
    name: str
    description: Optional[str]
    is_public: bool
    words: Optional[List[DictionaryCollection]]


class CollectionCreate(BaseModel):
    name: str
    description: Optional[str]
    is_public: bool


class CollectionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None
