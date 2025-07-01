from typing import TypeVar

from llm_twin.domain.base.nosql import NoSQLBaseDocument

DocT = TypeVar("DocT", bound=NoSQLBaseDocument)
__all__ = ["DocT"]
