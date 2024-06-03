from datetime import datetime
from typing import Any, List, Optional
from pydantic import BaseModel
from uuid import UUID

from schemas.user_dict import UserOut


class DictionaryBase(BaseModel):
    uuid: UUID
    idseq: Optional[int]
    kanji: Optional[str]
    hiragana: str
    katakana: Optional[str]
    romaji: str
    transliteration: str
    kunyomi: Optional[str]
    onyomi: Optional[str]
    en_translation: str
    ua_translation: Optional[str]
    approved: bool
    updated_at: datetime
    approved_by: Optional["UserOut"]
    created_by: Optional["UserOut"]


class DictionaryCreate(BaseModel):
    idseq: Optional[int]
    kanji: Optional[str]
    hiragana: str
    katakana: Optional[str]
    romaji: str
    transliteration: str
    kunyomi: Optional[str]
    onyomi: Optional[str]
    en_translation: str
    ua_translation: Optional[str]


class DictionaryCollection(DictionaryCreate):
    uuid: UUID


class DictionaryMassSearch(BaseModel):
    en_sourse: Optional[List[Any]]
    ua_sourse: Optional[List[DictionaryBase]]
