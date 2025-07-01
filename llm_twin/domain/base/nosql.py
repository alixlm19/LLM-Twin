import uuid
from abc import ABC
from typing import Type

from pydantic import UUID4, BaseModel, ConfigDict, Field


class NoSQLBaseDocument[T](BaseModel, ABC):
    id: UUID4 = Field(default_factory=uuid.uuid4)

    model_config = ConfigDict(
        populate_by_name=True,
    )

    @classmethod
    def find(cls: Type[T], **filter_options) -> T | None:
        return None

    def save(self: T, **kwargs) -> T | None:
        pass
