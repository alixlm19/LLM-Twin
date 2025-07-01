from functools import wraps
from typing import Callable, Concatenate

from loguru import logger

from llm_twin.settings import settings


@logger.catch
def check_if_deprecated[C, R, **P](
    error_msg: str = "This function/method is deprecated.",
    hint: str = "",
    log: bool = True,
    crash: bool = settings.CRASH_ON_DEPRECATION,
) -> Callable[
    [Callable[Concatenate[C, P], R]],
    Callable[Concatenate[C, P], R],
]:
    def decorator(
        func: Callable[Concatenate[C, P], R],
    ) -> Callable[Concatenate[C, P], R]:
        @wraps(func)
        def inner(self: C, *args: P.args, **kwargs: P.kwargs) -> R:
            if getattr(self, "_is_deprecated", False) and crash:
                raise DeprecationWarning(error_msg)

            return func(self, *args, **kwargs)

        return inner

    return decorator
