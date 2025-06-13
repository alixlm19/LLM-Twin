import os
import tempfile
import tomllib
from abc import ABC, abstractmethod
from typing import Any

from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.options import ArgOptions
from selenium.webdriver.remote.webdriver import WebDriver

from .errors import EmptyDriverSettingsError, InvalidDriverSettingsSchemaError
from .schema import DriverOptions, DriverSettings


class BaseCrawler(ABC):
    # TODO: change type of model
    model: Any

    @abstractmethod
    def extract(self, url: str, /, **kwargs) -> None:
        pass


class BaseSeleniumCrawler(BaseCrawler, ABC):
    def extract(self, url: str, /, **kwargs) -> None:
        return super().extract(url, **kwargs)

    def set_driver(self, driver: WebDriver) -> "BaseSeleniumCrawler":
        self.driver = driver
        return self

    def check_driver_installed(self, driver: WebDriver) -> bool: ...

    def set_options_handler(self) -> "BaseSeleniumCrawler":
        self.options_handler: ArgOptions
        driver_type: str = self.driver.__module__.split(".")[2]
        match driver_type:
            case "chrome":
                self.options_handler = webdriver.ChromeOptions()
            case "edge":
                self.options_handler = webdriver.EdgeOptions()
            case "safari":
                self.options_handler = webdriver.SafariOptions()
            case "firefox":
                self.options_handler = webdriver.FirefoxOptions()

        logger.info(f"Logger options set to {driver_type.title()}Options.")

        return self

    def from_config(self, path: None | str = None) -> "BaseSeleniumCrawler":
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
        option: str
        if "args" in options.keys():
            for option_arg in options["args"]:
                option = f"--{option_arg}"
                self.options_handler.add_argument(option)

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
                self.options_handler.add_argument(option)

                logger.info(f"Added option: {option}")

        return self
