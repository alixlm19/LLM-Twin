from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar

from selenium.webdriver.common.options import ArgOptions
from selenium.webdriver.remote.webdriver import WebDriver

DriverType = TypeVar("DriverType", bound=WebDriver)
DriverOptionsType = TypeVar(
    "DriverOptionsType",
    bound=ArgOptions,
)


class BaseCrawler(ABC):
    # TODO: change type of model
    model: Any

    @abstractmethod
    def extract(self, url: str, /, **kwargs) -> None:
        pass


class BaseSeleniumCrawler(BaseCrawler, ABC):
    def set_options(
        self, options: list[str], options_handler: Type[DriverOptionsType]
    ) -> None:
        self.options_handler = options_handler()
