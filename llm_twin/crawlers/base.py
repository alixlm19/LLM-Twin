# import chromedriver_autoinstaller

from abc import ABC, abstractmethod
from tempfile import mkdtemp
from typing import Any, TypeVar

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


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

    _DriverType = TypeVar("_DriverType", bound=WebDriver)

    def __init__(self, scroll_limit: int = 5) -> None:
        super().__init__()

        options: BaseSeleniumCrawler._DriverOptionsType = webdriver.ChromeOptions()

        options.add_argument("--no-sandbox")
        options.add_argument("--headless=new")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-background-networking")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        options.add_argument("--remote-debugging-port=9226")

        self.set_extra_driver_options(options)

        self.scroll_limit: int = scroll_limit
        self.driver: BaseSeleniumCrawler._DriverType = webdriver.Chrome(options=options)

    def set_extra_driver_options(self, options: _DriverOptionsType) -> None:
        pass
