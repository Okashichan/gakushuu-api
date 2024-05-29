from typing import Annotated, Optional
from datetime import datetime
from uuid import UUID, uuid4

from beanie import Document, Indexed, Link
from pydantic import Field
from models.user import User


class Dictionary(Document):
    uuid: UUID = Field(default_factory=uuid4)
    idseq: Optional[Annotated[int, Indexed(unique=True)]] = None
    kanji: Optional[str] = None
    hiragana: str = None
    katakana: Optional[str] = None
    romaji: str = Optional[None]
    transliteration: Optional[str] = None
    kunyomi: Optional[str] = None
    onyomi: Optional[str] = None
    en_translation: str = None
    ua_translation: Optional[str] = None
    approved: Optional[bool] = False

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    created_by: Link[User] = None
    approved_by: Optional[Link[User]] = None
