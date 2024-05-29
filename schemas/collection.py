
from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID
from schemas.dictionary import DictionaryCollection


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
