import os
import tempfile
import tomllib
from abc import ABC, abstractmethod
from typing import Any, Type

from loguru import logger
from selenium import webdriver

from .errors import (
    EmptyDriverSettingsError,
    InvalidDriverSettingsSchemaError,
    UnsupportedDriverError,
)
from .schema import DriverOptions, DriverSettings
from .types import CHROME_BUNDLE, EDGE_BUNDLE, FIREFOX_BUNDLE, DriverBundle

SUPPORTED_DRIVERS: dict[str, DriverBundle] = {
    "chrome": CHROME_BUNDLE,
    "edge": EDGE_BUNDLE,
    "firefox": FIREFOX_BUNDLE,
}

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


class BaseCrawler(ABC):
    # TODO: change type of model
    model: Any

    @abstractmethod
    def extract(self, url: str, /, **kwargs) -> None:
        pass


class BaseSeleniumCrawler(BaseCrawler, ABC):
    def __init__(self) -> None:
        super().__init__()

        self._driver: SUPPORTED_DRIVER_TYPES
        self._driver_path: str
        self._options: SUPPORTED_OPTIONS_TYPES
        self._service: SUPPORTED_SERVICE_TYPES

    def extract(self, url: str, /, **kwargs) -> None:
        return super().extract(url, **kwargs)

    def set_driver(self, driver_name: str) -> "BaseSeleniumCrawler":
        """"""
        if driver_name not in SUPPORTED_DRIVERS:
            raise UnsupportedDriverError()

        self._driver_bundle = SUPPORTED_DRIVERS[driver_name]
        self._driver_manager = self._driver_bundle.driver_manager()
        self._driver_path = self._driver_manager.install()

        self._options = self._driver_bundle.options()
        self._service = self._driver_bundle.service(self._driver_path)

        return self

    def load_config(self, path: str | None = None) -> "BaseSeleniumCrawler":
        """"""
        if path is None:
            path = os.path.join(os.getcwd(), "configs", "driver-settings.toml")

        if not os.path.exists(path):
            logger.warning(f"Could not find driver config options file: {path}")

        with open(path, "rb") as f:
            settings = tomllib.load(f)

            if not settings.keys():
                raise EmptyDriverSettingsError(
                    "Attempted to read and empty driver settings file."
                )

            selected_driver: str
            if "use" in settings:
                selected_driver = settings["use"]
            else:
                selected_driver = list(settings.keys())[0]

            settings = settings[selected_driver]

            self.settings: DriverSettings = settings

            self.set_options(self.settings["options"])
            logger.success("Driver settings loaded successfully!")

        return self

    @logger.catch
    def set_options(
        self,
        options: DriverOptions,
    ) -> "BaseSeleniumCrawler":
        """"""
        option: str
        if "args" in options.keys():
            for option_arg in options["args"]:
                option = f"--{option_arg}"
                self._options.add_argument(option)

                logger.info(f"Added option: {option}")

        if "kwargs" in options.keys():
            for option_kwarg in options["kwargs"].keys():
                value = options["kwargs"][option_kwarg]

                if isinstance(value, list) and len(value) != 2:
                    raise InvalidDriverSettingsSchemaError(
                        f"Option {option_kwarg} can only have 1 value. Got {value}."
                    )

                if value == "":
                    value = tempfile.mkdtemp()

                option = f"--{option_kwarg}={value}"
                self._options.add_argument(option)

                logger.info(f"Added option: {option}")

        return self

    def _build(self) -> None:
        self._driver = self._driver_bundle.driver(
            options=self._options, service=self._service
        )
