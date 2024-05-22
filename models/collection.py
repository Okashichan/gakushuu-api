from typing import Optional, List
from uuid import UUID, uuid4
from beanie import Document, Link
from pydantic import Field
from models.dictionary import Dictionary


class Collection(Document):
    uuid: UUID = Field(default_factory=uuid4)
    name: str = None
    description: Optional[str] = None
    is_public: bool = False

    words: Optional[List[Link[Dictionary]]] = []
