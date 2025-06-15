import os
import tempfile
import tomllib
from abc import ABC, abstractmethod
from typing import Any

from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.options import ArgOptions
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from .errors import (
    EmptyDriverSettingsError,
    InvalidDriverSettingsSchemaError,
    UnsupportedDriverDownloadError,
)
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

    def set_driver(
        self, driver: WebDriver, install_if_missing: bool = True
    ) -> "BaseSeleniumCrawler":
        BaseSeleniumCrawler.install_or_get_driver(driver.name, install_if_missing)
        self.driver = driver
        return self

    @classmethod
    def install_or_get_driver(
        cls,
        driver_name: str,
        install_if_missing: bool = False,
        set_file_permissions: bool = False,
    ) -> str:
        driver_manager: (
            ChromeDriverManager | EdgeChromiumDriverManager | GeckoDriverManager
        )
        match driver_name:
            case "chrome":
                driver_manager = ChromeDriverManager()
            case "edge":
                driver_manager = EdgeChromiumDriverManager()
            case "firefox":
                driver_manager = GeckoDriverManager()
            case _:
                raise UnsupportedDriverDownloadError()

        if install_if_missing:
            return driver_manager.install()

        driver_path = driver_manager._get_driver_binary_path(driver_manager.driver)
        if set_file_permissions:
            os.chmod(driver_path, 0o755)

        return driver_path

    def set_options_handler(self, driver_name: str | None) -> "BaseSeleniumCrawler":
        self.options_handler: ArgOptions
        if driver_name is None:
            driver_name = self.driver.__module__.split(".")[2]
        match driver_name:
            case "chrome":
                self.options_handler = webdriver.ChromeOptions()
            case "edge":
                self.options_handler = webdriver.EdgeOptions()
            case "safari":
                self.options_handler = webdriver.SafariOptions()
            case "firefox":
                self.options_handler = webdriver.FirefoxOptions()

        logger.info(f"Logger options set to {driver_name.title()}Options.")

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

            print(selected_driver)
            self.set_options_handler(selected_driver)
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
