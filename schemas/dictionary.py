from datetime import datetime
from typing import Any, List, Optional
from beanie import PydanticObjectId
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class DictionaryBase(BaseModel):
    idseq: Optional[int]
    kanji: str
    hiragana: str
    katakana: str
    romaji: str
    transliteration: str
    kunyomi: str
    onyomi: str
    en_translation: str
    ua_translation: Optional[str]


class DictionaryMassSearch(BaseModel):
    en_sourse: Optional[List[Any]]
    ua_sourse: Optional[List[DictionaryBase]]
