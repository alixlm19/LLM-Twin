from abc import ABC
from typing import Optional

from pydantic import UUID4, Field

from .base import NoSQLBaseDocument


class UserDocument(NoSQLBaseDocument):
    first_name: str
    last_name: str

    class Settings:
        name = "users"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Document(NoSQLBaseDocument, ABC):
    content: dict
    platform: str
    author_id: UUID4 = Field(alias="author_id")
    author_full_name: str = Field(alias="author_full_name")


class RepositoryDocument(Document):
    name: str
    url: str

    class Settings:
        pass


class PostDocument(Document):
    image: Optional[str] = None
    url: str | None = None

    class Settings:
        pass


class ArticleDocument(Document):
    url: str

    class Settings:
        pass
