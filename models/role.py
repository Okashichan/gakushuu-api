from uuid import UUID, uuid4
from beanie import Document
from pydantic import Field


class Role(Document):
    uuid: UUID = Field(default_factory=uuid4)
    name: str = None
