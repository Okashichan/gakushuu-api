from datetime import datetime
from typing import Any, List, Optional
from beanie import Link, PydanticObjectId
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from models.user import User


class DictionaryBase(BaseModel):
    uuid: UUID
    idseq: Optional[int]
    kanji: str
    hiragana: str
    katakana: Optional[str]
    romaji: str
    transliteration: str
    kunyomi: str
    onyomi: str
    en_translation: str
    ua_translation: Optional[str]
    approved: bool
    updated_at: datetime
    approved_by: Optional[Link[User]]
    created_by: Link[User]


class DictionaryCreate(BaseModel):
    idseq: Optional[int]
    kanji: str
    hiragana: str
    katakana: Optional[str]
    romaji: str
    transliteration: str
    kunyomi: str
    onyomi: str
    en_translation: str
    ua_translation: Optional[str]


class DictionaryCollection(DictionaryCreate):
    uuid: UUID


class DictionaryMassSearch(BaseModel):
    en_sourse: Optional[List[Any]]
    ua_sourse: Optional[List[DictionaryBase]]
