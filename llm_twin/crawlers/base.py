from abc import ABC, abstractmethod
from typing import Any, TypeVar

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

_DriverType = TypeVar("_DriverType", bound=WebDriver)


class BaseCrawler(ABC):
    # TODO: change type of model
    model: Any

    @abstractmethod
    def extract(self, url: str, /, **kwargs) -> None:
        pass


class BaseSeleniumCrawler(BaseCrawler, ABC):
    _DriverOptionsType = TypeVar(
        "_DriverOptionsType",
        bound=(
            webdriver.EdgeOptions
            | webdriver.ChromeOptions
            | webdriver.FirefoxOptions
            | webdriver.SafariOptions
        ),
    )

    def set_options(
        self, options: list[str], options_handler: _DriverOptionsType
    ) -> None:
        self.options = options_handler(options)
