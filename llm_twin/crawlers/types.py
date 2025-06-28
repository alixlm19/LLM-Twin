from dataclasses import dataclass
from typing import Generic, Type, TypeVar

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

TDriver = TypeVar("TDriver")
TOptions = TypeVar("TOptions")
TService = TypeVar("TService")
TManager = TypeVar("TManager")


@dataclass
class DriverBundle(Generic[TDriver, TOptions, TService, TManager]):
    driver: Type[TDriver]
    options: Type[TOptions]
    service: Type[TService]
    driver_manager: Type[TManager]


CHROME_BUNDLE = DriverBundle[
    webdriver.Chrome,
    webdriver.ChromeOptions,
    webdriver.ChromeService,
    ChromeDriverManager,
](
    driver=webdriver.Chrome,
    options=webdriver.ChromeOptions,
    service=webdriver.ChromeService,
    driver_manager=ChromeDriverManager,
)

EDGE_BUNDLE = DriverBundle[
    webdriver.Edge,
    webdriver.EdgeOptions,
    webdriver.EdgeService,
    EdgeChromiumDriverManager,
](
    driver=webdriver.Edge,
    options=webdriver.EdgeOptions,
    service=webdriver.EdgeService,
    driver_manager=EdgeChromiumDriverManager,
)
FIREFOX_BUNDLE = DriverBundle[
    webdriver.Firefox,
    webdriver.FirefoxOptions,
    webdriver.FirefoxService,
    GeckoDriverManager,
](
    driver=webdriver.Firefox,
    options=webdriver.FirefoxOptions,
    service=webdriver.FirefoxService,
    driver_manager=GeckoDriverManager,
)

SUPPORTED_SERVICE_TYPES = (
    webdriver.ChromeService | webdriver.EdgeService | webdriver.FirefoxService
)

SUPPORTED_DRIVER_TYPES = webdriver.Chrome | webdriver.Edge | webdriver.Firefox

SUPPORTED_DRIVER_CLASS_TYPES = (
    Type[webdriver.Chrome] | Type[webdriver.Edge] | Type[webdriver.Firefox]
)

SUPPORTED_OPTIONS_TYPES = (
    webdriver.ChromeOptions | webdriver.EdgeOptions | webdriver.FirefoxOptions
)
