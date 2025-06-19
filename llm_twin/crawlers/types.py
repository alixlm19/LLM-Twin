from typing import Generic, NamedTuple, Type, TypeVar

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

TDriver = TypeVar("TDriver")
TOptions = TypeVar("TOptions")
TService = TypeVar("TService")
TManager = TypeVar("TManager")


class DriverBundle(NamedTuple, Generic[TDriver, TOptions, TService, TManager]):
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
