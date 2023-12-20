from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class Role(BaseModel):
    name: str

    class Config():
        from_attributes = True


class RoleBase(BaseModel):
    name: str


class RoleDisplay(BaseModel):
    id: int
    name: str

    class Config():
        from_attributes = True


class Dictionary(BaseModel):
    original: str
    en_translation: str
    ua_translation: str
    romanization: str
    transliteration: str
    comment: str

    class Config():
        from_attributes = True


class DictionaryBase(BaseModel):
    original: str
    en_translation: str
    ua_translation: str
    romanization: str
    transliteration: str
    comment: str
    created_at: datetime
    last_modified: datetime
    author_id: int


class DictionaryDisplay(BaseModel):
    original: str
    en_translation: str
    ua_translation: str
    romanization: str
    transliteration: str
    comment: str
    created_at: datetime
    last_modified: datetime


class DictionaryUpdate(BaseModel):
    original: str
    en_translation: str
    ua_translation: str
    romanization: str
    transliteration: str
    comment: str
    last_modified: datetime


class UserBase(BaseModel):
    username: str
    password_hash: str
    email: str
    avatar: str = 'http://127.0.0.1:8000/static/blank_avatar.jpg'
    created_at: datetime
    role_id: int


class UserDisplay(BaseModel):
    username: str
    password_hash: str
    email: str
    avatar: str
    created_at: datetime
    role: Role
    dictionary: List[Dictionary] = []

    class Config():
        from_attributes = True
