import uuid
from abc import ABC
from typing import Generic, Type, TypeVar

from pydantic import UUID4, BaseModel, ConfigDict, Field

T = TypeVar("T", bound="NoSQLBaseDocument")


class NoSQLBaseDocument(BaseModel, Generic[T], ABC):
    id: UUID4 = Field(default_factory=uuid.uuid4)

    model_config = ConfigDict(
        populate_by_name=True,
    )

    @classmethod
    def find(cls: Type[T], **filter_options) -> T | None:
        return None

    def save(self: T, **kwargs) -> T | None:
        pass
